#!/usr/bin/env python3
import unreal


UI_PATH = "/Game/UI"
WIDGET_NAME = "WBP_MainPlayerMenu"
WIDGET_PATH = f"{UI_PATH}/{WIDGET_NAME}"

WHITE_TEXTURE = unreal.EditorAssetLibrary.load_asset("/Engine/EngineResources/WhiteSquareTexture")

SCREEN_SIZE = unreal.Vector2D(1920.0, 1080.0)
PANEL_FRAME = unreal.LinearColor(0.47, 0.51, 0.33, 0.70)
PANEL_FILL = unreal.LinearColor(0.03, 0.05, 0.04, 0.92)
PANEL_FILL_LIGHT = unreal.LinearColor(0.07, 0.09, 0.07, 0.82)
TEXT_MAIN = unreal.LinearColor(0.86, 0.87, 0.78, 1.00)
TEXT_MUTED = unreal.LinearColor(0.58, 0.64, 0.47, 1.00)
TEXT_ACCENT = unreal.LinearColor(0.92, 0.72, 0.25, 1.00)
TEXT_DARK = unreal.LinearColor(0.12, 0.09, 0.04, 1.00)
FULL_ANCHOR = unreal.Anchors(0.0, 0.0, 1.0, 1.0)
TOP_LEFT_ANCHOR = unreal.Anchors(0.0, 0.0, 0.0, 0.0)


def log(message: str) -> None:
    unreal.log(f"[LD Main Menu Visual] {message}")


def make_text(value: str):
    return unreal.Text(value)


def make_font(size: int):
    return unreal.SlateFontInfo(size=size)


def make_margin(left: float, top: float, right: float, bottom: float):
    return unreal.Margin(left=left, top=top, right=right, bottom=bottom)


def recreate_widget():
    if unreal.EditorAssetLibrary.does_asset_exist(WIDGET_PATH):
        unreal.EditorAssetLibrary.delete_asset(WIDGET_PATH)
        log(f"Deleted existing {WIDGET_PATH}")

    factory = unreal.WidgetBlueprintFactory()
    factory.set_editor_property("parent_class", unreal.UserWidget)
    widget = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        WIDGET_NAME,
        UI_PATH,
        unreal.WidgetBlueprint,
        factory,
    )
    if widget is None:
        raise RuntimeError(f"Failed to create {WIDGET_PATH}")
    log(f"Created {WIDGET_PATH}")
    return widget


def add_widget(widget_blueprint, widget_class, name: str, parent_name: str = ""):
    widget = unreal.EditorUtilityLibrary.add_source_widget(widget_blueprint, widget_class, name, parent_name)
    if widget is None:
        raise RuntimeError(f"Failed to add widget {name} under {parent_name or '<root>'}")
    return widget


def canvas_slot(widget, position: tuple[float, float], size: tuple[float, float], z_order: int = 0):
    slot = widget.slot
    slot.set_anchors(TOP_LEFT_ANCHOR)
    slot.set_position(unreal.Vector2D(position[0], position[1]))
    slot.set_size(unreal.Vector2D(size[0], size[1]))
    slot.set_z_order(z_order)
    return slot


def fullscreen_canvas_slot(widget, z_order: int = 0):
    slot = widget.slot
    slot.set_anchors(FULL_ANCHOR)
    slot.set_offsets(make_margin(0.0, 0.0, 0.0, 0.0))
    slot.set_z_order(z_order)
    return slot


def overlay_slot(widget, padding: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0), h_align=None, v_align=None):
    slot = widget.slot
    slot.set_padding(make_margin(*padding))
    if h_align is not None:
        slot.set_horizontal_alignment(h_align)
    if v_align is not None:
        slot.set_vertical_alignment(v_align)
    return slot


def vbox_slot(widget, padding: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0), fill: bool = False):
    slot = widget.slot
    slot.set_padding(make_margin(*padding))
    size_rule = unreal.SlateChildSize(size_rule=unreal.SlateSizeRule.FILL if fill else unreal.SlateSizeRule.AUTOMATIC, value=1.0)
    slot.set_size(size_rule)
    return slot


def hbox_slot(widget, padding: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0), fill: bool = False):
    slot = widget.slot
    slot.set_padding(make_margin(*padding))
    size_rule = unreal.SlateChildSize(size_rule=unreal.SlateSizeRule.FILL if fill else unreal.SlateSizeRule.AUTOMATIC, value=1.0)
    slot.set_size(size_rule)
    return slot


