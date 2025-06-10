from typing import Generator
from unittest.mock import MagicMock, patch

import anki
import pytest
from aqt import gui_hooks

from rubyaru import editorupdate


@pytest.fixture
def mock_config() -> Generator[MagicMock, None, None]:
    """Mock the config module."""
    with patch('rubyaru.config.get_config') as mock_get_config:
        mock_get_config.return_value.source_fields = ["Reading", "Expression"]
        mock_get_config.return_value.destination_field = "rubyaru"
        yield mock_get_config


@pytest.fixture
def mock_note() -> MagicMock:
    """Create a mock note for testing."""
    note = MagicMock(spec=anki.notes.Note)
    note.keys.return_value = ["Reading", "Expression", "rubyaru"]
    return note


@pytest.fixture
def mock_update_note() -> Generator[MagicMock, None, None]:
    """Mock the update_note function."""
    with patch('rubyaru.updatenote.update_note') as mock_update:
        yield mock_update


def test_on_field_unfocus_source_field_with_update(
    mock_note: MagicMock, mock_config: MagicMock, mock_update_note: MagicMock
) -> None:
    """Test field unfocus when a source field is modified and update succeeds."""
    # Setup
    mock_update_note.return_value = True
    current_field_idx = 0  # Reading field

    # Test
    result = editorupdate.on_field_unfocus(False, mock_note, current_field_idx)

    # Verify
    assert result is True
    mock_update_note.assert_called_once_with(mock_note)


def test_on_field_unfocus_source_field_without_update(
    mock_note: MagicMock, mock_config: MagicMock, mock_update_note: MagicMock
) -> None:
    """Test field unfocus when a source field is modified but update returns False."""
    # Setup
    mock_update_note.return_value = False
    current_field_idx = 0  # Reading field

    # Test
    result = editorupdate.on_field_unfocus(False, mock_note, current_field_idx)

    # Verify
    assert result is False
    mock_update_note.assert_called_once_with(mock_note)


def test_on_field_unfocus_non_source_field(
    mock_note: MagicMock, mock_config: MagicMock, mock_update_note: MagicMock
) -> None:
    """Test field unfocus when a non-source field is modified."""
    # Setup
    current_field_idx = 2  # rubyaru field

    # Test
    result = editorupdate.on_field_unfocus(False, mock_note, current_field_idx)

    # Verify
    assert result is False
    mock_update_note.assert_not_called()


def test_on_field_unfocus_preserves_flag(
    mock_note: MagicMock, mock_config: MagicMock, mock_update_note: MagicMock
) -> None:
    """Test that the original flag is preserved when appropriate."""
    # Setup
    mock_update_note.return_value = False
    current_field_idx = 0  # Reading field

    # Test with True flag
    result = editorupdate.on_field_unfocus(True, mock_note, current_field_idx)

    # Verify
    assert result is True  # Original True flag should be preserved
    mock_update_note.assert_called_once_with(mock_note)


def test_hook_editor_update() -> None:
    """Test hook registration."""
    # Setup
    original_hooks = list(gui_hooks.editor_did_unfocus_field._hooks)

    # Test
    editorupdate.hook_editor_update()

    # Verify
    new_hooks = list(gui_hooks.editor_did_unfocus_field._hooks)
    assert len(new_hooks) == len(original_hooks) + 1
    assert editorupdate.on_field_unfocus in new_hooks

    # Cleanup
    gui_hooks.editor_did_unfocus_field.remove(editorupdate.on_field_unfocus)
