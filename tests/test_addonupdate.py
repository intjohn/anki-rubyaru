from typing import Generator
from unittest.mock import MagicMock, patch

import anki
import pytest
from anki.collection import Collection
from anki.notes import Note

from rubyaru import addonupdate


@pytest.fixture
def mock_collection() -> Collection:
    """Mock Anki collection."""
    collection = MagicMock(spec=Collection)
    return collection


@pytest.fixture
def mock_note() -> Note:
    """Create a mock note for testing."""
    note = MagicMock(spec=Note)
    return note


@pytest.fixture
def mock_update_note() -> Generator[MagicMock, None, None]:
    """Mock the update_note function."""
    with patch('rubyaru.addonupdate.update_note') as mock_update:
        yield mock_update


def test_on_note_will_add(
    mock_collection: Collection, mock_note: Note, mock_update_note: MagicMock
) -> None:
    """Test note will add event handler."""
    # Setup
    deck_id = 1

    # Test
    addonupdate.on_note_will_add(mock_collection, mock_note, deck_id)

    # Verify
    mock_update_note.assert_called_once_with(mock_note)


def test_hook_addon_update() -> None:
    """Test hook registration for note addition."""
    # Setup
    original_hooks = list(anki.hooks.note_will_be_added._hooks)

    # Test
    addonupdate.hook_addon_update()

    # Verify
    new_hooks = list(anki.hooks.note_will_be_added._hooks)
    assert len(new_hooks) == len(original_hooks) + 1
    assert addonupdate.on_note_will_add in new_hooks

    # Cleanup
    anki.hooks.note_will_be_added.remove(addonupdate.on_note_will_add)