def style_image(image, color: unreal.LinearColor, opacity: float = 1.0):
    image.set_brush_from_texture(WHITE_TEXTURE, True)
    image.set_color_and_opacity(color)
    image.set_render_opacity(opacity)


def style_text(text, value: str, size: int, color: unreal.LinearColor, opacity: float = 1.0):
    text.set_text(make_text(value))
    text.set_font(make_font(size))
    text.set_color_and_opacity(color)
    text.set_render_opacity(opacity)


def panel_overlay(widget_blueprint, root_name: str, name: str, position: tuple[float, float], size: tuple[float, float]):
    overlay = add_widget(widget_blueprint, unreal.Overlay, name, root_name)
    canvas_slot(overlay, position, size, z_order=5)

    frame = add_widget(widget_blueprint, unreal.Image, f"{name}_Frame", name)
    overlay_slot(frame)
    style_image(frame, PANEL_FRAME)

    fill = add_widget(widget_blueprint, unreal.Image, f"{name}_Fill", name)
    overlay_slot(fill, (2.0, 2.0, 2.0, 2.0))
    style_image(fill, PANEL_FILL)

    content = add_widget(widget_blueprint, unreal.Overlay, f"{name}_Content", name)
    overlay_slot(content, (14.0, 14.0, 14.0, 14.0))
    return content


def nav_button(widget_blueprint, parent_name: str, name: str, label: str, highlighted: bool = False):
    button_overlay = add_widget(widget_blueprint, unreal.Overlay, name, parent_name)
    vbox_slot(button_overlay, (0.0, 0.0, 0.0, 12.0))

    frame = add_widget(widget_blueprint, unreal.Image, f"{name}_Frame", name)
    overlay_slot(frame)
    style_image(frame, PANEL_FRAME if not highlighted else TEXT_ACCENT)

    fill = add_widget(widget_blueprint, unreal.Image, f"{name}_Fill", name)
    overlay_slot(fill, (2.0, 2.0, 2.0, 2.0))
    style_image(fill, PANEL_FILL_LIGHT if not highlighted else unreal.LinearColor(0.25, 0.18, 0.06, 0.95))

    row = add_widget(widget_blueprint, unreal.HorizontalBox, f"{name}_Row", name)
    overlay_slot(row, (18.0, 16.0, 18.0, 16.0), unreal.HorizontalAlignment.FILL, unreal.VerticalAlignment.FILL)

    prefix = add_widget(widget_blueprint, unreal.TextBlock, f"{name}_Prefix", f"{name}_Row")
    hbox_slot(prefix, (0.0, 0.0, 14.0, 0.0))
    style_text(prefix, ">>" if highlighted else "[]", 18, TEXT_ACCENT if highlighted else TEXT_MUTED)

    body = add_widget(widget_blueprint, unreal.TextBlock, f"{name}_Body", f"{name}_Row")
    hbox_slot(body, (0.0, 0.0, 0.0, 0.0), fill=True)
    style_text(body, label.upper(), 24, TEXT_ACCENT if highlighted else TEXT_MAIN)


def stat_card(widget_blueprint, parent_name: str, name: str, heading: str, body_lines: list[str]):
    card = add_widget(widget_blueprint, unreal.Overlay, name, parent_name)
    vbox_slot(card, (0.0, 0.0, 0.0, 12.0))

    frame = add_widget(widget_blueprint, unreal.Image, f"{name}_Frame", name)
    overlay_slot(frame)
    style_image(frame, PANEL_FRAME)

    fill = add_widget(widget_blueprint, unreal.Image, f"{name}_Fill", name)
    overlay_slot(fill, (2.0, 2.0, 2.0, 2.0))
    style_image(fill, PANEL_FILL_LIGHT)

    content = add_widget(widget_blueprint, unreal.VerticalBox, f"{name}_Content", name)
    overlay_slot(content, (16.0, 14.0, 16.0, 14.0))

    title = add_widget(widget_blueprint, unreal.TextBlock, f"{name}_Heading", f"{name}_Content")
    vbox_slot(title, (0.0, 0.0, 0.0, 8.0))
    style_text(title, heading.upper(), 15, TEXT_MUTED)

    for index, line in enumerate(body_lines):
        body = add_widget(widget_blueprint, unreal.TextBlock, f"{name}_Body_{index}", f"{name}_Content")
        vbox_slot(body, (0.0, 0.0, 0.0, 4.0))
        style_text(body, line, 19 if index == 0 else 15, TEXT_MAIN if index == 0 else TEXT_MUTED)


