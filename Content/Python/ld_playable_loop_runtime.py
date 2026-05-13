import random

import unreal

from faction_model import build_new_realm_inventory
from inventory_model import InventoryError
from item_registry import load_registry
from loot_model import roll_loot
from project_board_model import HubProgressState, contribute_all_possible
from survival_model import SanityState


LEVEL1_MAP = "LD_Level1_ServiceHalls_Greybox"
PERSONAL_MAP = "LD_PersonalRoom_Greybox"
HUB_MAP = "LD_Hub_Greybox"


def log(message: str) -> None:
    unreal.log(f"[LD Loop Runtime] {message}")


def screen_message(message: str, color=None, duration: float = 3.0) -> None:
    unreal.SystemLibrary.print_string(
        None,
        message,
        text_color=color or unreal.LinearColor(0.9, 0.85, 0.35, 1.0),
        duration=duration,
    )


def make_key(name: str):
    key = unreal.Key()
    key.set_editor_property("key_name", unreal.SystemLibrary.make_literal_name(name))
    return key


KEYS = {
    "interact": [make_key("E"), make_key("Gamepad_FaceButton_Bottom")],
    "consume": [make_key("Q")],
    "debug_death": [make_key("K")],
}


def world_name(world) -> str:
    return world.get_name() if world else ""


def map_matches(world, token: str) -> bool:
    return token in world_name(world)


def load_bp_class(path: str):
    return unreal.EditorAssetLibrary.load_blueprint_class(path)


def actor_distance(a, b) -> float:
    return a.get_actor_location().distance(b.get_actor_location())


def get_prop(obj, *names, default=None):
    for name in names:
        try:
            return obj.get_editor_property(name)
        except Exception:
            continue
    return default


class PlayLoopSession:
    def __init__(self):
        self.registry = load_registry()
        self.rng = random.Random(7)
        self.reset()

    def reset(self):
        self.inventory = build_new_realm_inventory(self.registry, "player_state_v0_meg")
        rule = self.registry.sanity_rules["sanity_level1_service_halls_v0"]
        self.sanity = SanityState.from_rule(rule, starting_sanity=100)
        self.progress = HubProgressState(faction_id="meg")
        self.looted_actor_labels: set[str] = set()
        self.last_low_sanity_notice = False
        self.state = "menu"
        self.player_pawn = None

    def carried_summary(self) -> str:
        if not self.inventory.carried.stacks:
            return "None"
        return ", ".join(f"{stack.item_id} x{stack.quantity}" for stack in self.inventory.carried.stacks)


