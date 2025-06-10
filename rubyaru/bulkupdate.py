from typing import Sequence

import anki
from anki.collection import Collection, OpChanges
from aqt import gui_hooks, mw
from aqt.browser import Browser
from aqt.operations import CollectionOp
from aqt.qt import QAction, qconnect
from aqt.utils import showInfo

from . import updatenote
from .constant import ADDON_NAME


def update_notes_op(col: Collection, notes: Sequence[anki.notes.Note]) -> OpChanges:
    """
    Update the given notes with undo entry.
    """
    pos = col.add_custom_undo_entry(f"{ADDON_NAME}: Update {len(notes)} notes.")
    changed = []

    for note in notes:
        if updatenote.update_note(note):
            changed.append(note)

    col.update_notes(changed)

    return col.merge_undo_entries(pos)


def bulk_update_notes(noteIds: Sequence[anki.notes.NoteId], parent: Browser) -> None:
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

def hook_bulk_update() -> None:
    """
    Register hanlder for browser menus init event
    """
    gui_hooks.browser_menus_did_init.append(on_browser_menus_init)
