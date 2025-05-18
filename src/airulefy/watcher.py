"""File system watcher for Airulefy."""
import time
from pathlib import Path
from typing import Callable, Optional

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

class AIHandler(FileSystemEventHandler):
    """Handler for .ai directory events."""
    
    def __init__(self, callback: Callable[[], None]):
        """Initialize handler.
        
        Args:
            callback: Function to call when changes are detected
        """
        self.callback = callback
        
    def on_any_event(self, event):
        """Handle any file system event.
        
        Args:
            event: File system event
        """
        if event.src_path.endswith(".md"):
            self.callback()

class AIWatcher:
    """Watcher for .ai directory changes."""
    
    def __init__(
        self,
        ai_dir: Path,
        callback: Callable[[], None],
        recursive: bool = True
    ):
        """Initialize watcher.
        
        Args:
            ai_dir: Path to .ai directory
            callback: Function to call when changes are detected
            recursive: Whether to watch subdirectories
        """
        self.ai_dir = ai_dir
        self.callback = callback
        self.recursive = recursive
        self.observer: Optional[Observer] = None
        
    def start(self):
        """Start watching for changes."""
        if not self.ai_dir.exists():
            raise FileNotFoundError(f".ai directory not found: {self.ai_dir}")
            
        self.observer = Observer()
        self.observer.schedule(
            AIHandler(self.callback),
            str(self.ai_dir),
            recursive=self.recursive
        )
        self.observer.start()
        
    def stop(self):
        """Stop watching for changes."""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None
            
    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()
        
    def watch(self):
        """Watch for changes until interrupted."""
        try:
            self.start()
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop() 