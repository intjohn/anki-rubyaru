import re

import anki

from . import config
from .constant import RUBY_ARU_VALUE

# Exactly the same regex as Anki's furigana field filter
ANKI_FURIGANA_RE = r" ?([^ >]+?)\[(.+?)\]"


def detect_anki_ruby_annotation(text: str) -> bool:
    """
    Returns True if Anki's ruby annotation syntax is present in `text`, otherwise returns False.
    """
    return re.search(ANKI_FURIGANA_RE, text) is not None


def update_note(note: anki.notes.Note) -> bool:
    """
    Updates the destination field of the given note.
    Returns True if the destination field was updated, otherwise returns False.
    """
    source_fields = config.get_config().source_fields
    destination_field = config.get_config().destination_field

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
