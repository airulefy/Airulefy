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


def test_cursor_generate_preserve_structure(tmp_path):
    """Test generating Cursor rules with directory structure preserved."""
    # Create test files in subdirectories
    ai_dir = tmp_path / ".ai"
    ai_dir.mkdir()
    subdir = ai_dir / "sub"
    subdir.mkdir()
    input_file1 = ai_dir / "main.md"
    input_file1.write_text("# Main\n\nMain content.")
    input_file2 = subdir / "subfile.md"
    input_file2.write_text("# Sub\n\nSub content.")

    # Create a dummy .mdc file that should be removed
    output_dir = tmp_path / ".cursor/rules/sub"
    output_dir.mkdir(parents=True, exist_ok=True)
    old_file = output_dir / "old.mdc"
    old_file.write_text("old content")

    # Create generator (output path is ignored in preserve_structure mode)
    config = ToolConfig(mode=SyncMode.COPY)
    generator = CursorGenerator("cursor", config, tmp_path)

    # Find all markdown files
    md_files = [input_file1, input_file2]

    # Generate with preserve_structure=True
    result = generator.generate(md_files, preserve_structure=True)

    # Check result
    assert result is True
    out1 = tmp_path / ".cursor/rules/main.mdc"
    out2 = tmp_path / ".cursor/rules/sub/subfile.mdc"
    assert out1.exists()
    assert out2.exists()

    content1 = out1.read_text()
    content2 = out2.read_text()
    assert "# Main" in content1
    assert "Main content" in content1
    assert "# Sub" in content2
    assert "Sub content" in content2

    # Check that the old .mdc file has been removed
    assert not old_file.exists()
