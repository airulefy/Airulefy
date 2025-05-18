"""
Test configuration functionality.
"""

import os
from pathlib import Path

import pytest
import yaml

from airulefy.config import AirulefyConfig, SyncMode, load_config


def test_default_config():
    """Test the default configuration."""
    config = AirulefyConfig()
    
    assert config.default_mode == SyncMode.SYMLINK
    assert "cursor" in config.tools
    assert "cline" in config.tools
    assert "copilot" in config.tools
    assert "devin" in config.tools
    assert config.input_path == ".ai"


def test_custom_config():
    """Test a custom configuration."""
    config = AirulefyConfig(
        default_mode=SyncMode.COPY,
        tools={
            "cursor": {"mode": SyncMode.SYMLINK, "output": "custom/path.mdc"},
            "cline": {"mode": SyncMode.COPY},
        },
        input_path="custom/ai",
    )
    
    assert config.default_mode == SyncMode.COPY
    assert config.tools["cursor"].mode == SyncMode.SYMLINK
    assert config.tools["cursor"].output == "custom/path.mdc"
    assert config.tools["cline"].mode == SyncMode.COPY
    assert config.tools["cline"].output is None
    assert config.tools["copilot"].mode == SyncMode.COPY  # Inherited from default_mode
    assert config.input_path == "custom/ai"


def test_load_config(tmp_path):
    """Test loading configuration from a file."""
    # Create a test config file
    config_data = {
        "default_mode": "copy",
        "tools": {
            "cursor": {"mode": "symlink", "output": "custom/path.mdc"},
            "cline": {"mode": "copy"},
            "copilot": {},  # Empty dict
            "devin": None,  # None value
        },
        "input_path": "custom/ai",
    }
    
    config_path = tmp_path / ".ai-rules.yml"
    with open(config_path, "w", encoding="utf-8") as f:
        yaml.dump(config_data, f)
    
    # Load the config
    config = load_config(tmp_path)
    
    # Verify the loaded config
    assert config.default_mode == SyncMode.COPY
    assert config.tools["cursor"].mode == SyncMode.SYMLINK
    assert config.tools["cursor"].output == "custom/path.mdc"
    assert config.tools["cline"].mode == SyncMode.COPY
    assert config.tools["copilot"].mode == SyncMode.COPY  # Inherited from default_mode
    assert config.tools["devin"].mode == SyncMode.COPY  # Inherited from default_mode
    assert config.input_path == "custom/ai"


def test_load_config_no_file(tmp_path):
    """Test loading configuration when no file exists."""
    config = load_config(tmp_path)
    
    # Should return default config
    assert config.default_mode == SyncMode.SYMLINK
    assert "cursor" in config.tools
    assert "cline" in config.tools
    assert "copilot" in config.tools
    assert "devin" in config.tools


def test_input_path_normalization():
    """Test input path normalization."""
    # Trailing slashes should be removed
    config = AirulefyConfig(input_path=".ai/")
    assert config.input_path == ".ai"
    
    config = AirulefyConfig(input_path=".ai\\")
    assert config.input_path == ".ai"
    
    # Empty string should default to ".ai"
    config = AirulefyConfig(input_path="")
    assert config.input_path == ".ai"
