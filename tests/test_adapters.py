"""Tests for all tool adapters."""
import tempfile
from pathlib import Path

import pytest

from airulefy.config import AirulefyConfig
from airulefy.generator.cursor import CursorAdapter
from airulefy.generator.cline import ClineAdapter
from airulefy.generator.copilot import CopilotAdapter
from airulefy.generator.devin import DevinAdapter

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

@pytest.mark.parametrize("adapter_class", [
    CursorAdapter,
    ClineAdapter,
    CopilotAdapter,
    DevinAdapter
])
def test_adapter_generate(adapter_class, temp_project):
    """Test adapter generation."""
    config = AirulefyConfig()
    adapter = adapter_class(config)
    
    # Generate rules
    markdown_files = list((temp_project / ".ai").glob("*.md"))
    assert adapter.generate(markdown_files, temp_project)
    
    # Check output exists
    output_path = adapter.get_output_path(temp_project)
    assert output_path.exists()

@pytest.mark.parametrize("adapter_class", [
    CursorAdapter,
    ClineAdapter,
    CopilotAdapter,
    DevinAdapter
])
def test_adapter_custom_output(adapter_class, temp_project):
    """Test adapter with custom output path."""
    config = AirulefyConfig()
    config.tools[adapter_class().tool_name] = config.ToolConfig(
        output=Path("custom/rules.md")
    )
    
    adapter = adapter_class(config)
    markdown_files = list((temp_project / ".ai").glob("*.md"))
    
    assert adapter.generate(markdown_files, temp_project)
    assert (temp_project / "custom" / "rules.md").exists()

@pytest.mark.parametrize("adapter_class", [
    CursorAdapter,
    ClineAdapter,
    CopilotAdapter,
    DevinAdapter
])
def test_adapter_no_files(adapter_class, temp_project):
    """Test adapter with no markdown files."""
    config = AirulefyConfig()
    adapter = adapter_class(config)
    
    # Some adapters should fail with no files
    if adapter_class in [CopilotAdapter, DevinAdapter]:
        assert not adapter.generate([], temp_project)
    else:
        assert adapter.generate([], temp_project)
        output_path = adapter.get_output_path(temp_project)
        assert output_path.exists()

def test_cursor_adapter_content(temp_project):
    """Test Cursor adapter content format."""
    config = AirulefyConfig()
    adapter = CursorAdapter(config)
    
    markdown_files = list((temp_project / ".ai").glob("*.md"))
    assert adapter.generate(markdown_files, temp_project)
    
    output_path = temp_project / ".cursor" / "rules" / "core.mdc"
    content = output_path.read_text()
    
    assert "description: AI rules for Cursor" in content
    assert "alwaysApply: true" in content
    assert "@.ai/test1.md" in content
    assert "@.ai/test2.md" in content

def test_cline_adapter_multiple_files(temp_project):
    """Test Cline adapter with multiple files."""
    config = AirulefyConfig()
    adapter = ClineAdapter(config)
    
    markdown_files = list((temp_project / ".ai").glob("*.md"))
    assert adapter.generate(markdown_files, temp_project)
    
    output_dir = temp_project / ".cline-rules"
    assert (output_dir / "test1.md").exists()
    assert (output_dir / "test2.md").exists()
    
    # Check content
    assert (output_dir / "test1.md").read_text() == "# Test 1"
    assert (output_dir / "test2.md").read_text() == "# Test 2" 