"""
Test Cursor generator implementation.
"""

from pathlib import Path

import pytest

from airulefy.config import ToolConfig, SyncMode
from airulefy.generator.cursor import CursorGenerator


def test_cursor_transform_content_with_title():
    """Test transforming content that already has a title."""
    content = "# Existing Title\n\nThis is some content."
    
    generator = CursorGenerator(
        "cursor", 
        ToolConfig(mode=SyncMode.COPY), 
        Path("/project")
    )
    
    transformed = generator.transform_content(content)
    
    # Content should be unchanged since it already has a title
    assert transformed == content


def test_cursor_transform_content_without_title():
    """Test transforming content without a title."""
    content = "This is some content without a title."
    
    generator = CursorGenerator(
        "cursor", 
        ToolConfig(mode=SyncMode.COPY), 
        Path("/project")
    )
    
    transformed = generator.transform_content(content)
    
    # Should add a default title
    assert transformed.startswith("# Cursor Rules\n\n")
    assert transformed.endswith(content)


def test_cursor_generate_file(tmp_path):
    """Test generating a Cursor rule file."""
    # Create test file
    input_file = tmp_path / "input.md"
    input_file.write_text("# Custom Rules\n\nThis is a test rule.")
    
    # Create generator with custom output path
    config = ToolConfig(mode=SyncMode.COPY, output="cursor-rules.mdc")
    generator = CursorGenerator("cursor", config, tmp_path)
    
    # Generate
    result = generator.generate([input_file])
    
    # Check result
    assert result is True
    assert (tmp_path / "cursor-rules.mdc").exists()
    assert "# Custom Rules" in (tmp_path / "cursor-rules.mdc").read_text()


def test_cursor_generate_multiple_files(tmp_path):
    """Test generating Cursor rules from multiple files."""
    # Create test files
    input_file1 = tmp_path / "part1.md"
    input_file1.write_text("# Part 1\n\nThis is part 1.")
    
    input_file2 = tmp_path / "part2.md"
    input_file2.write_text("# Part 2\n\nThis is part 2.")
    
    # Create generator
    config = ToolConfig(mode=SyncMode.COPY, output="cursor-rules.mdc")
    generator = CursorGenerator("cursor", config, tmp_path)
    
    # Generate
    result = generator.generate([input_file1, input_file2])
    
    # Check result
    assert result is True
    assert (tmp_path / "cursor-rules.mdc").exists()
    
    content = (tmp_path / "cursor-rules.mdc").read_text()
    assert "# Part 1" in content
    assert "This is part 1." in content
    assert "# Part 2" in content
    assert "This is part 2." in content
