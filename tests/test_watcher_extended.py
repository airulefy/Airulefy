"""
Extended tests for the watcher module.
"""

import os
import tempfile
import time
from pathlib import Path
from threading import Event
from unittest.mock import MagicMock, patch

import pytest

from airulefy.watcher import RuleChangeHandler, watch_directory


class TestRuleChangeHandler:
    """Test the RuleChangeHandler class."""
    
    def test_on_any_event_md_file(self):
        """Test that on_any_event calls the callback function for MD files."""
        # Create a mock callback
        callback = MagicMock()
        
        # Create a handler
        handler = RuleChangeHandler(callback)
        
        # Create a mock event
        event = MagicMock()
        event.is_directory = False
        event.src_path = "test.md"
        
        # Call on_any_event
        handler.on_any_event(event)
        
        # Check that callback was called once
        callback.assert_called_once()
    
    def test_on_any_event_non_md_file(self):
        """Test that on_any_event ignores non-MD files."""
        # Create a mock callback
        callback = MagicMock()
        
        # Create a handler
        handler = RuleChangeHandler(callback)
        
        # Create a mock event for a non-MD file
        event = MagicMock()
        event.is_directory = False
        event.src_path = "test.txt"  # Not an MD file
        
        # Call on_any_event
        handler.on_any_event(event)
        
        # Check that callback was not called
        callback.assert_not_called()
    
    def test_ignore_directory_events(self):
        """Test that directory events are ignored."""
        # Create a mock callback
        callback = MagicMock()
        
        # Create a handler
        handler = RuleChangeHandler(callback)
        
        # Create a mock directory event
        event = MagicMock()
        event.is_directory = True
        event.src_path = "test.md"  # Even with MD extension
        
        # Call the event handler
        handler.on_any_event(event)
        
        # Check that callback was never called
        callback.assert_not_called()
        
    def test_cooldown_period(self):
        """Test that the cooldown period prevents rapid multiple triggers."""
        # Create a mock callback
        callback = MagicMock()
        
        # Create a handler
        handler = RuleChangeHandler(callback)
        
        # Create a mock event
        event = MagicMock()
        event.is_directory = False
        event.src_path = "test.md"
        
        # Call on_any_event multiple times in rapid succession
        handler.on_any_event(event)
        handler.on_any_event(event)  # This should be ignored due to cooldown
        
        # Check that callback was called only once
        callback.assert_called_once()


def test_watch_directory(tmp_path):
    """Test watching a directory for changes."""
    # Create a temporary directory structure
    watch_dir = tmp_path / "watch_dir"
    watch_dir.mkdir()
    
    # Create a mock callback
    callback = MagicMock()
    
    # Use a side effect to exit the infinite loop in watch_directory
    # First call allows loop to start, second call raises KeyboardInterrupt to exit
    keyboard_interrupts = [False, True]
    def side_effect(*args, **kwargs):
        if keyboard_interrupts.pop(0):
            raise KeyboardInterrupt()
        time.sleep(0.1)
    
    # Patch time.sleep to control the loop
    with patch('airulefy.watcher.Observer') as MockObserver, \
         patch('airulefy.watcher.time.sleep', side_effect=side_effect):
        
        # Configure the mock observer
        mock_observer = MockObserver.return_value
        
        # Call the function - this will return when KeyboardInterrupt is raised
        watch_directory(watch_dir, callback)
        
        # Check that observer was started and stopped
        mock_observer.start.assert_called_once()
        mock_observer.stop.assert_called_once()
        mock_observer.join.assert_called_once()
        
        # Create a mock event to simulate file change
        mock_handler = mock_observer.schedule.call_args[0][0]
        mock_event = MagicMock()
        mock_event.is_directory = False
        mock_event.src_path = str(watch_dir / "test.md")
        
        # Simulate the file event
        mock_handler.on_any_event(mock_event)
        
        # Check that callback was called
        callback.assert_called_once()
