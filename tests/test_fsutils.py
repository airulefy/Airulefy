"""
Test file system utilities.
"""

import os
from pathlib import Path

import pytest

from airulefy.config import SyncMode
from airulefy.fsutils import (
    combine_markdown_files,
    ensure_directory_exists,
    find_markdown_files,
    sync_file,
)


def test_find_markdown_files(tmp_path):
    """Test finding Markdown files."""
    # Create test structure
    ai_dir = tmp_path / ".ai"
    ai_dir.mkdir()
    
    # Create files
    (ai_dir / "main.md").write_text("# Main instruction")
    (ai_dir / "secondary.md").write_text("# Secondary instruction")
    
    # Create subdirectory with file
    sub_dir = ai_dir / "sub"
    sub_dir.mkdir()
    (sub_dir / "nested.md").write_text("# Nested instruction")
    
    # Create non-markdown file
    (ai_dir / "ignored.txt").write_text("Not markdown")
    
    # Find markdown files
    files = find_markdown_files(ai_dir)
    
    # Check results
    assert len(files) == 3
    filenames = [f.name for f in files]
    assert "main.md" in filenames
    assert "secondary.md" in filenames
    assert "nested.md" in filenames
    assert "ignored.txt" not in filenames


def test_find_markdown_files_empty_dir(tmp_path):
    """Test finding Markdown files in an empty directory."""
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    
    files = find_markdown_files(empty_dir)
    assert len(files) == 0


def test_find_markdown_files_nonexistent_dir(tmp_path):
    """Test finding Markdown files in a nonexistent directory."""
    nonexistent_dir = tmp_path / "nonexistent"
    
    files = find_markdown_files(nonexistent_dir)
    assert len(files) == 0


def test_ensure_directory_exists(tmp_path):
    """Test ensuring directory exists."""
    nested_path = tmp_path / "a" / "b" / "c" / "file.txt"
    
    ensure_directory_exists(nested_path)
    
    assert (tmp_path / "a" / "b" / "c").exists()
    assert (tmp_path / "a" / "b" / "c").is_dir()


def test_sync_file_copy(tmp_path):
    """Test syncing a file with copy mode."""
    source_file = tmp_path / "source.md"
    source_file.write_text("# Test content")
    
    target_file = tmp_path / "target" / "target.md"
    
    result = sync_file(source_file, target_file, SyncMode.COPY)
    
    assert result is True
    assert target_file.exists()
    assert target_file.read_text() == "# Test content"
    assert not target_file.is_symlink()


def test_sync_file_symlink(tmp_path):
    """Test syncing a file with symlink mode."""
    source_file = tmp_path / "source.md"
    source_file.write_text("# Test content")
    
    target_file = tmp_path / "target" / "target.md"
    
    # Symlink might not work on all platforms, so we just check the result
    result = sync_file(source_file, target_file, SyncMode.SYMLINK)
    
    assert result is True
    assert target_file.exists()
    
    # On platforms where symlink works, verify it's a symlink
    # On platforms where it falls back to copy, verify the content
    if target_file.is_symlink():
        assert os.path.normpath(os.readlink(target_file)) == os.path.normpath(
            os.path.relpath(source_file, target_file.parent)
        )
    else:
        assert target_file.read_text() == "# Test content"


def test_sync_file_nonexistent_source(tmp_path):
    """Test syncing a nonexistent source file."""
    source_file = tmp_path / "nonexistent.md"
    target_file = tmp_path / "target.md"
    
    result = sync_file(source_file, target_file, SyncMode.COPY)
    
    assert result is False
    assert not target_file.exists()


def test_combine_markdown_files(tmp_path):
    """Test combining multiple Markdown files."""
    # Create test files
    file1 = tmp_path / "file1.md"
    file1.write_text("# File 1\nContent of file 1")
    
    file2 = tmp_path / "file2.md"
    file2.write_text("# File 2\nContent of file 2")
    
    output_file = tmp_path / "output" / "combined.md"
    
    result = combine_markdown_files([file1, file2], output_file)
    
    assert result is True
    assert output_file.exists()
    
    content = output_file.read_text()
    assert "# File 1\nContent of file 1" in content
    assert "# File 2\nContent of file 2" in content
    assert "---" in content  # Check for separator
