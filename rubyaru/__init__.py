import re
from collections.abc import Sequence

from anki import hooks
from anki.collection import Collection, OpChanges
from anki.notes import Note, NoteId
from aqt import gui_hooks, mw
from aqt.browser import Browser
from aqt.operations import CollectionOp
from aqt.qt import QAction, qconnect
from aqt.utils import showInfo

ADDON_NAME = "Rubyaru"

# Exactly the same regex as Anki's furigana field filter
ANKI_FURIGANA_RE = r" ?([^ >]+?)\[(.+?)\]"

# The value to set the destination field to when the source field is ruby annotated
RUBY_ARU_VALUE = "yes"

# Get the configuration
config = mw.addonManager.getConfig(__name__)

# source fields should be either a string of comma separated field names, or a list of field names
source_fields = config["source_fields"]

if isinstance(source_fields, str):
    source_fields = source_fields.split(",")
elif isinstance(source_fields, list):
    source_fields = filter(lambda x: isinstance(x, str), source_fields)
else:
    source_fields = []

# destination field should be a string
destination_field = config["destination_field"]

if not isinstance(destination_field, str):
    destination_field = None


def detect_anki_ruby_annotation(text: str) -> bool:
    """
    Returns True if Anki's ruby annotation syntax is present in `text`, otherwise returns False.
    """
    return re.search(ANKI_FURIGANA_RE, text) is not None


def update_note(note: Note) -> bool:
    """
    Updates the destination field of the given note.
    Returns True if the destination field was updated, otherwise returns False.
    """

    if not destination_field or destination_field not in note:
        # destination field is not configured or not in the note, do nothing
        return False

    if len(source_fields) == 0:
        # source fields are not configured, do nothing
        return False

    res = False

    for field_name in source_fields:
        if field_name in note and note[field_name]:
            res |= detect_anki_ruby_annotation(note[field_name])

    if res:
        if note[destination_field] != RUBY_ARU_VALUE:
            note[destination_field] = RUBY_ARU_VALUE
            return True

        return False

    if note[destination_field] != "":
        note[destination_field] = ""
        return True

    return False


def on_field_unfocus(flag: bool, note: Note, current_field_idx: int) -> bool:
    """
    Handles the unfocus event for the given note and field index.
    Returns True if the destination field was updated, otherwise returns the original flag.
    """
    if note.keys()[current_field_idx] in source_fields:
        return update_note(note) or flag

    return flag


def on_note_will_add(_col: Collection, note: Note, _deck_id: int) -> None:
    """
    Handles the note will add event.
    """
    update_note(note)


def update_notes_op(col: Collection, notes: Sequence[Note]) -> OpChanges:
    """
    Update the given notes with undo entry.
    """
    pos = col.add_custom_undo_entry(f"{ADDON_NAME}: Update {len(notes)} notes.")
    changed = []

    for note in notes:
        if update_note(note):
            changed.append(note)

    col.update_notes(changed)

    return col.merge_undo_entries(pos)


def bulk_update_notes(noteIds: Sequence[NoteId], parent: Browser) -> None:
    """
    Bulk update in background.
    """
    CollectionOp(
        parent=parent,
        op=lambda col: update_notes_op(col, notes=[mw.col.get_note(noteId) for noteId in noteIds]),
    ).success(
        lambda _out: showInfo(
            text=f"Processed {len(noteIds)} notes.",
            parent=parent,
            title=f"{ADDON_NAME}: Bulk update done",
            textFormat="rich",
        )
    ).run_in_background()


def on_browser_menus_init(browser: Browser) -> None:
    """
    Adds a menu item to bulk update the ruby annotation detection result for selected notes.
    """
    action = QAction(text=f"{ADDON_NAME}: Bulk update", parent=browser)
    qconnect(action.triggered, lambda: bulk_update_notes(browser.selectedNotes(), parent=browser))
    browser.form.menuEdit.addAction(action)


# Register hanlder for editor unfocus event
gui_hooks.editor_did_unfocus_field.append(on_field_unfocus)

# Register hanlder for note will add event
hooks.note_will_be_added.append(on_note_will_add)

# Register hanlder for browser menus init event
gui_hooks.browser_menus_did_init.append(on_browser_menus_init)
