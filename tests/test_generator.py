"""
Test the base generator functionality.
"""

from pathlib import Path

import pytest

from airulefy.config import SyncMode, ToolConfig
from airulefy.generator.base import RuleGenerator
from airulefy.generator.cursor import CursorGenerator


# Concrete implementation of the abstract RuleGenerator class for testing
class TestGenerator(RuleGenerator):
    """Test implementation of RuleGenerator."""
    
    def __init__(self, tool_name: str, tool_config: ToolConfig, project_root: Path):
        """Initialize the test generator."""
        super().__init__(tool_name, tool_config, project_root)
        self.last_generated_files = []
    
    def transform_content(self, content: str) -> str:
        """Transform content for testing."""
        return f"TRANSFORMED: {content}"


def test_rule_generator_init():
    """Test RuleGenerator initialization."""
    config = ToolConfig(mode=SyncMode.COPY, output="custom/path.md")
    generator = TestGenerator("test", config, Path("/project"))
    
    assert generator.tool_name == "test"
    assert generator.config == config
    assert generator.project_root == Path("/project")
    assert generator.output_path == Path("/project/custom/path.md")


def test_rule_generator_default_output_path():
    """Test RuleGenerator with default output path."""
    config = ToolConfig(mode=SyncMode.COPY)  # No output path specified
    generator = TestGenerator("cursor", config, Path("/project"))
    
    assert generator.output_path == Path("/project/.cursor/rules/core.mdc")


def test_rule_generator_generate_single_file(tmp_path):
    """Test generating from a single file."""
    # Create test file
    input_file = tmp_path / "input.md"
    input_file.write_text("# Test content")
    
    # Create generator
    config = ToolConfig(mode=SyncMode.COPY, output="output.md")
    generator = TestGenerator("test", config, tmp_path)
    
    # Generate
    result = generator.generate([input_file])
    
    # Check result
    assert result is True
    assert (tmp_path / "output.md").exists()
    assert (tmp_path / "output.md").read_text() == "TRANSFORMED: # Test content"


def test_rule_generator_generate_multiple_files(tmp_path):
    """Test generating from multiple files."""
    # Create test files
    input_file1 = tmp_path / "input1.md"
    input_file1.write_text("# File 1")
    
    input_file2 = tmp_path / "input2.md"
    input_file2.write_text("# File 2")
    
    # Create generator
    config = ToolConfig(mode=SyncMode.COPY, output="output.md")
    generator = TestGenerator("test", config, tmp_path)
    
    # Generate
    result = generator.generate([input_file1, input_file2])
    
    # Check result
    assert result is True
    assert (tmp_path / "output.md").exists()
    
    content = (tmp_path / "output.md").read_text()
    assert "TRANSFORMED: " in content
    assert "# File 1" in content
    assert "# File 2" in content


def test_rule_generator_generate_symlink(tmp_path):
    """Test generating with symlink mode."""
    # Create test file
    input_file = tmp_path / "input.md"
    input_file.write_text("# Test content")
    
    # Create generator
    config = ToolConfig(mode=SyncMode.SYMLINK, output="output.md")
    generator = TestGenerator("test", config, tmp_path)
    
    # Generate with force symlink
    result = generator.generate([input_file], force_mode=SyncMode.SYMLINK)
    
    # Check result
    assert result is True
    assert (tmp_path / "output.md").exists()
    
    # If symlink is supported, check that it's a symlink
    # If not, check that content is copied
    output_path = tmp_path / "output.md"
    if output_path.is_symlink():
        # On platforms where symlinks work
        assert output_path.read_text() == "# Test content"  # Original content, not transformed
    else:
        # On platforms where symlinks don't work and it falls back to copy
        assert output_path.read_text() == "# Test content"


def test_rule_generator_generate_force_copy(tmp_path):
    """Test generating with forced copy mode."""
    # Create test file
    input_file = tmp_path / "input.md"
    input_file.write_text("# Test content")
    
    # Create generator
    config = ToolConfig(mode=SyncMode.SYMLINK, output="output.md")
    generator = TestGenerator("test", config, tmp_path)
    
    # Generate with force copy
    result = generator.generate([input_file], force_mode=SyncMode.COPY)
    
    # Check result
    assert result is True
    assert (tmp_path / "output.md").exists()
    assert not (tmp_path / "output.md").is_symlink()
    assert (tmp_path / "output.md").read_text() == "TRANSFORMED: # Test content"


def test_rule_generator_generate_preserve_structure(tmp_path):
    """Test generating with preserve_structure option."""
    # Create test files in subdirectories
    input_dir = tmp_path / ".ai"
    input_dir.mkdir()
    subdir = input_dir / "sub"
    subdir.mkdir()

    input_file1 = input_dir / "main.md"
    input_file1.write_text("# Main content")

    input_file2 = subdir / "subfile.md"
    input_file2.write_text("# Sub content")

    # Create generator
    config = ToolConfig(mode=SyncMode.COPY, output=".cursor/rules")
    generator = CursorGenerator("cursor", config, tmp_path)

    # Generate with preserve_structure
    result = generator.generate([input_file1, input_file2], preserve_structure=True, input_dir=input_dir)

    # Check result
    assert result is True

    # Check that files were generated in the correct structure
    output_dir = tmp_path / ".cursor/rules"
    assert (output_dir / "main.mdc").exists()
    assert (output_dir / "sub" / "subfile.mdc").exists()

    # Check content
    content1 = (output_dir / "main.mdc").read_text()
    content2 = (output_dir / "sub" / "subfile.mdc").read_text()
    assert "# Main content" in content1
    assert "# Sub content" in content2
