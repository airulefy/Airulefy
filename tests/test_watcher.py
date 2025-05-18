"""Tests for the watcher module."""
import time
from pathlib import Path

import pytest

from airulefy.watcher import AIWatcher

@pytest.fixture
def temp_ai_dir(tmp_path):
    """Create temporary .ai directory."""
    ai_dir = tmp_path / ".ai"
    ai_dir.mkdir()
    return ai_dir

def test_watcher_start_stop(temp_ai_dir):
    """Test watcher start and stop."""
    callback_called = False
    
    def callback():
        nonlocal callback_called
        callback_called = True
        
    watcher = AIWatcher(temp_ai_dir, callback)
    watcher.start()
    assert watcher.observer is not None
    
    watcher.stop()
    assert watcher.observer is None

def test_watcher_context_manager(temp_ai_dir):
    """Test watcher as context manager."""
    callback_called = False
    
    def callback():
        nonlocal callback_called
        callback_called = True
        
    with AIWatcher(temp_ai_dir, callback) as watcher:
        assert watcher.observer is not None
        
    assert watcher.observer is None

def test_watcher_missing_directory():
    """Test watcher with missing directory."""
    with pytest.raises(FileNotFoundError):
        AIWatcher(Path("/nonexistent"), lambda: None).start()

def test_watcher_callback(temp_ai_dir):
    """Test watcher callback on file change."""
    callback_called = False
    
    def callback():
        nonlocal callback_called
        callback_called = True
        
    with AIWatcher(temp_ai_dir, callback) as watcher:
        # Create a markdown file
        (temp_ai_dir / "test.md").write_text("# Test")
        
        # Wait for event processing
        time.sleep(0.1)
        
        assert callback_called

def test_watcher_non_markdown(temp_ai_dir):
    """Test watcher ignores non-markdown files."""
    callback_called = False
    
    def callback():
        nonlocal callback_called
        callback_called = True
        
    with AIWatcher(temp_ai_dir, callback) as watcher:
        # Create a non-markdown file
        (temp_ai_dir / "test.txt").write_text("Test")
        
        # Wait for event processing
        time.sleep(0.1)
        
        assert not callback_called 