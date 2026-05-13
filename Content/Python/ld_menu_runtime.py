import unreal


BUTTONS = ["deploy", "loadout", "operators", "market", "intel", "settings", "exit"]
BUTTON_INDEX = {name: idx for idx, name in enumerate(BUTTONS)}
MENU_WIDGET_PATH = "/Game/UI/WBP_MainPlayerMenu"
TEXTURE_PATHS = {
    "deploy": "/Game/UI/T_MenuDeployOverlay",
    "loadout": "/Game/UI/T_MenuLoadoutOverlay",
    "operators": "/Game/UI/T_MenuOperatorsOverlay",
    "market": "/Game/UI/T_MenuMarketOverlay",
    "intel": "/Game/UI/T_MenuIntelOverlay",
    "settings": "/Game/UI/T_MenuSettingsOverlay",
    "exit": "/Game/UI/T_MenuExitOverlay",
}


def log(message: str) -> None:
    unreal.log(f"[LD Menu Runtime] {message}")


def make_key(name: str):
    key = unreal.Key()
    key.set_editor_property("key_name", unreal.SystemLibrary.make_literal_name(name))
    return key


KEYS = {
    "up": [make_key("W"), make_key("Up"), make_key("Gamepad_DPad_Up")],
    "down": [make_key("S"), make_key("Down"), make_key("Gamepad_DPad_Down")],
    "confirm": [make_key("Enter"), make_key("SpaceBar"), make_key("Gamepad_FaceButton_Bottom")],
    "back": [make_key("Escape"), make_key("BackSpace"), make_key("Gamepad_FaceButton_Right")],
}


