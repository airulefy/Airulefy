"""Cursor tool adapter for Airulefy."""
import yaml
from pathlib import Path
from typing import List

from .base import ToolAdapter
from ..fsutils import relative_path

class CursorAdapter(ToolAdapter):
    """Adapter for Cursor tool."""
    
    @property
    def tool_name(self) -> str:
        return "cursor"
        
    def _get_default_output_path(self, project_root: Path) -> Path:
        return project_root / ".cursor" / "rules" / "core.mdc"
        
    def generate(self, markdown_files: List[Path], project_root: Path) -> bool:
        """Generate Cursor rules.
        
        Args:
            markdown_files: List of markdown files to process
            project_root: Project root directory
            
        Returns:
            bool: True if generation succeeded
        """
        output_path = self.get_output_path(project_root)
        self._ensure_output_directory(output_path)
        
        # Create front matter
        front_matter = {
            "description": "AI rules for Cursor",
            "alwaysApply": True
        }
        
        # Create content with relative paths
        content = []
        content.append("---")
        content.append(yaml.dump(front_matter))
        content.append("---\n")
        
        for md_file in markdown_files:
            rel_path = relative_path(project_root, md_file)
            content.append(f"@.ai/{rel_path}\n")
            
        # Write to output file
        try:
            output_path.write_text("\n".join(content))
            return True
        except Exception:
            return False 