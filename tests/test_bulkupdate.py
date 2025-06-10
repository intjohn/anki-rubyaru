from typing import Generator
from unittest.mock import MagicMock, patch

import pytest
from anki.collection import Collection
from anki.notes import Note, NoteId
from aqt.browser import Browser

from rubyaru import bulkupdate


@pytest.fixture
def mock_collection() -> MagicMock:
    """Mock Anki collection."""
    collection = MagicMock(spec=Collection)
    collection.add_custom_undo_entry.return_value = "undo_pos"
    return collection


@pytest.fixture
def mock_note() -> MagicMock:
    """Create a mock note for testing."""
    note = MagicMock(spec=Note)
    return note


@pytest.fixture
def mock_browser() -> MagicMock:
    """Mock browser window."""
    browser = MagicMock(spec=Browser)
    browser.form = MagicMock()
    browser.form.menuEdit = MagicMock()
    return browser


@pytest.fixture
def mock_update_note() -> Generator[MagicMock, None, None]:
    """Mock the update_note function."""
    with patch('rubyaru.updatenote.update_note') as mock_update:
        yield mock_update


@pytest.fixture
def mock_mw() -> Generator[MagicMock, None, None]:
    """Mock Anki's main window."""
    with patch('rubyaru.bulkupdate.mw') as mock_main_window:
        yield mock_main_window


@pytest.fixture
def mock_collection_op() -> Generator[MagicMock, None, None]:
    """Mock CollectionOp."""
    with patch('rubyaru.bulkupdate.CollectionOp') as mock_op:
        mock_op_instance = MagicMock()
        mock_op_instance.success.return_value = mock_op_instance
        mock_op.return_value = mock_op_instance
        yield mock_op


@pytest.fixture
def mock_show_info() -> Generator[MagicMock, None, None]:
    """Mock showInfo function."""
    with patch('rubyaru.bulkupdate.showInfo') as mock_info:
        yield mock_info


@pytest.fixture
def mock_qaction() -> Generator[MagicMock, None, None]:
    """Mock QAction."""
    with patch('rubyaru.bulkupdate.QAction') as mock_action:
        yield mock_action


@pytest.fixture
def mock_bulk_update_notes() -> Generator[MagicMock, None, None]:
    """Mock bulk_update_notes function."""
    with patch('rubyaru.bulkupdate.bulk_update_notes') as mock_bulk:
        yield mock_bulk


@pytest.fixture
def mock_qconnect() -> Generator[MagicMock, None, None]:
    """Mock qconnect function."""
    with patch('rubyaru.bulkupdate.qconnect') as mock_connect:
        yield mock_connect


def test_update_notes_op_with_changes(
    mock_collection: MagicMock, mock_note: MagicMock, mock_update_note: MagicMock
) -> None:
    """Test update_notes_op when notes are changed."""
    # Setup
    mock_update_note.return_value = True
    notes = [mock_note, mock_note]

    # Test
    result = bulkupdate.update_notes_op(mock_collection, notes)

    # Verify
    assert result == mock_collection.merge_undo_entries.return_value
    mock_collection.add_custom_undo_entry.assert_called_once()
    mock_collection.update_notes.assert_called_once_with(notes)
    assert mock_update_note.call_count == 2


def test_update_notes_op_without_changes(
    mock_collection: MagicMock, mock_note: MagicMock, mock_update_note: MagicMock
) -> None:
    """Test update_notes_op when no notes are changed."""
    # Setup
    mock_update_note.return_value = False
    notes = [mock_note, mock_note]

    # Test
    result = bulkupdate.update_notes_op(mock_collection, notes)

    # Verify
    assert result == mock_collection.merge_undo_entries.return_value
    mock_collection.add_custom_undo_entry.assert_called_once()
    mock_collection.update_notes.assert_called_once_with([])
    assert mock_update_note.call_count == 2


def test_bulk_update_notes_collection_op(
    mock_browser: MagicMock,
    mock_collection_op: MagicMock,
    mock_mw: MagicMock,
    mock_show_info: MagicMock,
) -> None:
    """Test bulk_update_notes function."""
    # Setup
    note_ids: list[NoteId] = [NoteId(1), NoteId(2), NoteId(3)]
    mock_notes = [MagicMock() for _ in range(3)]
    mock_mw.col.get_note.side_effect = mock_notes

    # Test
    bulkupdate.bulk_update_notes(note_ids, mock_browser)

    # Verify
    mock_collection_op.assert_called_once()
    mock_collection_op.return_value.success.assert_called_once()
    mock_collection_op.return_value.run_in_background.assert_called_once()


def test_on_browser_menus_init(
    mock_browser: MagicMock,
    mock_qaction: MagicMock,
    mock_bulk_update_notes: MagicMock,
    mock_qconnect: MagicMock,
) -> None:
    """Test browser menu initialization."""
    # Test
    bulkupdate.on_browser_menus_init(mock_browser)

    # Verify
    mock_qaction.assert_called_once()
    assert mock_qaction.call_args[1]['text'] == "Rubyaru: Bulk update"

    mock_qconnect.assert_called_once()

    mock_browser.form.menuEdit.addAction.assert_called_once()
    added_action = mock_browser.form.menuEdit.addAction.call_args[0][0]
    assert added_action == mock_qaction.return_value


def test_hook_bulk_update() -> None:
    """Test hook registration for bulk update."""
    # Setup
    from aqt import gui_hooks
    original_hooks = list(gui_hooks.browser_menus_did_init._hooks)

    # Test
    bulkupdate.hook_bulk_update()

    # Verify
    new_hooks = list(gui_hooks.browser_menus_did_init._hooks)
    assert len(new_hooks) == len(original_hooks) + 1
    assert bulkupdate.on_browser_menus_init in new_hooks

    # Cleanup
    gui_hooks.browser_menus_did_init.remove(bulkupdate.on_browser_menus_init)
