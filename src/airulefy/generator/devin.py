"""Devin tool adapter for Airulefy."""
from pathlib import Path
from typing import List

from .base import ToolAdapter

class DevinAdapter(ToolAdapter):
    """Adapter for Devin tool."""
    
    @property
    def tool_name(self) -> str:
        return "devin"
        
    def _get_default_output_path(self, project_root: Path) -> Path:
        return project_root / "devin-guidelines.md"
        
    def generate(self, markdown_files: List[Path], project_root: Path) -> bool:
        """Generate Devin rules.
        
        Args:
            markdown_files: List of markdown files to process
            project_root: Project root directory
            
        Returns:
            bool: True if generation succeeded
        """
        output_path = self.get_output_path(project_root)
        
        # For Devin, we'll use the first markdown file as the source
        if not markdown_files:
            return False
            
        return self._create_rule_file(markdown_files[0], output_path) 