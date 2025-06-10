import pytest
from unittest.mock import MagicMock

from rubyaru import detect_anki_ruby_annotation, update_note

from anki.notes import Note


@pytest.fixture
def mock_note():
    """Create a mock note for testing."""
    note = MagicMock(spec=Note)
    note.__contains__ = MagicMock()
    note.__getitem__ = MagicMock()
    note.__setitem__ = MagicMock()
    note.keys = MagicMock(return_value=["Reading", "Expression", "rubyaru"])
    return note


@pytest.mark.parametrize("text", [
    "漢字[かんじ]",
    "今日[きょう]は晴[は]れです",
    "複数[ふくすう]の漢字[かんじ]に振[ふ]り仮名[がな]",
    "漢字[かんじ] with spaces",
    "multiple 漢字[かんじ] 仮名[かな] annotations",
])
def test_detect_anki_ruby_annotation_with_ruby(text):
    """Test detection of ruby annotations in text."""
    assert detect_anki_ruby_annotation(text)


@pytest.mark.parametrize("text", [
    "漢字",
    "ひらがな",
    "カタカナ",
    "English text",
    "Mixed 漢字 and かな",
    "Incomplete [ruby]",
    "Incomplete ruby[",
    "[]",
    "",
])
def test_detect_anki_ruby_annotation_without_ruby(text):
    """Test detection of text without ruby annotations."""
    assert not detect_anki_ruby_annotation(text)


def test_update_note_with_ruby_in_reading(mock_note):
    """Test updating note when Reading field has ruby annotations."""
    # Setup mock note
    mock_note.__contains__.side_effect = lambda x: x in ["Reading", "rubyaru"]
    mock_note.__getitem__.side_effect = lambda x: "漢字[かんじ]" if x == "Reading" else ""

    # Test update
    result = update_note(mock_note)

    # Verify results
    assert result
    mock_note.__setitem__.assert_called_once_with("rubyaru", "yes")


def test_update_note_without_ruby(mock_note):
    """Test updating note when no ruby annotations are present."""
    # Setup mock note
    mock_note.__contains__.side_effect = lambda x: x in ["Reading", "rubyaru"]
    mock_note.__getitem__.side_effect = lambda x: "漢字" if x == "Reading" else ""

    # Test update
    result = update_note(mock_note)

    # Verify results
    assert result
    mock_note.__setitem__.assert_called_once_with("rubyaru", "")


def test_update_note_without_required_fields(mock_note):
    """Test that note is not updated when required fields are missing."""
    # Setup mock note without rubyaru field
    mock_note.__contains__.side_effect = lambda x: x != "rubyaru"

    # Test update
    result = update_note(mock_note)

    # Verify results
    assert not result
    mock_note.__setitem__.assert_not_called()


def test_update_note_with_multiple_source_fields(mock_note):
    """Test updating note when checking multiple source fields."""
    # Setup mock note with ruby in Expression but not in Reading
    mock_note.__contains__.side_effect = lambda x: x in ["Reading", "Expression", "rubyaru"]
    mock_note.__getitem__.side_effect = lambda x: {
        "Reading": "漢字",
        "Expression": "今日[きょう]は",
        "rubyaru": ""
    }[x]

    # Test update
    result = update_note(mock_note)

    # Verify results
    assert result
    mock_note.__setitem__.assert_called_once_with("rubyaru", "yes") 