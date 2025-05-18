"""
File system utilities for Airulefy.
"""

import os
import shutil
from pathlib import Path
from typing import List, Union

from .config import SyncMode


def find_markdown_files(directory: Union[str, Path]) -> List[Path]:
    """
    Find all Markdown files in the specified directory.
    
    Args:
        directory: Directory to search in
        
    Returns:
        List of Path objects for the found files
    """
    directory = Path(directory)
    
    if not directory.exists() or not directory.is_dir():
        return []
    
    # Find all .md files in directory and subdirectories
    md_files = []
    for file_path in directory.glob("**/*.md"):
        if file_path.is_file():
            md_files.append(file_path)
    
    md_files.sort()  # Sort files for consistent order
    return md_files


def ensure_directory_exists(path: Union[str, Path]) -> None:
    """
    Ensure that the parent directory for the given path exists.
    
    Args:
        path: Path for which to ensure the parent directory exists
    """
    directory = Path(path).parent
    directory.mkdir(parents=True, exist_ok=True)


def sync_file(source: Union[str, Path], target: Union[str, Path], mode: SyncMode) -> bool:
    """
    Synchronize a file from source to target using the specified mode.
    
    Args:
        source: Source file path
        target: Target file path
        mode: Synchronization mode (symlink or copy)
        
    Returns:
        bool: True if successful, False otherwise
    """
    source = Path(source)
    target = Path(target)
    
    # Check if source exists
    if not source.exists() or not source.is_file():
        return False
    
    # Ensure target directory exists
    ensure_directory_exists(target)
    
    # Remove existing target if it exists
    if target.exists():
        if target.is_symlink() or target.is_file():
            target.unlink()
        else:
            return False  # Target exists but is not a file or symlink
    
    try:
        if mode == SyncMode.SYMLINK:
            # Try to create symlink
            try:
                source_rel = os.path.relpath(source, target.parent)
                target.symlink_to(source_rel)
                return True
            except (OSError, NotImplementedError):
                # Fallback to copy if symlink fails
                pass
        
        # Copy the file (either as primary mode or fallback)
        shutil.copy2(source, target)
        return True
    except Exception:
        return False


def combine_markdown_files(files: List[Path], output_file: Path) -> bool:
    """
    Combine multiple Markdown files into a single output file.
    
    Args:
        files: List of input Markdown files
        output_file: Path to the output file
        
    Returns:
        bool: True if successful, False otherwise
    """
    if not files:
        return False
    
    try:
        # Ensure output directory exists
        ensure_directory_exists(output_file)
        
        with open(output_file, 'w', encoding='utf-8') as outfile:
            for i, file_path in enumerate(files):
                with open(file_path, 'r', encoding='utf-8') as infile:
                    content = infile.read()
                    
                    # Add separator between files
                    if i > 0:
                        outfile.write('\n\n---\n\n')
                    
                    outfile.write(content)
        
        return True
    except Exception:
        return False
