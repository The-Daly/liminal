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
from economy_model import buy_item, can_buy
from faction_model import hub_upgrade_focus, resolve_starting_loadout
from inventory_model import InventoryContainer, InventoryError, build_player_inventory
from item_registry import index_by, load_registry
from loot_model import preview_table, roll_loot
from quest_model import is_quest_complete, reward_preview
from survival_model import SanityState
from weapon_model import can_craft, can_fire, can_open_container, consume_round, craft_recipe


class DataToolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = load_registry()

    def test_registry_loads_runtime_data(self):
        self.assertIn("currency_old_movie_ticket", self.registry.items)
        self.assertIn("run_level1_service_halls_v0", self.registry.run_states)
        self.assertIn("trader_broken_kiosk_v0", self.registry.traders)
        self.assertIn("npc_tom_quartermaster_v0", self.registry.npcs)
        self.assertIn("quest_first_service_halls_recovery", self.registry.quests)
        self.assertIn("weapon_service_pistol_v0", self.registry.weapons)
        self.assertIn("ammo_type_9mm_crude", self.registry.ammo)
        self.assertIn("recipe_crude_9mm_rounds_v0", self.registry.crafting_recipes)
        self.assertIn("container_level1_bntg_supply_crate_v0", self.registry.containers)
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
        self.assertIn("RouteWall", hub_upgrade_focus(self.registry, "clippers"))

    def test_trader_purchase_uses_movie_tickets(self):
        inventory = InventoryContainer("buyer", max_slots=4)
        inventory.add_item(self.registry, "currency_old_movie_ticket", 25)
        self.assertTrue(can_buy(self.registry, "trader_broken_kiosk_v0", "consumable_almond_water", 1, inventory))
        buy_item(self.registry, "trader_broken_kiosk_v0", "consumable_almond_water", 1, inventory)
        self.assertEqual(inventory.quantity("currency_old_movie_ticket"), 0)
        self.assertEqual(inventory.quantity("consumable_almond_water"), 1)

    def test_quest_completion_and_rewards(self):
        inventory = InventoryContainer("quest", max_slots=4)
        quest_id = "quest_first_service_halls_recovery"
        self.assertFalse(is_quest_complete(self.registry, quest_id, inventory))
        inventory.add_item(self.registry, "consumable_almond_water", 1)
        inventory.add_item(self.registry, "item_scrap_metal", 3)
        self.assertTrue(is_quest_complete(self.registry, quest_id, inventory))
        self.assertEqual(reward_preview(self.registry, quest_id), [("currency_old_movie_ticket", 20)])

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


if __name__ == "__main__":
    unittest.main()
