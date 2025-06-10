import anki
from anki.collection import Collection
from anki.notes import Note

from .updatenote import update_note


def on_note_will_add(_col: Collection, note: Note, _deck_id: int) -> None:
    """
    Handles the note will add event.
    """
    update_note(note)

def hook_addon_update() -> None:
    """
    Register hanlder for note will add event
    """
    anki.hooks.note_will_be_added.append(on_note_will_add)
