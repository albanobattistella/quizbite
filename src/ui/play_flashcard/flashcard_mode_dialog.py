"""Flashcard start-page builder."""

from __future__ import annotations

from collections.abc import Callable
from gettext import gettext as _

from gi.repository import Adw, Gtk

from .flashcard_quiz_builder import SIDE_DEFINITION, SIDE_TERM


def build_flashcard_mode_page(
    *,
    deck_data: dict,
    on_start_quiz: Callable[[str], None],
    on_start_match: Callable[[str], None],
) -> Adw.NavigationPage:
    """Build a dedicated navigation page for starting flashcard study."""
    selected_direction = SIDE_TERM
    term_to_definition_label = _("Term to Definition")
    definition_to_term_label = _("Definition to Term")

    direction_button = Gtk.MenuButton()
    direction_button.add_css_class("flat")
    direction_button.add_css_class("pill")
    direction_button.set_label(term_to_definition_label)
    direction_button.set_direction(Gtk.ArrowType.DOWN)
    direction_button.set_valign(Gtk.Align.CENTER)

    direction_popover = Gtk.Popover()
    direction_popover.add_css_class("menu")
    direction_menu_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    direction_popover.set_child(direction_menu_box)
    direction_button.set_popover(direction_popover)

    def selected_prompt_side() -> str:
        return selected_direction

    def set_direction(side: str) -> None:
        nonlocal selected_direction
        selected_direction = side
        direction_button.set_label(
            term_to_definition_label
            if side == SIDE_TERM
            else definition_to_term_label
        )
        direction_popover.popdown()

    toolbar_view = Adw.ToolbarView()
    toolbar_view.add_top_bar(Adw.HeaderBar())

    content_box = Gtk.Box(
        orientation=Gtk.Orientation.VERTICAL,
        spacing=18,
        margin_top=24,
        margin_bottom=24,
        margin_start=24,
        margin_end=24,
    )
    content_box.set_halign(Gtk.Align.FILL)
    content_box.set_hexpand(True)

    title_label = Gtk.Label(label=deck_data["title"], wrap=True, xalign=0)
    title_label.add_css_class("title-2")
    title_label.set_halign(Gtk.Align.FILL)
    title_label.set_hexpand(True)
    title_label.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
    content_box.append(title_label)

    count_label = Gtk.Label(
        label=_("{count} flashcards").format(count=len(deck_data["cards"])),
        xalign=0,
    )
    count_label.add_css_class("caption-heading")
    count_label.set_halign(Gtk.Align.FILL)
    count_label.set_hexpand(True)
    content_box.append(count_label)

    direction_row = Adw.ActionRow(
        title=_("Direction"),
        subtitle=_("Choose which side appears first during study."),
    )
    direction_row.set_title_lines(2)
    direction_row.set_subtitle_lines(2)
    direction_row.add_suffix(direction_button)
    direction_row.set_activatable_widget(direction_button)
    content_box.append(direction_row)

    direction_menu_box.append(
        _build_direction_option_button(
            term_to_definition_label,
            lambda _button: set_direction(SIDE_TERM),
        )
    )
    direction_menu_box.append(
        _build_direction_option_button(
            definition_to_term_label,
            lambda _button: set_direction(SIDE_DEFINITION),
        )
    )

    actions_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
    actions_box.set_halign(Gtk.Align.FILL)
    actions_box.set_hexpand(True)

    quiz_button = Gtk.Button(label=_("Quiz Mode"))
    quiz_button.add_css_class("suggested-action")
    quiz_button.add_css_class("pill")
    quiz_button.set_halign(Gtk.Align.FILL)
    quiz_button.set_hexpand(True)
    quiz_button.set_sensitive(len(deck_data["cards"]) >= 2)
    quiz_button.connect("clicked", lambda _button: on_start_quiz(selected_prompt_side()))
    actions_box.append(quiz_button)

    if len(deck_data["cards"]) < 2:
        helper_label = Gtk.Label(
            label=_("Quiz mode needs at least two flashcards."),
            wrap=True,
            xalign=0,
        )
        helper_label.add_css_class("caption")
        helper_label.set_halign(Gtk.Align.FILL)
        helper_label.set_hexpand(True)
        helper_label.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        actions_box.append(helper_label)

    match_button = Gtk.Button(label=_("Match Mode"))
    match_button.add_css_class("pill")
    match_button.set_halign(Gtk.Align.FILL)
    match_button.set_hexpand(True)
    match_button.connect(
        "clicked",
        lambda _button: on_start_match(selected_prompt_side()),
    )
    actions_box.append(match_button)

    content_box.append(actions_box)

    clamp = Adw.Clamp(maximum_size=720, tightening_threshold=480)
    clamp.set_halign(Gtk.Align.FILL)
    clamp.set_hexpand(True)
    clamp.set_child(content_box)

    scrolled_window = Gtk.ScrolledWindow()
    scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
    scrolled_window.set_halign(Gtk.Align.FILL)
    scrolled_window.set_hexpand(True)
    scrolled_window.set_vexpand(True)
    scrolled_window.set_child(clamp)

    toolbar_view.set_content(scrolled_window)
    return Adw.NavigationPage.new(
        toolbar_view,
        _("{title} (Flashcards)").format(title=deck_data["title"]),
    )


def _build_direction_option_button(
    label: str,
    callback: Callable,
) -> Gtk.Button:
    """Build one direction option inside the popover menu."""
    button = Gtk.Button(label=label)
    button.set_halign(Gtk.Align.FILL)
    button.set_hexpand(True)
    button.set_has_frame(False)
    button.add_css_class("menuitem")
    button.connect("clicked", callback)
    return button
