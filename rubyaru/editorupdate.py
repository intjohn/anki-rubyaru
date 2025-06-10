import anki
from aqt import gui_hooks

from . import config, updatenote


def on_field_unfocus(flag: bool, note: anki.notes.Note, current_field_idx: int) -> bool:
    """
    Handles the unfocus event for the given note and field index.
    Returns True if the destination field was updated, otherwise returns the original flag.
    """
    source_fields = config.get_config().source_fields

    if note.keys()[current_field_idx] in source_fields:
        return updatenote.update_note(note) or flag

    return flag

def hook_editor_update() -> None:
    """
    Register hanlder for editor unfocus event
    """
    gui_hooks.editor_did_unfocus_field.append(on_field_unfocus)
