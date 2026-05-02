import json
import random
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from extraction_model import can_extract
from economy_model import buy_item, can_buy, sell_preview
from faction_model import hub_upgrade_focus, resolve_starting_loadout
from inventory_model import InventoryContainer, InventoryError, build_player_inventory
from item_registry import index_by, load_registry
from level_layout_model import faction_foothold_zones, shortest_route_seconds
from loot_model import container_owner, is_level1_weapon_armor_sparse, preview_table, roll_loot
from navigation_marker_model import is_marker_expired, marker_visibility
from npc_roster_model import faction_roster, hireable_security_npcs, npcs_by_service, security_brokers
from quest_model import is_quest_complete, quest_ids_for_npc, reward_preview
from social_model import can_form_squad, can_players_damage_each_other, radio_connects_squadmates
from survival_model import SanityState
from weapon_model import can_craft, can_fire, can_open_container, consume_round, craft_recipe, roll_noise_response


class DataToolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = load_registry()

    def test_registry_loads_runtime_data(self):
        self.assertIn("currency_old_movie_ticket", self.registry.items)
        self.assertIn("run_level1_service_halls_v0", self.registry.run_states)
        self.assertIn("trader_the_turnstile_v0", self.registry.traders)
        self.assertIn("npc_marrow_vell_quartermaster_v0", self.registry.npcs)
        self.assertIn("npc_roster_marrow_vell", self.registry.npc_roster)
        self.assertIn("quest_still_water", self.registry.quests)
        self.assertIn("weapon_service_pistol_v0", self.registry.weapons)
        self.assertIn("ammo_type_9mm_crude", self.registry.ammo)
        self.assertIn("recipe_crude_9mm_rounds_v0", self.registry.crafting_recipes)
        self.assertIn("container_level1_bntg_supply_crate_v0", self.registry.containers)
        self.assertIn("marker_trail_string_v0", self.registry.navigation_markers)
        self.assertIn("noise_level1_gunshot_flicker_v0", self.registry.noise_responses)
        self.assertIn("density_level1_slim_v0", self.registry.loot_density)
        self.assertIn("social_faction_safe_squads_v0", self.registry.social_rules)
        self.assertIn("level1_service_halls", self.registry.level_layouts)
        self.assertEqual(len(self.registry.factions), 3)

    def test_duplicate_ids_fail(self):
        records = [{"item_id": "same"}, {"item_id": "same"}]
        with self.assertRaises(ValueError):
            index_by(records, "item_id", "test")

    def test_bad_rarity_enum_fails_schema(self):
        schema = json.loads((ROOT / "data/schemas/item.schema.json").read_text(encoding="utf-8"))
        bad_item = {
            "item_id": "bad",
            "display_name": "Bad",
            "category": "Test",
            "rarity": "Legendary",
            "stackable": True,
            "can_be_lost_on_death": True,
        }
        errors = list(Draft202012Validator(schema).iter_errors(bad_item))
        self.assertTrue(errors)

    def test_inventory_stacks_and_removes(self):
        container = InventoryContainer("test", max_slots=2)
        container.add_item(self.registry, "consumable_almond_water", 11)
        self.assertEqual(container.quantity("consumable_almond_water"), 11)
        self.assertEqual(len(container.stacks), 2)
        container.remove_item("consumable_almond_water", 6)
        self.assertEqual(container.quantity("consumable_almond_water"), 5)

    def test_storage_cap_rejects_without_partial_add(self):
        container = InventoryContainer("tiny", max_slots=1)
        with self.assertRaises(InventoryError):
            container.add_item(self.registry, "consumable_almond_water", 11)
        self.assertEqual(container.quantity("consumable_almond_water"), 0)

    def test_death_wipes_carried_and_preserves_personal(self):
        inventory = build_player_inventory(self.registry)
        inventory.carried.add_item(self.registry, "currency_old_movie_ticket", 5)
        inventory.personal.add_item(self.registry, "relic_golden_admit_one_ticket", 1)
        inventory.apply_death()
        self.assertEqual(inventory.carried.quantity("currency_old_movie_ticket"), 0)
        self.assertEqual(inventory.personal.quantity("relic_golden_admit_one_ticket"), 1)

    def test_sanity_drain_and_almond_water(self):
        rule = self.registry.sanity_rules["sanity_level1_service_halls_v0"]
        sanity = SanityState.from_rule(rule)
        sanity.drain_seconds(60)
        self.assertEqual(sanity.current, 96)
        sanity.drain_seconds(1200)
        self.assertTrue(sanity.is_low)
        sanity.consume_almond_water()
        self.assertGreater(sanity.current, sanity.low_threshold)

    def test_hidden_extraction_requires_ticket(self):
        inventory = build_player_inventory(self.registry)
        extraction_id = "extract_level1_hidden_ticket_booth"
        self.assertFalse(can_extract(self.registry, extraction_id, inventory.carried))
        inventory.carried.add_item(self.registry, "currency_old_movie_ticket")
        self.assertTrue(can_extract(self.registry, extraction_id, inventory.carried))

    def test_loot_roll_and_preview(self):
        rng = random.Random(1)
        item_id = roll_loot(self.registry, "loot_level1_basic", rng)
        self.assertIn(item_id, self.registry.items)
        preview = preview_table(self.registry, "loot_level1_basic")
        self.assertTrue(any(row["item_id"] == "item_scrap_metal" for row in preview))

    def test_faction_loadout_resolves_items(self):
        loadout = resolve_starting_loadout(self.registry, "clippers")
        self.assertTrue(any(item["item_id"] == "tool_clippers_camcorder" for item in loadout))
        self.assertFalse(any(item["category"] in ("Weapon", "Armor", "Ammo") for item in loadout))
        self.assertIn("RouteWall", hub_upgrade_focus(self.registry, "clippers"))

    def test_trader_purchase_uses_movie_tickets(self):
        inventory = InventoryContainer("buyer", max_slots=4)
        inventory.add_item(self.registry, "currency_old_movie_ticket", 25)
        self.assertTrue(can_buy(self.registry, "trader_the_turnstile_v0", "consumable_almond_water", 1, inventory))
        buy_item(self.registry, "trader_the_turnstile_v0", "consumable_almond_water", 1, inventory)
        self.assertEqual(inventory.quantity("currency_old_movie_ticket"), 0)
        self.assertEqual(inventory.quantity("consumable_almond_water"), 1)
        self.assertEqual(sell_preview(self.registry, "item_scrap_metal", 3), 9)

    def test_quest_completion_and_rewards(self):
        inventory = InventoryContainer("quest", max_slots=4)
        quest_id = "quest_still_water"
        self.assertFalse(is_quest_complete(self.registry, quest_id, inventory))
        inventory.add_item(self.registry, "consumable_almond_water", 1)
        self.assertTrue(is_quest_complete(self.registry, quest_id, inventory))
        self.assertEqual(reward_preview(self.registry, quest_id), [("currency_old_movie_ticket", 15)])
        expected_quests = {
            "quest_still_water",
            "quest_floor_gives_way",
            "quest_back_to_one",
            "quest_pry_rights",
            "quest_ticket_hunger",
        }
        self.assertTrue(expected_quests.issubset(set(self.registry.quests)))
        self.assertEqual(set(quest_ids_for_npc(self.registry, "npc_marrow_vell_quartermaster_v0")), expected_quests)

    def test_weapon_ammo_consumption(self):
        inventory = InventoryContainer("weapon", max_slots=4)
        weapon_id = "weapon_service_pistol_v0"
        self.assertFalse(can_fire(self.registry, weapon_id, inventory))
        inventory.add_item(self.registry, "ammo_9mm_crude", 2)
        self.assertTrue(can_fire(self.registry, weapon_id, inventory))
        consume_round(self.registry, weapon_id, inventory)
        self.assertEqual(inventory.quantity("ammo_9mm_crude"), 1)

    def test_ammo_crafting_recipe(self):
        inventory = InventoryContainer("craft", max_slots=6)
        recipe_id = "recipe_crude_9mm_rounds_v0"
        inventory.add_item(self.registry, "item_spent_casings", 6)
        inventory.add_item(self.registry, "item_gunpowder_pouch", 1)
        inventory.add_item(self.registry, "item_scrap_metal", 2)
        self.assertTrue(can_craft(self.registry, recipe_id, inventory))
        craft_recipe(self.registry, recipe_id, inventory)
        self.assertEqual(inventory.quantity("ammo_9mm_crude"), 6)

    def test_crowbar_gated_container(self):
        inventory = InventoryContainer("crate", max_slots=4)
        container_id = "container_level1_bntg_supply_crate_v0"
        self.assertFalse(can_open_container(self.registry, container_id, inventory))
        inventory.add_item(self.registry, "tool_bntg_crowbar")
        self.assertTrue(can_open_container(self.registry, container_id, inventory))
        self.assertEqual(container_owner(self.registry, container_id), "bntg")

    def test_trail_string_marker_rules(self):
        marker_id = "marker_trail_string_v0"
        marker = self.registry.navigation_markers[marker_id]
        self.assertEqual(marker_visibility(self.registry, marker_id), "SelfAndSquad")
        self.assertEqual(marker["duration_seconds"], 3600)
        self.assertFalse(is_marker_expired(100, 3699, marker["duration_seconds"]))
        self.assertTrue(is_marker_expired(100, 3700, marker["duration_seconds"]))

    def test_gun_noise_response_has_varied_level_specific_outcomes(self):
        table_id = "noise_level1_gunshot_flicker_v0"
        response_types = {response["response_type"] for response in self.registry.noise_responses[table_id]["responses"]}
        self.assertIn("None", response_types)
        self.assertIn("EntityApproach", response_types)
        outcomes = {roll_noise_response(self.registry, table_id, random.Random(seed))["response_type"] for seed in range(30)}
        self.assertGreaterEqual(len(outcomes), 2)

    def test_level1_loot_density_keeps_weapons_and_armor_rare(self):
        self.assertTrue(is_level1_weapon_armor_sparse(self.registry))

    def test_faction_safe_squad_rules_disable_team_kill(self):
        self.assertFalse(can_players_damage_each_other(self.registry, "meg", "meg"))
        self.assertFalse(can_players_damage_each_other(self.registry, "meg", "meg", same_squad=True))
        self.assertTrue(can_players_damage_each_other(self.registry, "meg", "bntg"))
        self.assertTrue(can_form_squad(self.registry, ["clippers", "clippers"]))
        self.assertFalse(can_form_squad(self.registry, ["meg", "bntg"]))
        self.assertTrue(radio_connects_squadmates(self.registry))

    def test_master_npc_roster_has_roles_and_security_options(self):
        self.assertGreaterEqual(len(self.registry.npc_roster), 21)
        names = {npc["display_name"] for npc in self.registry.npc_roster.values()}
        self.assertEqual(len(names), len(self.registry.npc_roster))
        self.assertIn("Marrow Vell", names)
        self.assertIn("The Turnstile", names)
        self.assertGreaterEqual(len(npcs_by_service(self.registry, "Quest")), 6)
        self.assertGreaterEqual(len(npcs_by_service(self.registry, "Buy")), 6)
        self.assertGreaterEqual(len(hireable_security_npcs(self.registry)), 4)
        self.assertGreaterEqual(len(security_brokers(self.registry)), 4)
        self.assertGreaterEqual(len(faction_roster(self.registry, "meg")), 5)

    def test_level_layout_faction_footholds_and_spacing(self):
        level_id = "level1_service_halls"
        layout = self.registry.level_layouts[level_id]
        self.assertGreaterEqual(layout["footprint_meters"]["width"], 800)
        self.assertGreaterEqual(layout["footprint_meters"]["height"], 600)
        self.assertGreaterEqual(layout["target_run_minutes"]["min"], 18)
        footholds = faction_foothold_zones(self.registry, level_id)
        self.assertEqual(footholds["meg"], "meg_archive_office")
        self.assertEqual(footholds["bntg"], "bntg_broken_trader_kiosk")
        self.assertEqual(footholds["clippers"], "clippers_route_wall")
        meg_to_bntg = shortest_route_seconds(self.registry, level_id, footholds["meg"], footholds["bntg"])
        bntg_to_clippers = shortest_route_seconds(self.registry, level_id, footholds["bntg"], footholds["clippers"])
        self.assertIsNotNone(meg_to_bntg)
        self.assertIsNotNone(bntg_to_clippers)
        self.assertGreaterEqual(meg_to_bntg, 540)
        self.assertGreaterEqual(bntg_to_clippers, 540)


if __name__ == "__main__":
    unittest.main()
