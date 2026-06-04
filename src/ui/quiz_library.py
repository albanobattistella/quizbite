"""Widgets for the study library list."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from gettext import gettext as _, ngettext

from gi.repository import Adw, Gtk


MOBILE_ROW_WIDTH = 480


class LibraryActionRow(Adw.ActionRow):
    """Action row that adapts its trailing controls for narrow screens."""

    __gtype_name__ = "QuizbiteLibraryActionRow"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._actions_box: Gtk.Box | None = None
        self._actions_are_stacked = False

    def set_actions_box(self, actions_box: Gtk.Box) -> None:
        """Track the action controls that should stack on mobile widths."""
        self._actions_box = actions_box

    def do_size_allocate(self, width: int, height: int, baseline: int) -> None:
        """Update the row action layout when GTK allocates a new width."""
        self._update_action_layout(width)
        super().do_size_allocate(width, height, baseline)

    def _update_action_layout(self, width: int) -> None:
        if self._actions_box is None or width <= 0:
            return

        should_stack = width <= MOBILE_ROW_WIDTH
        if should_stack == self._actions_are_stacked:
            return

        self._actions_are_stacked = should_stack
        self._actions_box.set_orientation(
            Gtk.Orientation.VERTICAL
            if should_stack
            else Gtk.Orientation.HORIZONTAL
        )
        self._actions_box.set_spacing(2 if should_stack else 4)
        self.queue_resize()


def build_library_row(
    item: dict,
    on_activate: Callable,
    menu_actions: Sequence[dict],
) -> Adw.ActionRow:
    """Build one row for the mixed library list."""
    row = LibraryActionRow(
        title=item["title"],
        subtitle=format_library_item_subtitle(item),
    )
    row.set_title_lines(2)
    row.set_subtitle_lines(2)
    row.set_activatable(True)
    actions_box = build_row_actions(row, item, on_activate, menu_actions)
    row.set_actions_box(actions_box)
    row.add_suffix(actions_box)
    row.connect("activated", on_activate, item)
    return row


def build_row_actions(
    row: Adw.ActionRow,
    item: dict,
    on_activate: Callable,
    menu_actions: Sequence[dict],
) -> Gtk.Box:
    """Build the trailing row buttons, stacked later on narrow screens."""
    actions_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
    actions_box.set_valign(Gtk.Align.CENTER)

    actions_box.append(build_item_menu_button(menu_actions))
    actions_box.append(build_open_item_button(row, item, on_activate))
    return actions_box


def build_open_item_button(
    row: Adw.ActionRow,
    item: dict,
    on_activate: Callable,
) -> Gtk.Button:
    """Build the explicit open button shown at the end of a library row."""
    button = Gtk.Button(icon_name="go-next-symbolic")
    button.set_valign(Gtk.Align.CENTER)
    button.add_css_class("flat")
    button.set_tooltip_text(_("Open study set"))
    button.connect("clicked", activate_library_row, row, item, on_activate)
    return button


def activate_library_row(
    _button: Gtk.Button,
    row: Adw.ActionRow,
    item: dict,
    on_activate: Callable,
) -> None:
    """Route the explicit open button through the row activation callback."""
    on_activate(row, item)


def build_item_menu_button(
    menu_actions: Sequence[dict],
) -> Gtk.MenuButton:
    """Build the "more" menu button for a library row."""
    menu_button = Gtk.MenuButton(icon_name="view-more-symbolic")
    menu_button.set_valign(Gtk.Align.CENTER)
    menu_button.add_css_class("flat")
    menu_button.set_tooltip_text(_("Item actions"))

    popover = Gtk.Popover()
    popover.add_css_class("menu")

    menu_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    for action in menu_actions:
        menu_box.append(
            build_menu_item_button(
                action["label"],
                action["callback"],
                action["item"],
                popover,
                icon_name=action.get("icon_name"),
                destructive=action.get("destructive", False),
            )
        )

    popover.set_child(menu_box)
    menu_button.set_popover(popover)
    return menu_button


def build_menu_item_button(
    label: str,
    callback: Callable,
    *args,
    icon_name: str | None = None,
    destructive: bool = False,
) -> Gtk.Button:
    """Build a menu-like button for a popover list."""
    button = Gtk.Button()
    button.set_halign(Gtk.Align.FILL)
    button.set_hexpand(True)
    button.set_has_frame(False)
    button.add_css_class("menuitem")

    button.set_child(build_menu_item_content(label, icon_name))

    if destructive:
        button.add_css_class("destructive-action")

    button.connect("clicked", callback, *args)
    return button


def build_menu_item_content(label: str, icon_name: str | None) -> Gtk.Box:
    """Build the visible icon and label content for a popover item."""
    content = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
    content.set_halign(Gtk.Align.FILL)
    content.set_hexpand(True)

    if icon_name is not None:
        content.append(Gtk.Image(icon_name=icon_name))

    item_label = Gtk.Label(label=label)
    item_label.set_hexpand(True)
    item_label.set_max_width_chars(28)
    item_label.set_wrap(True)
    item_label.set_xalign(0)
    content.append(item_label)
    return content


def format_library_item_subtitle(item: dict) -> str:
    """Format the mixed-library count/type subtitle."""
    entry_count = item["entry_count"]
    if item["item_type"] == "flashcard":
        count_label = ngettext(
            "{count} flashcard",
            "{count} flashcards",
            entry_count,
        ).format(count=entry_count)
        type_label = _("Flashcard")
    else:
        count_label = ngettext(
            "{count} question",
            "{count} questions",
            entry_count,
        ).format(count=entry_count)
        type_label = _("Quiz")

    return _("{count} • {type}").format(count=count_label, type=type_label)


def library_item_matches_query(item: dict, query: str) -> bool:
    """Return whether a library item should be visible for a search query."""
    terms = query.casefold().split()
    if not terms:
        return True

    search_text = _build_library_item_search_text(item).casefold()
    return all(term in search_text for term in terms)


def _build_library_item_search_text(item: dict) -> str:
    """Build the normalized text used for library search matching."""
    return " ".join(
        (
            item["title"],
            item["item_type"],
            format_library_item_subtitle(item),
        )
    )
