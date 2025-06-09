# Rubyaru - Ruby Annotation Detection for Anki

This Anki add-on automatically detects ruby annotations (furigana) in specified fields and marks their presence in a destination field. This can be useful for filtering cards based on whether they contain ruby annotations.

## Features

- Detects Anki's ruby annotation syntax (e.g., `漢字[かんじ]`)
- Monitors multiple source fields for ruby annotations
- Updates a destination field with "yes" when ruby annotations are found
- Works in real-time while editing
- Includes bulk update functionality in the card browser

## Configuration

The add-on can be configured through Anki's add-on configuration. Here's what you can configure:

```json
{
    "source_fields": ["Reading", "Expression"],
    "destination_field": "hasruby"
}
```

- `source_fields`: Can be either a comma-separated string or a list of field names to monitor
- `destination_field`: The field name where the detection result will be stored

## How it Works

1. When editing a note:
   - The add-on monitors only if the note contains the configured destination field.
   - When you finish editing a field (by tabbing out or clicking elsewhere) listed in the configured source fields, detection is performed.
   - When detection is performed, all the fields included in the configured source fields are scanned to find ruby annotation.
   - If no ruby annotations are found, clears the destination field, otherwise it's filled with value "yes".

2. When adding new notes:
   - The add-on automatically processes a note only if the note contains the configured destination field.
   - Checks for ruby annotations before the note is added
   - Updates the destination field accordingly

3. Bulk updating:
   - In the card browser, select the notes you want to update
   - Go to Edit menu and click "Rubyaru: Bulk update"
   - The add-on will process all selected notes in the background

## Examples

If your source field contains:
- `漢字[かんじ]` → destination field will be set to "yes"
- `漢字` → destination field will be cleared
- `今日[きょう]は晴[は]れです` → destination field will be set to "yes"

## Note Type Setup

1. Make sure your note type has the configured destination field
2. You can use this field to:
   - Filter cards with/without ruby annotations in the browser
   - Create conditional card templates, e.g. Only create cards to test pronounce recognition of words/sentences if they contain Kanji annotated with Kana.
   - Can be combined with use of Japanese Support Add-on and include "Reading" (the default output field of Japanese Support Add-on) in the source fields configuration.

## Installation

1. Download the add-on from AnkiWeb
2. Install it through Anki's add-on manager
3. Restart Anki
4. Configure the source and destination fields in the add-on configuration 