class PlayableLoopRuntimeController:
    def __init__(self):
        self.session = PlayLoopSession()
        self.active_world = None
        self.player_class = None

    def reset_for_editor(self):
        self.active_world = None
        self.session.reset()

    def _pressed_any(self, player_controller, keys) -> bool:
        return any(player_controller.was_input_key_just_pressed(key) for key in keys)

    def _ensure_player_class(self):
        if self.player_class is None:
            self.player_class = load_bp_class("/Game/Blueprints/BP_LDPlayer")
        return self.player_class

    def _find_actor_by_label(self, world, label: str):
        for actor in unreal.EditorLevelLibrary.get_all_level_actors():
            if actor.get_world() == world and actor.get_actor_label() == label:
                return actor
        return None

    def _find_label_prefix(self, world, suffix: str):
        for actor in unreal.EditorLevelLibrary.get_all_level_actors():
            if actor.get_world() == world and actor.get_actor_label().endswith(suffix):
                return actor
        return None

    def _hide_menu_boot(self, world):
        menu_boot = self._find_actor_by_label(world, "MenuBootPawn")
        if menu_boot is None:
            return
        menu_boot.set_actor_hidden_in_game(True)
        menu_boot.set_actor_enable_collision(False)
        for component in menu_boot.get_components_by_class(unreal.PrimitiveComponent):
            component.set_hidden_in_game(True)
            component.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)

    def _sync_player_debug_state(self):
        pawn = self.session.player_pawn
        if pawn is None:
            return
        try:
            pawn.set_editor_property("CurrentSanity", float(self.session.sanity.current))
        except Exception:
            pass
        try:
            pawn.set_editor_property("CarriedInventorySummary", self.session.carried_summary())
        except Exception:
            pass

    def _spawn_or_reuse_player(self, world, player_controller, start_label_suffix: str):
        player_class = self._ensure_player_class()
        if player_class is None:
            return None

        pawn = player_controller.get_pawn()
        if pawn and pawn.get_class() == player_class:
            self.session.player_pawn = pawn
            self._sync_player_debug_state()
            return pawn

        start = self._find_label_prefix(world, start_label_suffix)
        location = unreal.Vector(0.0, 0.0, 200.0)
        rotation = unreal.Rotator(0.0, 0.0, 0.0)
        if start:
            location = start.get_actor_location()
            rotation = start.get_actor_rotation()

        pawn = None
        if hasattr(world, "actor_spawn"):
            try:
                pawn = world.actor_spawn(player_class, location, rotation)
            except Exception:
                pawn = None
        if pawn is None:
            try:
                pawn = unreal.EditorLevelLibrary.spawn_actor_from_class(player_class, location, rotation)
            except Exception:
                pawn = None
        if pawn is None:
            return None
        pawn.set_actor_label("LDG_RuntimePlayer")
        player_controller.possess(pawn)
        player_controller.show_mouse_cursor = False
        player_controller.enable_click_events = False
        player_controller.enable_mouse_over_events = False
        player_controller.set_ignore_move_input(False)
        player_controller.set_ignore_look_input(False)
        self.session.player_pawn = pawn
        self._sync_player_debug_state()
        return pawn

    def _current_nearby_actor(self, world, pawn):
        if pawn is None:
            return None
        candidates = []
        for actor in unreal.EditorLevelLibrary.get_all_level_actors():
            if actor.get_world() != world:
                continue
            label = actor.get_actor_label()
            if not label.startswith("LDG_"):
                continue
            if any(token in label for token in ["LootContainer", "Extraction_", "PersonalRoomStorage", "HubProjectBoard", "HubDeploymentGate", "FlickerStalker"]):
                candidates.append(actor)
        if not candidates:
            return None
        nearest = min(candidates, key=lambda actor: actor_distance(actor, pawn))
        if actor_distance(nearest, pawn) > 400.0:
            return None
        return nearest

    def _consume_almond_water(self):
        if self.session.inventory.carried.quantity("consumable_almond_water") <= 0:
            screen_message("No Almond Water in carried inventory.", unreal.LinearColor(0.8, 0.3, 0.3, 1.0))
            return
        self.session.inventory.carried.remove_item("consumable_almond_water", 1)
        self.session.sanity.consume_almond_water()
        self._sync_player_debug_state()
        screen_message(f"Consumed Almond Water. Sanity: {self.session.sanity.current:.0f}")

    def _handle_loot(self, actor):
        label = actor.get_actor_label()
        if label in self.session.looted_actor_labels:
            screen_message("Container already looted.", unreal.LinearColor(0.7, 0.7, 0.7, 1.0))
            return
        loot_table_id = get_prop(actor, "LootTableId", "loot_table_id", default="loot_level1_basic")
        item_id = roll_loot(self.session.registry, loot_table_id, self.session.rng)
        self.session.inventory.carried.add_item(self.session.registry, item_id)
        self.session.looted_actor_labels.add(label)
        self._sync_player_debug_state()
        screen_message(f"Looted {item_id}. Carried: {self.session.carried_summary()}")

    def _open_level(self, world, map_name: str):
        unreal.GameplayStatics.open_level(world, unreal.Name(map_name))

    def _handle_extract(self, actor, world):
        required = get_prop(actor, "RequiredItemId", "required_item_id", default="")
        if required and self.session.inventory.carried.quantity(required) <= 0:
            screen_message(f"Extraction blocked. Need {required}.", unreal.LinearColor(0.9, 0.3, 0.3, 1.0))
            return
        self.session.state = "personal_room"
        screen_message("Extraction successful. Returning to Personal Room.")
        self._open_level(world, PERSONAL_MAP)

    def _handle_personal_storage(self, world):
        moved_any = False
        for stack in list(self.session.inventory.carried.stacks):
            result = self.session.inventory.move_carried_to_personal(
                self.session.registry,
                stack.item_id,
                stack.quantity,
            )
            moved_any = moved_any or result.moved_quantity > 0
        self._sync_player_debug_state()
        if moved_any:
            screen_message("Deposited extracted loot. Routing to Hub.")
        else:
            screen_message("No carried loot to deposit.", unreal.LinearColor(0.7, 0.7, 0.7, 1.0))
        self.session.state = "hub"
        self._open_level(world, HUB_MAP)

    def _handle_project_board(self):
        results = contribute_all_possible(
            self.session.registry,
            self.session.progress,
            "hub_project_board_signal_lamp_v0",
            self.session.inventory.personal,
        )
        moved = sum(result.moved_quantity for result in results)
        complete = "hub_project_board_signal_lamp_v0" in self.session.progress.completed_upgrades
        if moved <= 0:
            screen_message("No valid contribution items in personal storage.", unreal.LinearColor(0.7, 0.7, 0.7, 1.0))
            return
        if complete:
            screen_message("Signal Lamp Project completed.")
        else:
            screen_message(f"Contributed {moved} resources to the Signal Lamp Project.")

    def _handle_deployment_gate(self, world):
        self.session.state = "run"
        screen_message("Deploying into Service Halls.")
        self._open_level(world, LEVEL1_MAP)

    def _handle_flicker_proximity(self, world):
        pawn = self.session.player_pawn
        flicker = self._find_label_prefix(world, "FlickerStalker_MainPatrol")
        if pawn is None or flicker is None:
            return
        distance = actor_distance(pawn, flicker)
        if distance <= 700.0:
            self.session.sanity.current = max(self.session.sanity.minimum, self.session.sanity.current - 12.0 / 60.0)
            if distance <= 250.0:
                self.session.sanity.current = max(self.session.sanity.minimum, self.session.sanity.current - 25.0 / 60.0)
        if self.session.sanity.current <= self.session.sanity.low_threshold and not self.session.last_low_sanity_notice:
            self.session.last_low_sanity_notice = True
            screen_message("Sanity is low. Use Almond Water or extract.", unreal.LinearColor(0.95, 0.45, 0.2, 1.0))
        if self.session.sanity.current <= self.session.sanity.minimum:
            self._handle_death(world)
        self._sync_player_debug_state()

    def _handle_death(self, world):
        self.session.inventory.apply_death()
        self.session.state = "personal_room"
        self._sync_player_debug_state()
        screen_message("You died. Carried inventory lost.", unreal.LinearColor(0.95, 0.2, 0.2, 1.0), duration=5.0)
        self._open_level(world, PERSONAL_MAP)

    def _handle_interact(self, world):
        pawn = self.session.player_pawn
        actor = self._current_nearby_actor(world, pawn)
        if actor is None:
            screen_message("Nothing to interact with.", unreal.LinearColor(0.7, 0.7, 0.7, 1.0), duration=1.5)
            return

        label = actor.get_actor_label()
        if "LootContainer" in label:
            self._handle_loot(actor)
        elif "Extraction_" in label:
            self._handle_extract(actor, world)
        elif "PersonalRoomStorage" in label:
            self._handle_personal_storage(world)
        elif "HubProjectBoard" in label:
            self._handle_project_board()
        elif "HubDeploymentGate" in label:
            self._handle_deployment_gate(world)
        elif "FlickerStalker" in label:
            self.session.sanity.current = max(self.session.sanity.minimum, self.session.sanity.current - 10.0)
            self._sync_player_debug_state()
            screen_message("Flicker Stalker lashes your sanity.", unreal.LinearColor(0.95, 0.35, 0.2, 1.0))

    def _handle_menu_deploy(self, world, player_controller):
        import ld_menu_runtime

        if ld_menu_runtime._controller.current_state != "deploy":
            return
        self._hide_menu_boot(world)
        self.session.state = "run"
        self._spawn_or_reuse_player(world, player_controller, "ServiceHallsPlayerStart")
        screen_message("Deployment started. Follow the route: loot -> stalker -> extract.")

    def tick(self, delta_seconds: float):
        subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
        if subsystem is None or not subsystem.is_in_play_in_editor():
            self.reset_for_editor()
            return True

        worlds = unreal.EditorLevelLibrary.get_pie_worlds(False)
        if not worlds:
            return True

        world = worlds[0]
        player_controller = unreal.GameplayStatics.get_player_controller(world, 0)
        if player_controller is None:
            return True

        self.active_world = world

        if map_matches(world, LEVEL1_MAP):
            if self.session.state == "menu":
                import ld_menu_runtime

                if self._pressed_any(player_controller, ld_menu_runtime.KEYS["confirm"]):
                    self._handle_menu_deploy(world, player_controller)
                return True

            self._spawn_or_reuse_player(world, player_controller, "ServiceHallsPlayerStart")
            self.session.sanity.drain_seconds(delta_seconds)
            self._handle_flicker_proximity(world)

            if self._pressed_any(player_controller, KEYS["consume"]):
                self._consume_almond_water()
            if self._pressed_any(player_controller, KEYS["debug_death"]):
                self._handle_death(world)
            if self._pressed_any(player_controller, KEYS["interact"]):
                self._handle_interact(world)
            return True

        if map_matches(world, PERSONAL_MAP):
            self.session.state = "personal_room"
            self._spawn_or_reuse_player(world, player_controller, "PersonalRoomPlayerStart")
            if self._pressed_any(player_controller, KEYS["interact"]):
                self._handle_interact(world)
            return True

        if map_matches(world, HUB_MAP):
            self.session.state = "hub"
            self._spawn_or_reuse_player(world, player_controller, "HubPlayerStart")
            if self._pressed_any(player_controller, KEYS["interact"]):
                self._handle_interact(world)
            return True

        return True


_controller = PlayableLoopRuntimeController()
_callback_handle = None


def register():
    global _callback_handle
    if _callback_handle is None:
        _callback_handle = unreal.register_slate_post_tick_callback(_controller.tick)
        log("Registered PIE playable-loop runtime callback")
