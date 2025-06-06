from aqt import mw, gui_hooks
from anki.notes import Note
import re

# Exactly the same regex as Anki's furigana field filter
ANKI_FURIGANA_RE = r" ?([^ >]+?)\[(.+?)\]"

# The value to set the destination field to when the source field is ruby annotated
RUBY_ARU_VALUE = "yes"

# Get the configuration
config = mw.addonManager.getConfig(__name__)

# source fields should be either a string of comma separated field names, or a list of field names
source_fields = config['source_fields']

if isinstance(source_fields, str):
    source_fields = source_fields.split(',')
elif isinstance(source_fields, list):
    source_fields = filter(lambda x: isinstance(x, str), source_fields)
else:
    source_fields = []

# destination field should be a string
destination_field = config['destination_field']

if not isinstance(destination_field, str):
    destination_field = None

def detect_anki_ruby_annotation(text: str) -> bool:
    '''
    Returns True if Anki's ruby annotation syntax is present in `text`, otherwise returns False.
    '''
    return re.search(ANKI_FURIGANA_RE, text) is not None

def handle_unfocus(note: Note, field_idx: int) -> bool:
    '''
    Handles the unfocus event for the given note and field index.
    Returns True if the destination field was updated, otherwise returns False.
    '''

    if not destination_field or destination_field not in note:
        # destination field is not configured or not in the note, do nothing
        return False
    
    if len(source_fields) == 0:
        # source fields are not configured, do nothing
        return False

    source_content = None

    if note.keys()[field_idx] in source_fields:
        source_content = note.fields[field_idx]
        
    if source_content is None:
        # It's not a source field being unfocused, do nothing
        return False
    
    if not source_content:
        # source field is empty
        if not note[destination_field]:
            # destination field is also empty, do nothing
            return False
        
        # destination field is not empty, clear it
        note[destination_field] = ""
        return True
    
    if detect_anki_ruby_annotation(source_content):
        # Ruby annotation is present, set the destination field to RUBY_ARU_VALUE
        if note[destination_field] == RUBY_ARU_VALUE:
            # destination field is already set, do nothing
            return False
        
        note[destination_field] = RUBY_ARU_VALUE
        return True
    
    if note[destination_field]:
        # Ruby annotation is not present but destination field is not empty, clear it
        note[destination_field] = ""
        return True

    return False

def on_field_unfocus(flag: bool, note: Note, current_field_idx: int) -> bool:
    '''
    Handles the unfocus event for the given note and field index.
    Returns True if the destination field was updated, otherwise returns the original flag.
    '''
    return True if handle_unfocus(note, current_field_idx) else flag

# Register the hook
gui_hooks.editor_did_unfocus_field.append(on_field_unfocus)
