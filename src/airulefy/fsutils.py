"""File system utilities for Airulefy."""
import os
import shutil
from pathlib import Path
from typing import Literal, Optional

def create_link_or_copy(
    source: Path,
    destination: Path,
    mode: Literal["symlink", "copy"] = "symlink",
    force: bool = False,
) -> bool:
    """Create a symlink or copy file from source to destination.
    
    Args:
        source: Source file path
        destination: Destination file path
        mode: Either "symlink" or "copy"
        force: If True, overwrite existing file/link
        
    Returns:
        bool: True if operation succeeded, False otherwise
    """
    try:
        if destination.exists() and not force:
            return False
            
        if destination.exists():
            if destination.is_symlink():
                destination.unlink()
            else:
                destination.unlink()
                
        if mode == "symlink":
            # Try symlink first
            try:
                os.symlink(source, destination)
                return True
            except OSError:
                # Fallback to copy if symlink fails
                shutil.copy2(source, destination)
                return True
        else:
            shutil.copy2(source, destination)
            return True
            
    except Exception:
        return False

def relative_path(base: Path, target: Path) -> Path:
    """Calculate relative path from base to target.
    
    Args:
        base: Base directory path
        target: Target file path
        
    Returns:
        Path: Relative path from base to target
    """
    try:
        return Path(os.path.relpath(target, base))
    except ValueError:
        # Handle case where paths are on different drives
        return target

def ensure_directory(path: Path) -> None:
    """Ensure directory exists, create if it doesn't.
    
    Args:
        path: Directory path to ensure
    """
    path.mkdir(parents=True, exist_ok=True)

def is_symlink_supported() -> bool:
    """Check if symlinks are supported on the current system.
    
    Returns:
        bool: True if symlinks are supported
    """
    try:
        test_dir = Path("test_symlink_support")
        test_dir.mkdir(exist_ok=True)
        test_file = test_dir / "test.txt"
        test_file.write_text("test")
        test_link = test_dir / "test_link.txt"
        os.symlink(test_file, test_link)
        test_link.unlink()
        test_file.unlink()
        test_dir.rmdir()
        return True
    except OSError:
        return False 