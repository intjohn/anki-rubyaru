# Kana Detection Add-on for Anki

This Anki add-on automatically detects kana annotations in Ruby syntax when adding new notes and extracts the kanji part into a separate field.

## Installation

1. Download the add-on files
2. Place them in your Anki addons folder (usually `~/Documents/Anki2/addons21/kanjionly_filter/`)
3. Restart Anki

## Usage

1. Make sure your note type has a field named `haskana`
2. When adding new notes, the add-on will:
   - Check the first field for Ruby syntax annotations
   - If kana annotations are found, extract the kanji part and non-annotated text
   - Store the result in the `haskana` field

### Examples:

- If your first field contains: `多[た]分[ぶん]`
  - `haskana` field will contain: `多分`
  
- If your first field contains: `たぶん` or `多分` (without Ruby)
  - `haskana` field will be empty

- If your first field contains: `今日[きょう]はたぶんいい天気[てんき]です`
  - `haskana` field will contain: `今日はたぶんいい天気です`

## Note Type Setup

1. Open the Card Types window in Anki
2. Add a field named `haskana` to your note type
3. You can use this field in your card templates to:
   - Show different cards based on whether kana annotations exist
   - Create kanji-only versions of your cards
   - Filter or sort your cards based on annotation presence 