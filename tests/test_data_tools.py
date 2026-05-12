import json
import random
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from character_framework_model import appearance_presets_for_faction, can_use_appearance, faction_character_rules
from extraction_model import can_extract
from economy_model import buy_item, can_buy, sell_preview
from faction_model import build_new_realm_inventory, hub_upgrade_focus, reset_realm_for_faction, resolve_starting_loadout
from frontend_menu_model import (
    MenuFlowState,
    bootstrap_menu_flow,
    build_character_selection_snapshot,
    build_main_player_menu_snapshot,
    build_server_browser_snapshot,
    build_subpanel_snapshot,
    build_title_shell_copy,
    character_setup_defaults,
    faction_lock_warning,
    navigate_route,
    ordered_routes,
    resolve_next_route,
    transition_targets,
)
from frontend_operations_hub_model import build_operations_hub_snapshot
from inventory_model import InventoryContainer, InventoryError, build_player_inventory
from item_registry import index_by, load_registry
from level_layout_model import faction_foothold_zones, shortest_route_seconds
from loot_model import container_owner, is_level1_weapon_armor_sparse, preview_table, roll_loot
from navigation_marker_model import is_marker_expired, marker_visibility
from npc_roster_model import faction_roster, hireable_security_npcs, npcs_by_service, security_brokers
from persistence_model import (
    PersistentRealmCollection,
    RealmCharacterRecord,
    FrontendSessionState,
    load_frontend_session,
    load_persistent_collection,
    load_profile,
    new_local_profile,
    save_frontend_session,
    save_persistent_collection,
    save_profile,
)
from playable_loop_model import LoopOutcome, simulate_death_run, simulate_successful_run
from persistent_world_model import (
    can_change_faction,
    can_create_character_on_realm,
    create_character_profile,
    profiles_by_server_type,
    realm_menu_summary,
    realm_descriptor,
)
from project_board_model import HubProgressState, contribute_all_possible, contribute_item, is_upgrade_complete
from quest_model import is_quest_complete, quest_ids_for_npc, reward_preview
from social_model import can_form_squad, can_players_damage_each_other, radio_connects_squadmates
from survival_model import SanityState
from weapon_model import can_craft, can_fire, can_open_container, consume_round, craft_recipe, roll_noise_response
from validate_seed_data import validate_records


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

    def test_registry_loads_frontend_and_persistent_world_data(self):
        self.assertIn("official_north_america_01", self.registry.server_realms)
        self.assertIn("wipe_official_biannual", self.registry.wipe_schedules)
        self.assertIn("appearance_meg_operator_field_v0", self.registry.character_appearance)
        self.assertIn("menu_title_shell", self.registry.menu_routes)

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

    def test_validation_reports_missing_required_field_readably(self):
        schema = {
            "type": "object",
            "required": ["item_id", "display_name"],
            "properties": {
                "item_id": {"type": "string"},
                "display_name": {"type": "string"},
            },
        }

        with self.assertRaises(ValueError) as ctx:
            validate_records("items.seed.json", schema, [{"item_id": "ticket"}])

        message = str(ctx.exception)
        self.assertIn("items.seed.json[0]", message)
        self.assertIn("(required)", message)
        self.assertIn("'display_name' is a required property", message)

    def test_validation_reports_bad_enum_readably(self):
        schema = {
            "type": "object",
            "required": ["rarity"],
            "properties": {
                "rarity": {"enum": ["Common", "Uncommon"]},
            },
        }

        with self.assertRaises(ValueError) as ctx:
            validate_records("items.seed.json", schema, [{"rarity": "Legendary"}])

        message = str(ctx.exception)
        self.assertIn("items.seed.json[0].rarity", message)
        self.assertIn("(enum)", message)
        self.assertIn("'Legendary' is not one of ['Common', 'Uncommon']", message)

    def test_inventory_stacks_and_removes(self):
        container = InventoryContainer("test", max_slots=2)
        container.add_item(self.registry, "consumable_almond_water", 11)
        self.assertEqual(container.quantity("consumable_almond_water"), 11)
        self.assertEqual(len(container.stacks), 2)
        container.remove_item("consumable_almond_water", 6)
        self.assertEqual(container.quantity("consumable_almond_water"), 5)

    def test_inventory_tracks_weight_cap(self):
        container = InventoryContainer("weighted", max_slots=10, max_weight=2.0)
        container.add_item(self.registry, "item_flashlight")
        container.add_item(self.registry, "consumable_almond_water", 6)
        self.assertAlmostEqual(container.total_weight(self.registry), 2.0)
        with self.assertRaises(InventoryError):
            container.add_item(self.registry, "currency_old_movie_ticket")
        self.assertEqual(container.quantity("currency_old_movie_ticket"), 0)

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

    def test_personal_storage_caps_movie_tickets_with_overflow_stub(self):
        inventory = build_player_inventory(self.registry)
        result = inventory.personal.store_with_overflow(self.registry, "currency_old_movie_ticket", 5100)
        self.assertEqual(result.moved_quantity, 5000)
        self.assertIsNotNone(result.overflow)
        self.assertEqual(result.overflow.quantity, 100)
        self.assertEqual(result.overflow.cap_key, "MovieTickets")
        self.assertEqual(inventory.personal.quantity("currency_old_movie_ticket"), 5000)

    def test_transfer_to_personal_preserves_overflow_in_carried(self):
        inventory = build_player_inventory(self.registry)
        inventory.carried.add_item(self.registry, "consumable_almond_water", 55)
        result = inventory.move_carried_to_personal(self.registry, "consumable_almond_water", 55)
        self.assertEqual(result.moved_quantity, 50)
        self.assertIsNotNone(result.overflow)
        self.assertEqual(result.overflow.quantity, 5)
        self.assertEqual(result.overflow.cap_key, "AlmondWater")
        self.assertEqual(inventory.personal.quantity("consumable_almond_water"), 50)
        self.assertEqual(inventory.carried.quantity("consumable_almond_water"), 5)

    def test_personal_storage_caps_weapons_by_total_count(self):
        inventory = build_player_inventory(self.registry)
        result = inventory.personal.store_with_overflow(self.registry, "weapon_service_pistol", 19)
        self.assertEqual(result.moved_quantity, 18)
        self.assertIsNotNone(result.overflow)
        self.assertEqual(result.overflow.quantity, 1)
        self.assertEqual(result.overflow.cap_key, "Weapons")
        self.assertEqual(inventory.personal.quantity("weapon_service_pistol"), 18)

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

    def test_playable_loop_successfully_extracts_to_personal_room(self):
        outcome = simulate_successful_run(self.registry, rng=random.Random(7))
        self.assertTrue(outcome.extracted)
        self.assertFalse(outcome.died)
        self.assertEqual(outcome.destination_map, "LD_PersonalRoom_Greybox")
        self.assertGreaterEqual(len(outcome.looted_item_ids), 1)
        self.assertGreaterEqual(len(outcome.deposited_item_ids), 1)

    def test_playable_loop_death_run_wipes_carried_progress(self):
        outcome = simulate_death_run(self.registry, rng=random.Random(7))
        self.assertFalse(outcome.extracted)
        self.assertTrue(outcome.died)
        self.assertIsNone(outcome.extraction_id)
        self.assertEqual(outcome.deposited_item_ids, ())

    def test_local_profile_round_trips_storage_progress_and_history(self):
        profile = new_local_profile(self.registry)
        profile.personal.add_item(self.registry, "currency_old_movie_ticket", 25)
        profile.personal.add_item(self.registry, "item_scrap_metal", 5)
        profile.hub_progress.contributions["hub_project_board_signal_lamp_v0"] = {
            "currency_old_movie_ticket": 10
        }
        profile.append_run(simulate_successful_run(self.registry, rng=random.Random(7)))

        with tempfile.TemporaryDirectory() as temp_dir:
            profile_path = Path(temp_dir) / "local_profile.json"
            save_profile(profile_path, profile)
            restored = load_profile(self.registry, profile_path)

        self.assertEqual(restored.faction_id, "meg")
        self.assertEqual(restored.personal.quantity("currency_old_movie_ticket"), 25)
        self.assertEqual(restored.personal.quantity("item_scrap_metal"), 5)
        self.assertEqual(
            restored.hub_progress.contributions["hub_project_board_signal_lamp_v0"]["currency_old_movie_ticket"],
            10,
        )
        self.assertEqual(len(restored.run_history), 1)
        self.assertTrue(restored.run_history[0].extracted)

    def test_local_profile_trims_run_history_to_latest_entries(self):
        profile = new_local_profile(self.registry)
        for index in range(25):
            profile.append_run(
                LoopOutcome(
                    faction_id="meg",
                    run_state_id=f"run_{index}",
                    extracted=False,
                    died=True,
                    extraction_id=None,
                    destination_map=None,
                    looted_item_ids=(),
                    deposited_item_ids=(),
                    completed_upgrades=(),
                    remaining_sanity=float(100 - index),
                ),
                max_entries=20,
            )

        self.assertEqual(len(profile.run_history), 20)
        self.assertEqual(profile.run_history[0].run_state_id, "run_5")
        self.assertEqual(profile.run_history[-1].run_state_id, "run_24")

    def test_persistent_realm_collection_separates_official_and_community(self):
        official = RealmCharacterRecord(
            character_id="char_official_001",
            realm_id="official_north_america_01",
            server_type="official",
            faction_id="meg",
            wipe_schedule_id="wipe_official_biannual",
            wipe_id="wipe_official_biannual_2028",
            slot_index=1,
            callsign="Archive-Delta",
            appearance_id="appearance_meg_operator_field_v0",
            role_preset="operator",
            created_at_utc="2026-05-11T12:00:00Z",
            last_login_utc="2026-05-11T12:00:00Z",
            locked_until_wipe=True,
        )
        community = RealmCharacterRecord(
            character_id="char_community_001",
            realm_id="community_rustwater_lab_01",
            server_type="community",
            faction_id="clippers",
            wipe_schedule_id="wipe_community_biannual",
            wipe_id="wipe_community_biannual_2028",
            slot_index=1,
            callsign="Route-Knot",
            appearance_id="appearance_clippers_route_runner_v0",
            role_preset="operator",
            created_at_utc="2026-05-11T12:00:00Z",
            last_login_utc="2026-05-11T12:00:00Z",
            locked_until_wipe=True,
        )
        collection = PersistentRealmCollection(
            official_characters=[official],
            community_characters=[community],
            wipe_state={
                "official_north_america_01": {"next_wipe_utc": "2028-01-01T00:00:00Z"},
                "community_rustwater_lab_01": {"next_wipe_utc": "2028-03-01T00:00:00Z"},
            },
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "persistent_realms.json"
            save_persistent_collection(path, collection)
            restored = load_persistent_collection(path)

        self.assertEqual(len(restored.official_characters), 1)
        self.assertEqual(len(restored.community_characters), 1)
        self.assertEqual(restored.official_characters[0].realm_id, "official_north_america_01")
        self.assertEqual(restored.community_characters[0].realm_id, "community_rustwater_lab_01")

    def test_faction_loadout_and_realm_reset(self):
        loadout = resolve_starting_loadout(self.registry, "meg")
        self.assertIn("tool_meg_entity_scanner", loadout.item_ids)

        inventory = build_new_realm_inventory(self.registry)
        self.assertEqual(inventory.carried.quantity("tool_meg_entity_scanner"), 1)
        inventory.personal.add_item(self.registry, "relic_golden_admit_one_ticket")

        reset_inventory = reset_realm_for_faction(self.registry, "clippers")
        self.assertEqual(reset_inventory.carried.quantity("tool_clippers_camcorder"), 1)
        self.assertEqual(reset_inventory.personal.quantity("relic_golden_admit_one_ticket"), 0)

    def test_project_board_accepts_partial_contribution_without_over_removing(self):
        state = HubProgressState(faction_id="meg")
        storage = InventoryContainer("personal", max_slots=20)
        storage.add_item(self.registry, "currency_old_movie_ticket", 10)
        result = contribute_item(
            self.registry,
            state,
            "hub_project_board_signal_lamp_v0",
            storage,
            "currency_old_movie_ticket",
            25,
        )
        self.assertEqual(result.moved_quantity, 10)
        self.assertEqual(result.remaining_quantity, 15)
        self.assertFalse(result.completed_upgrade)
        self.assertEqual(storage.quantity("currency_old_movie_ticket"), 0)
        self.assertFalse(is_upgrade_complete(self.registry, state, "hub_project_board_signal_lamp_v0"))

    def test_project_board_completes_signal_lamp_upgrade(self):
        state = HubProgressState(faction_id="meg")
        storage = InventoryContainer("personal", max_slots=20)
        storage.add_item(self.registry, "currency_old_movie_ticket", 25)
        storage.add_item(self.registry, "item_scrap_metal", 5)
        results = contribute_all_possible(self.registry, state, "hub_project_board_signal_lamp_v0", storage)
        self.assertTrue(is_upgrade_complete(self.registry, state, "hub_project_board_signal_lamp_v0"))
        self.assertIn("hub_project_board_signal_lamp_v0", state.completed_upgrades)
        self.assertTrue(any(result.completed_upgrade for result in results))
        self.assertEqual(storage.quantity("currency_old_movie_ticket"), 0)
        self.assertEqual(storage.quantity("item_scrap_metal"), 0)

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

    def test_official_realm_cap_and_queue_snapshot(self):
        descriptor = realm_descriptor(
            self.registry,
            "official_north_america_01",
            active_counts={"meg": 30, "bntg": 28, "clippers": 24},
            queue_counts={"meg": 6, "bntg": 1, "clippers": 0},
        )
        self.assertEqual(descriptor.population_cap, 90)
        self.assertEqual({state.cap for state in descriptor.faction_caps}, {30})
        meg_state = next(state for state in descriptor.faction_caps if state.faction_id == "meg")
        self.assertEqual(meg_state.current_active, 30)
        self.assertEqual(meg_state.queue_count, 6)
        self.assertFalse(can_create_character_on_realm(self.registry, "official_north_america_01", "meg", {"meg": 30}))
        self.assertTrue(can_create_character_on_realm(self.registry, "official_north_america_01", "bntg", {"bntg": 29}))

    def test_character_profile_is_server_bound_and_faction_locked(self):
        profile = create_character_profile(
            self.registry,
            realm_id="official_north_america_01",
            faction_id="meg",
            callsign="Archive-Delta",
            appearance_id="appearance_meg_operator_field_v0",
            slot_index=1,
            timestamp_utc="2026-05-11T12:00:00Z",
        )
        self.assertEqual(profile.server_type, "official")
        self.assertEqual(profile.realm_id, "official_north_america_01")
        self.assertFalse(can_change_faction(profile, profile.wipe_id))
        self.assertTrue(can_change_faction(profile, "wipe_official_biannual_2030"))

        grouped = profiles_by_server_type([profile])
        self.assertEqual(len(grouped["official"]), 1)
        self.assertEqual(len(grouped["community"]), 0)

    def test_character_profile_example_matches_schema(self):
        schema = json.loads((ROOT / "data/schemas/character_profile.schema.json").read_text(encoding="utf-8"))
        example = json.loads((ROOT / "data/examples/character_profile.example.json").read_text(encoding="utf-8"))
        errors = list(Draft202012Validator(schema).iter_errors(example))
        self.assertEqual(errors, [])

    def test_menu_flow_respects_server_first_and_existing_character_rules(self):
        routes = ordered_routes(self.registry)
        self.assertEqual(routes[0].menu_route_id, "menu_title_shell")
        self.assertEqual(resolve_next_route(MenuFlowState("menu_title_shell", None, False, False, False)), "menu_server_browser")
        self.assertEqual(
            resolve_next_route(MenuFlowState("menu_server_browser", "official_north_america_01", False, False, False)),
            "menu_faction_selection",
        )
        self.assertEqual(
            resolve_next_route(MenuFlowState("menu_server_browser", "official_north_america_01", True, False, False)),
            "menu_character_selection",
        )
        self.assertEqual(
            resolve_next_route(MenuFlowState("menu_character_selection", "official_north_america_01", True, False, False)),
            "menu_main_player_hub",
        )

    def test_realm_menu_summary_formats_population_and_wipe_context(self):
        summary = realm_menu_summary(
            self.registry,
            "official_north_america_01",
            active_counts={"meg": 30, "bntg": 28, "clippers": 24},
            queue_counts={"meg": 6, "bntg": 1, "clippers": 0},
        )
        self.assertEqual(summary.total_active, 82)
        self.assertEqual(summary.total_capacity, 90)
        self.assertEqual(summary.total_queue, 7)
        self.assertIn("Next wipe", summary.wipe_summary_text)
        self.assertIn("MEG 30/30 Q6", summary.faction_population_summary)

    def test_frontend_menu_helpers_build_server_and_faction_copy(self):
        title_copy = build_title_shell_copy()
        self.assertEqual(title_copy.current_route_id, "menu_title_shell")
        self.assertEqual(title_copy.headline_text, "Liminal Dominion")
        self.assertIn("mass wipe", title_copy.subhead_text.lower())
        self.assertEqual(title_copy.primary_action_label, "Enter Server Browser")
        self.assertEqual(title_copy.stage_counter_text, "Stage 1 / 6")

        server_snapshot = build_server_browser_snapshot(
            self.registry,
            "official_north_america_01",
            active_counts={"meg": 30, "bntg": 28, "clippers": 24},
            queue_counts={"meg": 6, "bntg": 1, "clippers": 0},
        )
        self.assertEqual(server_snapshot.selected_server_type, "official")
        self.assertIn("Official Realm", server_snapshot.server_name_text)
        self.assertIn("Population 82/90 | Queue 7", server_snapshot.queue_summary_text)
        self.assertEqual(server_snapshot.primary_action_label, "Select Realm")
        self.assertIn("Server Browser", server_snapshot.breadcrumb_text)

        warning = faction_lock_warning(self.registry, "official_north_america_01", "meg")
        self.assertIn("M.E.G.", warning)
        self.assertIn("next wipe", warning.lower())

        setup_defaults = character_setup_defaults(self.registry, "meg", slot_index=2)
        self.assertEqual(setup_defaults.selected_faction_id, "meg")
        self.assertEqual(setup_defaults.selected_appearance_id, "appearance_meg_operator_field_v0")
        self.assertEqual(setup_defaults.character_callsign, "MEG-02")

    def test_menu_bootstrap_and_main_player_snapshot_follow_existing_character(self):
        profile = create_character_profile(
            self.registry,
            realm_id="official_north_america_01",
            faction_id="meg",
            callsign="Archive-Delta",
            appearance_id="appearance_meg_operator_field_v0",
            slot_index=1,
            timestamp_utc="2026-05-11T12:00:00Z",
        )
        bootstrap = bootstrap_menu_flow(
            self.registry,
            "official_north_america_01",
            profiles=(profile,),
            route_id="menu_server_browser",
        )
        self.assertTrue(bootstrap.has_existing_character)
        self.assertEqual(bootstrap.next_route_id, "menu_character_selection")
        self.assertEqual(bootstrap.selected_character_id, profile.character_id)
        self.assertEqual(bootstrap.selected_faction_id, "meg")

        character_selection = build_character_selection_snapshot(profile)
        self.assertEqual(character_selection.selected_character_id, profile.character_id)
        self.assertIn("Existing character found", character_selection.existing_character_status_text)
        self.assertEqual(character_selection.primary_action_label, "Enter Character Menu")
        self.assertIn("Character Selection", character_selection.breadcrumb_text)

        snapshot = build_main_player_menu_snapshot(
            self.registry,
            profile,
            active_counts={"meg": 27, "bntg": 23, "clippers": 22},
            queue_counts={"meg": 2, "bntg": 0, "clippers": 1},
        )
        self.assertTrue(snapshot.deploy_enabled)
        self.assertEqual(snapshot.selected_character_id, profile.character_id)
        self.assertIn("Archive-Delta", snapshot.character_summary_text)
        self.assertIn("MEG 27/30 Q2", snapshot.faction_population_summary)
        self.assertEqual(snapshot.primary_action_label, "Deploy Operator")
        self.assertIn("Character Overview", snapshot.breadcrumb_text)

        deploy_panel = build_subpanel_snapshot(self.registry, profile, "menu_deploy_panel")
        stash_panel = build_subpanel_snapshot(self.registry, profile, "menu_stash_panel")
        settings_panel = build_subpanel_snapshot(self.registry, profile, "menu_settings_panel")
        self.assertEqual(deploy_panel.primary_action_label, "Queue Deployment")
        self.assertIn("personal storage", stash_panel.panel_summary_text.lower())
        self.assertEqual(settings_panel.secondary_action_label, "Return to Main Menu")
        self.assertIn("Deploy", deploy_panel.breadcrumb_text)

        operations_snapshot = build_operations_hub_snapshot(
            self.registry,
            profile,
            deploy_enabled=snapshot.deploy_enabled,
        )
        self.assertEqual(operations_snapshot.nav_section_title_text, "Main Menu")
        self.assertEqual(operations_snapshot.operation_brief.zone_code_text, "Zone // SH-17")
        self.assertIn("Investigate service halls", operations_snapshot.operation_brief.brief_objective_text)
        self.assertEqual(operations_snapshot.operator_status.operator_name_text, "Archive-Delta")
        self.assertIn("Credits", operations_snapshot.operator_status.currency_summary_text)
        self.assertIn("operators", operations_snapshot.footer.footer_status_text)

    def test_frontend_transition_targets_follow_route_roles(self):
        title_targets = transition_targets(MenuFlowState("menu_title_shell", None, False, False, False))
        self.assertEqual(title_targets.primary_target_route_id, "menu_server_browser")
        self.assertEqual(title_targets.secondary_target_route_id, "menu_title_shell")
        self.assertIsNone(title_targets.back_target_route_id)

        server_targets = transition_targets(
            MenuFlowState("menu_server_browser", "official_north_america_01", True, False, False)
        )
        self.assertEqual(server_targets.primary_target_route_id, "menu_character_selection")
        self.assertEqual(server_targets.back_target_route_id, "menu_title_shell")

        hub_targets = transition_targets(
            MenuFlowState("menu_main_player_hub", "official_north_america_01", True, True, True)
        )
        self.assertEqual(hub_targets.primary_target_route_id, "menu_deploy_panel")
        self.assertEqual(hub_targets.secondary_target_route_id, "menu_stash_panel")

        settings_targets = transition_targets(
            MenuFlowState("menu_settings_panel", "official_north_america_01", True, True, True)
        )
        self.assertEqual(settings_targets.secondary_target_route_id, "menu_main_player_hub")
        self.assertEqual(settings_targets.back_target_route_id, "menu_main_player_hub")

    def test_frontend_navigation_allows_expected_route_hops_and_rejects_invalid_ones(self):
        self.assertEqual(
            navigate_route(
                self.registry,
                MenuFlowState("menu_title_shell", None, False, False, False),
                "menu_server_browser",
            ),
            "menu_server_browser",
        )
        self.assertEqual(
            navigate_route(
                self.registry,
                MenuFlowState("menu_server_browser", "official_north_america_01", True, False, False),
                "menu_title_shell",
            ),
            "menu_title_shell",
        )
        self.assertEqual(
            navigate_route(
                self.registry,
                MenuFlowState("menu_main_player_hub", "official_north_america_01", True, True, True),
                "menu_deploy_panel",
            ),
            "menu_deploy_panel",
        )
        self.assertEqual(
            navigate_route(
                self.registry,
                MenuFlowState("menu_stash_panel", "official_north_america_01", True, True, True),
                "menu_main_player_hub",
            ),
            "menu_main_player_hub",
        )
        with self.assertRaises(Exception):
            navigate_route(
                self.registry,
                MenuFlowState("menu_title_shell", None, False, False, False),
                "menu_main_player_hub",
            )

    def test_frontend_session_round_trips_menu_state(self):
        session = FrontendSessionState(
            current_route_id="menu_main_player_hub",
            next_route_id="menu_deploy_panel",
            primary_target_route_id="menu_deploy_panel",
            secondary_target_route_id="menu_stash_panel",
            back_target_route_id="menu_server_browser",
            selected_realm_id="official_north_america_01",
            selected_server_type="official",
            selected_faction_id="meg",
            selected_character_id="char_official_001",
            selected_appearance_id="appearance_meg_operator_field_v0",
            character_callsign="Archive-Delta",
            has_existing_character=True,
            character_configured=True,
            current_wipe_label="Biannual Official Wipe | Next wipe 2028-01-01",
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "frontend_session.json"
            save_frontend_session(path, session)
            restored = load_frontend_session(path)

        self.assertEqual(restored.current_route_id, "menu_main_player_hub")
        self.assertEqual(restored.next_route_id, "menu_deploy_panel")
        self.assertEqual(restored.primary_target_route_id, "menu_deploy_panel")
        self.assertEqual(restored.selected_realm_id, "official_north_america_01")
        self.assertEqual(restored.selected_server_type, "official")
        self.assertTrue(restored.has_existing_character)

    def test_character_appearance_presets_are_minimal_and_faction_safe(self):
        meg_player_presets = appearance_presets_for_faction(self.registry, "meg", usable_by="player")
        bntg_player_presets = appearance_presets_for_faction(self.registry, "bntg", usable_by="player")
        clippers_player_presets = appearance_presets_for_faction(self.registry, "clippers", usable_by="player")
        self.assertGreaterEqual(len(meg_player_presets), 1)
        self.assertGreaterEqual(len(bntg_player_presets), 1)
        self.assertGreaterEqual(len(clippers_player_presets), 1)
        self.assertTrue(can_use_appearance(self.registry, "meg", "appearance_meg_operator_field_v0", "player"))
        self.assertFalse(can_use_appearance(self.registry, "meg", "appearance_bntg_salvage_runner_v0", "player"))
        rules = faction_character_rules(self.registry, "clippers")
        self.assertIn("appearance_clippers_route_runner_v0", rules.allowed_appearance_ids)
        self.assertEqual(rules.starter_identity_item_id, "tool_clippers_camcorder")

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
