"""Tests for Cursor adapter."""
import tempfile
from pathlib import Path

import pytest

from airulefy.config import AirulefyConfig
from airulefy.generator.cursor import CursorAdapter

@pytest.fixture
def temp_project():
    """Create temporary project structure."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_root = Path(tmpdir)
        ai_dir = project_root / ".ai"
        ai_dir.mkdir()
        
        # Create test markdown files
        (ai_dir / "test1.md").write_text("# Test 1")
        (ai_dir / "test2.md").write_text("# Test 2")
        
        yield project_root

def test_cursor_adapter_generate(temp_project):
    """Test Cursor adapter generation."""
    config = AirulefyConfig()
    adapter = CursorAdapter(config)
    
    # Generate rules
    markdown_files = list((temp_project / ".ai").glob("*.md"))
    assert adapter.generate(markdown_files, temp_project)
    
    # Check output file
    output_path = temp_project / ".cursor" / "rules" / "core.mdc"
    assert output_path.exists()
    
    content = output_path.read_text()
    assert "description: AI rules for Cursor" in content
    assert "alwaysApply: true" in content
    assert "@.ai/test1.md" in content
    assert "@.ai/test2.md" in content

def test_cursor_adapter_custom_output(temp_project):
    """Test Cursor adapter with custom output path."""
    config = AirulefyConfig()
    config.tools["cursor"] = config.ToolConfig(
        output=Path("custom/rules.mdc")
    )
    
    adapter = CursorAdapter(config)
    markdown_files = list((temp_project / ".ai").glob("*.md"))
    
    assert adapter.generate(markdown_files, temp_project)
    assert (temp_project / "custom" / "rules.mdc").exists()

def test_cursor_adapter_no_files(temp_project):
    """Test Cursor adapter with no markdown files."""
    config = AirulefyConfig()
    adapter = CursorAdapter(config)
    
    assert adapter.generate([], temp_project)
    output_path = temp_project / ".cursor" / "rules" / "core.mdc"
    assert output_path.exists()
    
    content = output_path.read_text()
    assert "description: AI rules for Cursor" in content
    assert "alwaysApply: true" in content 