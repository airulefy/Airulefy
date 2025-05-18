"""
File watcher for Airulefy.
"""

import time
from pathlib import Path
from typing import Callable

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer


class RuleChangeHandler(FileSystemEventHandler):
    """Handle file system events for AI rule files."""
    
    def __init__(self, callback: Callable[[], None]):
        """
        Initialize the handler.
        
        Args:
            callback: Function to call when a change is detected
        """
        self.callback = callback
        self.last_triggered = 0
        self.cooldown = 1.0  # Cooldown in seconds to avoid multiple rapid triggers
    
    def on_any_event(self, event: FileSystemEvent) -> None:
        """
        Handle any file system event.
        
        Args:
            event: File system event
        """
        # Only trigger on markdown files
        if not event.is_directory and self._is_markdown_file(event.src_path):
            current_time = time.time()
            # Check if it's been long enough since the last trigger
            if current_time - self.last_triggered > self.cooldown:
                self.last_triggered = current_time
                self.callback()
    
    def _is_markdown_file(self, path: str) -> bool:
        """
        Check if a file is a Markdown file.
        
        Args:
            path: File path
            
        Returns:
            bool: True if the file is a Markdown file, False otherwise
        """
        return path.lower().endswith('.md')


def watch_directory(directory: Path, callback: Callable[[], None]) -> None:
    """
    Watch a directory for changes to Markdown files.
    
    Args:
        directory: Directory to watch
        callback: Function to call when changes are detected
    """
    observer = Observer()
    handler = RuleChangeHandler(callback)
    
    # Start watching
    observer.schedule(handler, str(directory), recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()
