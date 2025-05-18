"""
Test file watcher functionality.
"""

import time
from pathlib import Path
from threading import Event, Thread
from typing import Optional

import pytest

from airulefy.watcher import RuleChangeHandler


def test_rule_change_handler():
    """Test that the handler detects Markdown file changes."""
    # Setup tracker for callback
    callback_triggered = Event()
    
    def callback():
        callback_triggered.set()
    
    # Create handler
    handler = RuleChangeHandler(callback)
    
    # Simulate file events
    class MockEvent:
        def __init__(self, path, is_dir=False):
            self.src_path = path
            self.is_directory = is_dir
    
    # Simulate Markdown file change
    handler.on_any_event(MockEvent("test/file.md"))
    assert callback_triggered.is_set()
    
    # Reset and test non-markdown file
    callback_triggered.clear()
    handler.on_any_event(MockEvent("test/file.txt"))
    assert not callback_triggered.is_set()
    
    # Reset and test directory event
    callback_triggered.clear()
    handler.on_any_event(MockEvent("test/dir", is_dir=True))
    assert not callback_triggered.is_set()


def test_cooldown():
    """Test that the handler respects cooldown period."""
    # Setup tracker for callback count
    callback_count = 0
    
    def callback():
        nonlocal callback_count
        callback_count += 1
    
    # Create handler with cooldown
    handler = RuleChangeHandler(callback)
    handler.cooldown = 0.1  # Short cooldown for testing
    
    # Simulate rapid file events
    class MockEvent:
        def __init__(self, path):
            self.src_path = path
            self.is_directory = False
    
    # First event should trigger
    handler.on_any_event(MockEvent("test/file.md"))
    assert callback_count == 1
    
    # Second event immediately after should not trigger due to cooldown
    handler.on_any_event(MockEvent("test/file2.md"))
    assert callback_count == 1
    
    # Wait for cooldown to expire
    time.sleep(0.2)
    
    # Third event after cooldown should trigger
    handler.on_any_event(MockEvent("test/file3.md"))
    assert callback_count == 2