class MenuRuntimeController:
    def __init__(self):
        self.current_state = "deploy"
        self.active_world = None
        self.dynamic_material = None
        self.menu_plane = None
        self.menu_widget = None
        self.menu_widget_class = None
        self.session_initialized = False
        self.loaded_textures = {}
        self.last_click_down = False

    def reset_session(self):
        if self.menu_widget is not None:
            try:
                self.menu_widget.remove_from_viewport()
            except Exception:
                pass
        self.active_world = None
        self.dynamic_material = None
        self.menu_plane = None
        self.menu_widget = None
        self.session_initialized = False
        self.current_state = "deploy"
        self.last_click_down = False

    def load_texture(self, state: str):
        if state not in self.loaded_textures:
            self.loaded_textures[state] = unreal.EditorAssetLibrary.load_asset(TEXTURE_PATHS[state])
        return self.loaded_textures[state]

    def _find_menu_plane(self, world):
        menu_class = unreal.EditorAssetLibrary.load_blueprint_class("/Game/Blueprints/BP_MainMenuPawn")
        if menu_class is None:
            return None
        actors = unreal.GameplayStatics.get_all_actors_of_class(world, menu_class)
        for actor in actors:
            if actor.get_actor_label() == "MenuBootPawn":
                for component in actor.get_components_by_class(unreal.StaticMeshComponent):
                    if component.get_name() == "MenuPlane":
                        return component
        return None

    def _load_menu_widget_class(self):
        if self.menu_widget_class is None:
            self.menu_widget_class = unreal.EditorAssetLibrary.load_blueprint_class(MENU_WIDGET_PATH)
        return self.menu_widget_class

    def _ensure_viewport_widget(self, player_controller):
        if self.menu_widget is not None:
            try:
                if self.menu_widget.is_in_viewport():
                    return True
            except Exception:
                self.menu_widget = None

        widget_class = self._load_menu_widget_class()
        if widget_class is None:
            return False

        try:
            widget = unreal.new_object(widget_class, outer=player_controller, name="LD_MainMenuViewportWidget")
        except Exception:
            widget = None

        if widget is None:
            return False

        try:
            widget.set_owning_player(player_controller)
        except Exception:
            pass

        try:
            widget.add_to_viewport(1000)
            widget.set_position_in_viewport(unreal.Vector2D(0.0, 0.0), False)
            self.menu_widget = widget
            log("Added WBP_MainPlayerMenu to viewport")
            return True
        except Exception:
            self.menu_widget = None
            return False

    def _ensure_session(self, world, player_controller):
        if self.active_world == world and (
            (self.menu_widget is not None and self.menu_widget.is_in_viewport()) or
            (self.dynamic_material and self.menu_plane)
        ):
            return True

        self.active_world = world
        player_controller.show_mouse_cursor = True
        player_controller.enable_click_events = True
        player_controller.enable_mouse_over_events = True
        player_controller.set_ignore_move_input(True)
        player_controller.set_ignore_look_input(True)

        plane_candidate = self._find_menu_plane(world)
        if plane_candidate is not None:
            plane_candidate.set_hidden_in_game(True)

        if self._ensure_viewport_widget(player_controller):
            self.dynamic_material = None
            self.menu_plane = plane_candidate
            self._apply_state(self.current_state)
            self.session_initialized = True
            log("PIE menu runtime initialized in fullscreen viewport mode")
            return True

        self.menu_plane = plane_candidate
        if self.menu_plane is None:
            return False

        self.menu_plane.set_hidden_in_game(False)
        self.dynamic_material = self.menu_plane.create_dynamic_material_instance(0)
        if self.dynamic_material is None:
            return False

        self._apply_state(self.current_state)
        self.session_initialized = True
        log("PIE menu runtime initialized in world-plane fallback mode")
        return True

    def _apply_state(self, state: str):
        self.current_state = state
        texture = self.load_texture(state)
        if texture is not None and self.dynamic_material is not None:
            self.dynamic_material.set_texture_parameter_value("MenuTexture", texture)

    def _pressed_any(self, player_controller, keys) -> bool:
        return any(player_controller.was_input_key_just_pressed(key) for key in keys)

    def _handle_click(self, player_controller):
        left_mouse = make_key("LeftMouseButton")
        clicked = player_controller.was_input_key_just_pressed(left_mouse)
        if not clicked:
            return None
        mouse = player_controller.get_mouse_position()
        viewport = player_controller.get_viewport_size()
        if not mouse or not viewport:
            return None
        mx, my = mouse
        vw, vh = viewport
        if vw <= 0 or vh <= 0:
            return None

        button_region = (
            int(vw * 0.29),
            int(vw * 0.40),
            int(vh * 0.36),
            int(vh * 0.73),
        )
        min_x, max_x, min_y, max_y = button_region
        if mx < min_x or mx > max_x or my < min_y or my > max_y:
            return None
        button_height = (max_y - min_y) / len(BUTTONS)
        index = int((my - min_y) / button_height)
        index = max(0, min(len(BUTTONS) - 1, index))
        return BUTTONS[index]

    def _confirm_current(self):
        if self.current_state == "exit":
            unreal.EditorLevelLibrary.editor_end_play()

    def tick(self, delta_seconds: float):
        subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
        if subsystem is None or not subsystem.is_in_play_in_editor():
            self.reset_session()
            return True

        worlds = unreal.EditorLevelLibrary.get_pie_worlds(False)
        if not worlds:
            return True
        world = worlds[0]
        player_controller = unreal.GameplayStatics.get_player_controller(world, 0)
        if player_controller is None:
            return True
        if not self._ensure_session(world, player_controller):
            return True

        clicked_state = self._handle_click(player_controller)
        if clicked_state:
            self._apply_state(clicked_state)
            return True

        if self._pressed_any(player_controller, KEYS["up"]):
            next_index = (BUTTON_INDEX[self.current_state] - 1) % len(BUTTONS)
            self._apply_state(BUTTONS[next_index])
            return True

        if self._pressed_any(player_controller, KEYS["down"]):
            next_index = (BUTTON_INDEX[self.current_state] + 1) % len(BUTTONS)
            self._apply_state(BUTTONS[next_index])
            return True

        if self._pressed_any(player_controller, KEYS["confirm"]):
            self._confirm_current()
            return True

        if self._pressed_any(player_controller, KEYS["back"]):
            self._apply_state("deploy")
            return True

        return True


_controller = MenuRuntimeController()
_callback_handle = None


def register():
    global _callback_handle
    if _callback_handle is None:
        _callback_handle = unreal.register_slate_post_tick_callback(_controller.tick)
        log("Registered PIE menu runtime callback")
