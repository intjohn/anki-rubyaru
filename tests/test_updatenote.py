from typing import Generator
from unittest.mock import MagicMock, patch

import anki
import pytest

from rubyaru import updatenote


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
    note.__contains__ = MagicMock(return_value=True)
    note.__getitem__ = MagicMock()
    note.__setitem__ = MagicMock()
    note.__getitem__.side_effect = lambda x: {
        "Reading": "漢字[かんじ]",
        "Expression": "漢字[かんじ]を勉強[べんきょう]する",
        "rubyaru": ""
    }[x]
    return note


def test_detect_anki_ruby_annotation_with_ruby() -> None:
    """Test ruby detection with ruby annotation present."""
    text = "漢字[かんじ]を勉強[べんきょう]する"
    assert updatenote.detect_anki_ruby_annotation(text) is True


def test_detect_anki_ruby_annotation_without_ruby() -> None:
    """Test ruby detection with no ruby annotation."""
    text = "漢字を勉強する"
    assert updatenote.detect_anki_ruby_annotation(text) is False


def test_detect_anki_ruby_annotation_with_empty_string() -> None:
    """Test ruby detection with empty string."""
    text = ""
    assert updatenote.detect_anki_ruby_annotation(text) is False


def test_update_note_with_ruby(mock_note: MagicMock, mock_config: MagicMock) -> None:
    """Test note update with ruby annotation present."""
    # Test
    result = updatenote.update_note(mock_note)

    # Verify results
    assert result is True
    mock_note.__setitem__.assert_called_once_with("rubyaru", "yes")


def test_update_note_without_ruby(mock_note: MagicMock, mock_config: MagicMock) -> None:
    """Test note update with no ruby annotation."""
    # Setup
    mock_note.__getitem__.side_effect = lambda x: {
        "Reading": "漢字",
        "Expression": "漢字を勉強する",
        "rubyaru": "yes"
    }[x]

    # Test
    result = updatenote.update_note(mock_note)

    # Verify
    assert result is True
    mock_note.__setitem__.assert_called_once_with("rubyaru", "")


def test_update_note_without_required_fields(mock_note: MagicMock, mock_config: MagicMock) -> None:
    """Test that note is not updated when required fields are missing."""
    # Setup mock note without rubyaru field
    mock_note.__contains__.side_effect = lambda x: x != "rubyaru"

    # Test
    result = updatenote.update_note(mock_note)

    # Verify
    assert result is False
    mock_note.__setitem__.assert_not_called()


def test_update_note_with_no_change_needed(mock_note: MagicMock, mock_config: MagicMock) -> None:
    """Test note update when no change is needed."""
    # Setup
    mock_note.__getitem__.side_effect = lambda x: {
        "Reading": "漢字[かんじ]",
        "Expression": "漢字[かんじ]を勉強[べんきょう]する",
        "rubyaru": "yes"
    }[x]

    # Test
    result = updatenote.update_note(mock_note)

    # Verify
    assert result is False
    mock_note.__setitem__.assert_not_called()
