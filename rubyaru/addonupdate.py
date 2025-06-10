from anki import hooks
from anki.collection import Collection
from anki.notes import Note

from .updatenote import update_note


def on_note_will_add(_col: Collection, note: Note, _deck_id: int) -> None:
    """
    Handles the note will add event.
    """
    update_note(note)

# Register hanlder for note will add event
hooks.note_will_be_added.append(on_note_will_add)
