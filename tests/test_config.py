from typing import Generator
from unittest.mock import MagicMock, patch

import pytest

from rubyaru import config


@pytest.fixture
def mock_addon_manager() -> Generator[MagicMock, None, None]:
    """Mock Anki's addon manager."""
    with patch('rubyaru.config.mw') as mock_mw:
        mock_mw.addonManager.getConfig.return_value = {
            "source_fields": ["Reading", "Expression"],
            "destination_field": "rubyaru"
        }
        yield mock_mw.addonManager


def test_get_config_with_valid_config(mock_addon_manager: MagicMock) -> None:
    """Test getting config with valid values."""
    cfg = config.get_config()
    assert cfg.source_fields == ["Reading", "Expression"]
    assert cfg.destination_field == "rubyaru"


def test_get_config_with_string_source_fields(mock_addon_manager: MagicMock) -> None:
    """Test getting config with comma-separated string for source fields."""
    mock_addon_manager.getConfig.return_value = {
        "source_fields": "Reading,Expression",
        "destination_field": "rubyaru"
    }
    cfg = config.get_config()
    assert cfg.source_fields == ["Reading", "Expression"]
    assert cfg.destination_field == "rubyaru"


def test_get_config_with_invalid_source_fields(mock_addon_manager: MagicMock) -> None:
    """Test getting config with invalid source fields."""
    mock_addon_manager.getConfig.return_value = {
        "source_fields": 123,  # Invalid type
        "destination_field": "rubyaru"
    }
    cfg = config.get_config()
    assert cfg.source_fields == []
    assert cfg.destination_field == "rubyaru"


def test_get_config_with_invalid_destination_field(mock_addon_manager: MagicMock) -> None:
    """Test getting config with invalid destination field."""
    mock_addon_manager.getConfig.return_value = {
        "source_fields": ["Reading"],
        "destination_field": 123  # Invalid type
    }
    cfg = config.get_config()
    assert cfg.source_fields == ["Reading"]
    assert cfg.destination_field is None


def test_get_config_with_mixed_source_fields(mock_addon_manager: MagicMock) -> None:
    """Test getting config with mixed valid/invalid source fields."""
    mock_addon_manager.getConfig.return_value = {
        "source_fields": ["Reading", 123, "Expression", None],
        "destination_field": "rubyaru"
    }
    cfg = config.get_config()
    assert cfg.source_fields == ["Reading", "Expression"]
    assert cfg.destination_field == "rubyaru"


def test_get_config_with_missing_fields(mock_addon_manager: MagicMock) -> None:
    """Test getting config with missing fields."""
    mock_addon_manager.getConfig.return_value = {}
    cfg = config.get_config()
    assert cfg.source_fields == []
    assert cfg.destination_field is None


def test_get_config_with_empty_source_fields(mock_addon_manager: MagicMock) -> None:
    """Test getting config with empty source fields."""
    mock_addon_manager.getConfig.return_value = {
        "source_fields": [],
        "destination_field": "rubyaru"
    }
    cfg = config.get_config()
    assert cfg.source_fields == []
    assert cfg.destination_field == "rubyaru"


def test_get_config_with_whitespace_in_fields(mock_addon_manager: MagicMock) -> None:
    """Test getting config with whitespace in field names."""
    mock_addon_manager.getConfig.return_value = {
        "source_fields": " Reading , Expression ",
        "destination_field": " rubyaru "
    }
    cfg = config.get_config()
    assert cfg.source_fields == ["Reading", "Expression"]
    assert cfg.destination_field == "rubyaru"
