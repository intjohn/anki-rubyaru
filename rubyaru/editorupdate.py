from anki.notes import Note
from aqt import gui_hooks

from .config import config
from .updatenote import update_note

source_fields = config.source_fields


def on_field_unfocus(flag: bool, note: Note, current_field_idx: int) -> bool:
    """
    Handles the unfocus event for the given note and field index.
    Returns True if the destination field was updated, otherwise returns the original flag.
    """
    if note.keys()[current_field_idx] in source_fields:
        return update_note(note) or flag

    return flag

# Register hanlder for editor unfocus event
gui_hooks.editor_did_unfocus_field.append(on_field_unfocus)