def build_main_menu_layout():
    widget = recreate_widget()
    root = add_widget(widget, unreal.CanvasPanel, "RootCanvas", "")

    top_left = panel_overlay(widget, "RootCanvas", "TopLeftPanel", (28.0, 20.0), (370.0, 118.0))
    top_left_box = add_widget(widget, unreal.VerticalBox, "TopLeftBox", "TopLeftPanel_Content")
    overlay_slot(top_left_box)
    for name, text, color in (
        ("NetworkHeader", "REER-LIMINAL OPS NETWORK", TEXT_MUTED),
        ("ConnectionText", "CONNECTION: LOCAL", TEXT_MAIN),
        ("ZoneAccessText", "ZONE ACCESS: RESTRICTED", TEXT_ACCENT),
        ("SignalText", "SIGNAL STABILITY: DEGRADED", TEXT_MUTED),
    ):
        item = add_widget(widget, unreal.TextBlock, name, "TopLeftBox")
        vbox_slot(item, (0.0, 0.0, 0.0, 6.0))
        style_text(item, text, 16, color)

    header = panel_overlay(widget, "RootCanvas", "HeaderPanel", (430.0, 20.0), (1040.0, 118.0))
    header_box = add_widget(widget, unreal.VerticalBox, "HeaderBox", "HeaderPanel_Content")
    overlay_slot(header_box)
    title = add_widget(widget, unreal.TextBlock, "HeaderTitle", "HeaderBox")
    vbox_slot(title, (0.0, 0.0, 0.0, 4.0))
    style_text(title, "L I M I N A L", 56, TEXT_MAIN)
    subtitle = add_widget(widget, unreal.TextBlock, "HeaderSubtitle", "HeaderBox")
    vbox_slot(subtitle)
    style_text(subtitle, "OPERATIONS.HUB", 22, TEXT_MUTED)

    top_right = panel_overlay(widget, "RootCanvas", "TopRightPanel", (1494.0, 20.0), (350.0, 118.0))
    top_right_box = add_widget(widget, unreal.VerticalBox, "TopRightBox", "TopRightPanel_Content")
    overlay_slot(top_right_box)
    for name, text in (
        ("NavEnabled", "KB/CTRL NAV ENABLED"),
        ("SfxHover", "SFX_HOVER"),
        ("SfxClick", "SFX_CLICK"),
    ):
        item = add_widget(widget, unreal.TextBlock, name, "TopRightBox")
        vbox_slot(item, (0.0, 0.0, 0.0, 10.0))
        style_text(item, text, 16, TEXT_MUTED if name == "NavEnabled" else TEXT_MAIN)

    left = panel_overlay(widget, "RootCanvas", "LeftRailPanel", (20.0, 160.0), (410.0, 790.0))
    left_box = add_widget(widget, unreal.VerticalBox, "LeftRailBox", "LeftRailPanel_Content")
    overlay_slot(left_box)
    left_title = add_widget(widget, unreal.TextBlock, "LeftRailTitle", "LeftRailBox")
    vbox_slot(left_title, (0.0, 0.0, 0.0, 18.0))
    style_text(left_title, "// MAIN MENU", 18, TEXT_MUTED)
    nav_button(widget, "LeftRailBox", "NavDeploy", "Deploy", highlighted=True)
    nav_button(widget, "LeftRailBox", "NavLoadout", "Loadout")
    nav_button(widget, "LeftRailBox", "NavOperators", "Operators")
    nav_button(widget, "LeftRailBox", "NavMarket", "Market")
    nav_button(widget, "LeftRailBox", "NavIntel", "Intel")
    nav_button(widget, "LeftRailBox", "NavSettings", "Settings")
    nav_button(widget, "LeftRailBox", "NavExit", "Exit")
    left_footer = add_widget(widget, unreal.TextBlock, "LeftRailFooter", "LeftRailBox")
    vbox_slot(left_footer, (0.0, 16.0, 0.0, 0.0))
    style_text(left_footer, "NAVIGATION SUPPORT: ON", 18, TEXT_MUTED)

    center = panel_overlay(widget, "RootCanvas", "CenterPanel", (450.0, 160.0), (980.0, 790.0))
    center_canvas = add_widget(widget, unreal.CanvasPanel, "CenterCanvas", "CenterPanel_Content")
    overlay_slot(center_canvas)

    center_frame = add_widget(widget, unreal.Image, "CenterPreviewFrame", "CenterCanvas")
    canvas_slot(center_frame, (0.0, 0.0), (952.0, 525.0), z_order=0)
    style_image(center_frame, unreal.LinearColor(0.38, 0.42, 0.27, 0.35))

    center_fill = add_widget(widget, unreal.Image, "CenterPreviewFill", "CenterCanvas")
    canvas_slot(center_fill, (2.0, 2.0), (948.0, 521.0), z_order=0)
    style_image(center_fill, unreal.LinearColor(0.02, 0.05, 0.04, 0.10))

    center_title = add_widget(widget, unreal.TextBlock, "CenterOperationTitle", "CenterCanvas")
    canvas_slot(center_title, (24.0, 24.0), (620.0, 52.0), z_order=2)
    style_text(center_title, "OPERATION: SERVICE HALLS", 34, TEXT_MAIN)

    zone_tag_overlay = add_widget(widget, unreal.Overlay, "ZoneTagOverlay", "CenterCanvas")
    canvas_slot(zone_tag_overlay, (760.0, 24.0), (168.0, 44.0), z_order=2)
    zone_tag_frame = add_widget(widget, unreal.Image, "ZoneTagFrame", "ZoneTagOverlay")
    overlay_slot(zone_tag_frame)
    style_image(zone_tag_frame, PANEL_FRAME)
    zone_tag_fill = add_widget(widget, unreal.Image, "ZoneTagFill", "ZoneTagOverlay")
    overlay_slot(zone_tag_fill, (2.0, 2.0, 2.0, 2.0))
    style_image(zone_tag_fill, PANEL_FILL)
    zone_tag_text = add_widget(widget, unreal.TextBlock, "ZoneTagText", "ZoneTagOverlay")
    overlay_slot(zone_tag_text, (18.0, 9.0, 18.0, 9.0))
    style_text(zone_tag_text, "ZONE // SH-17", 16, TEXT_MUTED)

    feed_label = add_widget(widget, unreal.TextBlock, "CenterFeedLabel", "CenterCanvas")
    canvas_slot(feed_label, (26.0, 92.0), (360.0, 36.0), z_order=2)
    style_text(feed_label, "LIVE FEED // LEVEL 1 SERVICE HALLS", 18, TEXT_MUTED, opacity=0.85)

    hint_label = add_widget(widget, unreal.TextBlock, "CenterHintLabel", "CenterCanvas")
    canvas_slot(hint_label, (26.0, 124.0), (620.0, 70.0), z_order=2)
    style_text(
        hint_label,
        "The center frame is intended to sit over the in-world Level 1 corridor view.",
        18,
        TEXT_MAIN,
        opacity=0.78,
    )

    metrics_overlay = add_widget(widget, unreal.Overlay, "MetricsOverlay", "CenterCanvas")
    canvas_slot(metrics_overlay, (18.0, 390.0), (916.0, 162.0), z_order=2)
    metrics_frame = add_widget(widget, unreal.Image, "MetricsFrame", "MetricsOverlay")
    overlay_slot(metrics_frame)
    style_image(metrics_frame, PANEL_FRAME)
    metrics_fill = add_widget(widget, unreal.Image, "MetricsFill", "MetricsOverlay")
    overlay_slot(metrics_fill, (2.0, 2.0, 2.0, 2.0))
    style_image(metrics_fill, PANEL_FILL_LIGHT)
    metrics_box = add_widget(widget, unreal.HorizontalBox, "MetricsBox", "MetricsOverlay")
    overlay_slot(metrics_box, (14.0, 14.0, 14.0, 14.0))

    metric_specs = (
        ("Threat Level", "HIGH", "////"),
        ("Extraction Windows", "00:20-00:30", "00:50-01:00 | 01:20-01:30"),
        ("Environmental Anomaly", "DISORIENTATION", "Signal interference"),
        ("Recommended Team Size", "1 - 3", "Field unit"),
        ("Brief Objective", "Investigate service halls", "Recover diagnostics from terminal nodes."),
    )
    for index, (heading, body, subbody) in enumerate(metric_specs):
        card_box = add_widget(widget, unreal.VerticalBox, f"MetricCard_{index}", "MetricsBox")
        hbox_slot(card_box, (10.0, 0.0, 10.0, 0.0), fill=True)
        heading_widget = add_widget(widget, unreal.TextBlock, f"MetricCard_{index}_Heading", f"MetricCard_{index}")
        vbox_slot(heading_widget, (0.0, 0.0, 0.0, 8.0))
        style_text(heading_widget, heading.upper(), 14, TEXT_MUTED)
        body_widget = add_widget(widget, unreal.TextBlock, f"MetricCard_{index}_Body", f"MetricCard_{index}")
        vbox_slot(body_widget, (0.0, 0.0, 0.0, 6.0))
        style_text(body_widget, body.upper(), 18, TEXT_MAIN if index != 0 else TEXT_ACCENT)
        sub_widget = add_widget(widget, unreal.TextBlock, f"MetricCard_{index}_Sub", f"MetricCard_{index}")
        vbox_slot(sub_widget)
        style_text(sub_widget, subbody.upper(), 13, TEXT_MUTED)

    deploy_overlay = add_widget(widget, unreal.Overlay, "DeployButtonOverlay", "CenterCanvas")
    canvas_slot(deploy_overlay, (180.0, 585.0), (460.0, 92.0), z_order=3)
    deploy_frame = add_widget(widget, unreal.Image, "DeployButtonFrame", "DeployButtonOverlay")
    overlay_slot(deploy_frame)
    style_image(deploy_frame, TEXT_ACCENT)
    deploy_fill = add_widget(widget, unreal.Image, "DeployButtonFill", "DeployButtonOverlay")
    overlay_slot(deploy_fill, (2.0, 2.0, 2.0, 2.0))
    style_image(deploy_fill, unreal.LinearColor(0.29, 0.18, 0.05, 0.95))
    deploy_box = add_widget(widget, unreal.VerticalBox, "DeployButtonBox", "DeployButtonOverlay")
    overlay_slot(deploy_box)
    deploy_label = add_widget(widget, unreal.TextBlock, "DeployButtonLabel", "DeployButtonBox")
    vbox_slot(deploy_label, (0.0, 12.0, 0.0, 4.0))
    style_text(deploy_label, "DEPLOY", 38, TEXT_ACCENT)
    deploy_sub = add_widget(widget, unreal.TextBlock, "DeployButtonSub", "DeployButtonBox")
    vbox_slot(deploy_sub)
    style_text(deploy_sub, "ENTER ZONE", 22, TEXT_MAIN)

    right = panel_overlay(widget, "RootCanvas", "RightRailPanel", (1460.0, 160.0), (390.0, 790.0))
    right_box = add_widget(widget, unreal.VerticalBox, "RightRailBox", "RightRailPanel_Content")
    overlay_slot(right_box)
    right_title = add_widget(widget, unreal.TextBlock, "RightRailTitle", "RightRailBox")
    vbox_slot(right_title, (0.0, 0.0, 0.0, 18.0))
    style_text(right_title, "// OPERATOR STATUS", 18, TEXT_MUTED)
    stat_card(widget, "RightRailBox", "OperatorCard", "Operator Name", ["Archive-Delta", "ID: CHAR-OFFICIAL"])
    stat_card(widget, "RightRailBox", "FactionCard", "Faction", ["M.E.G.", "Research / archive / scanner play"])
    stat_card(widget, "RightRailBox", "HealthCard", "Health Condition", ["GOOD", "100% stable"])
    stat_card(widget, "RightRailBox", "ReputationCard", "Reputation", ["Tier I - Field Clearance", "Progress pending"])
    stat_card(widget, "RightRailBox", "CurrencyCard", "Currency / Resources", ["Credits 18,420", "Research 450 | Contracts 12"])
    stat_card(widget, "RightRailBox", "KitCard", "Current Kit Summary", ["Operator Field Kit", "Scanner | flashlight | archive badge"])

    footer = panel_overlay(widget, "RootCanvas", "FooterPanel", (20.0, 965.0), (1830.0, 92.0))
    footer_box = add_widget(widget, unreal.HorizontalBox, "FooterBox", "FooterPanel_Content")
    overlay_slot(footer_box)
    footer_values = (
        "BUILD: V0.1.0",
        "ENV: LOCAL TEST",
        "ALL SYSTEMS NOMINAL... STANDBY",
        "LOCAL TIME",
    )
    for index, text in enumerate(footer_values):
        item = add_widget(widget, unreal.TextBlock, f"FooterText_{index}", "FooterBox")
        hbox_slot(item, (10.0, 10.0, 10.0, 10.0), fill=True)
        style_text(item, text, 18, TEXT_MUTED if index != 2 else TEXT_MAIN)

    unreal.BlueprintEditorLibrary.compile_blueprint(widget)
    unreal.EditorAssetLibrary.save_loaded_asset(widget, only_if_is_dirty=False)
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    log("Main menu visual layout rebuilt")


if __name__ == "__main__":
    build_main_menu_layout()
