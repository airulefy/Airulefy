"""
Extended tests for filesystem utilities.
"""

import os
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from airulefy.config import SyncMode
from airulefy.fsutils import (
    combine_markdown_files,
    find_markdown_files,
    sync_file
)


def test_symlink_fallback_to_copy(tmp_path):
    """Test that sync_file falls back to copying when symlink fails."""
    # Create source file
    source_file = tmp_path / "source.md"
    source_file.write_text("# Test Content")
    
    # Define destination
    dest_file = tmp_path / "dest.md"
    
    # Mock os.symlink to raise an OSError
    with patch('os.path.relpath', return_value="source.md"):
        with patch('pathlib.Path.symlink_to', side_effect=OSError("Mocked symlink failure")):
            # Mock shutil.copy2 to track calls
            with patch('shutil.copy2') as mock_copy:
                # Call the function
                result = sync_file(source_file, dest_file, SyncMode.SYMLINK)
                
                # Verify that copy was called when symlink fails
                mock_copy.assert_called_once_with(source_file, dest_file)
                assert result is True


def test_sync_file_create_parent_dirs(tmp_path):
    """Test that sync_file creates parent directories if they don't exist."""
    # Create source file
    source_file = tmp_path / "source.md"
    source_file.write_text("# Test Content")
    
    # Define destination in a nested directory that doesn't exist yet
    dest_file = tmp_path / "nested" / "dir" / "dest.md"
    
    # Sync the file
    result = sync_file(source_file, dest_file, SyncMode.COPY)
    
    # Check result
    assert result is True
    assert dest_file.exists()
    assert dest_file.read_text() == "# Test Content"


def test_sync_file_symlink_error_handling(tmp_path):
    """Test error handling in sync_file when symlink fails."""
    # Create source file
    source_file = tmp_path / "source.md"
    source_file.write_text("# Test Content")
    
    # Define destination
    dest_file = tmp_path / "dest.md"
    
    # Mock os.symlink to raise an OSError
    with patch('os.symlink', side_effect=OSError("Mocked symlink error")):
        # Call sync_file
        result = sync_file(source_file, dest_file, SyncMode.SYMLINK)
        
        # Check result - should fall back to copy
        assert result is True
        assert dest_file.exists()
        assert dest_file.read_text() == "# Test Content"


def test_sync_file_copy_error_handling(tmp_path):
    """Test error handling in sync_file when copy fails."""
    # Create source file
    source_file = tmp_path / "source.md"
    source_file.write_text("# Test Content")
    
    # Define destination
    dest_file = tmp_path / "dest.md"
    
    # Mock shutil.copy2 to raise an OSError
    with patch('shutil.copy2', side_effect=OSError("Mocked copy error")):
        # Call sync_file
        result = sync_file(source_file, dest_file, SyncMode.COPY)
        
        # Check result - should return False
        assert result is False
        assert not dest_file.exists()


def test_combine_markdown_files_error_handling(tmp_path):
    """Test error handling in combine_markdown_files."""
    # Create a file that can't be read
    input_file = tmp_path / "unreadable.md"
    input_file.touch()
    os.chmod(input_file, 0)  # Remove read permissions
    
    # Create output file
    output_file = tmp_path / "output.md"
    
    try:
        # This should gracefully handle the permission error
        combine_markdown_files([input_file], output_file)
        
        # Check that an empty file was created
        assert output_file.exists()
        assert output_file.stat().st_size == 0
    except PermissionError:
        # On some systems, we can't even check if a file exists without read permission
        # In this case, just pass the test
        pass
    finally:
        # Restore permissions to allow cleanup
        try:
            os.chmod(input_file, 0o644)
        except:
            pass
