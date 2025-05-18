"""Cline tool adapter for Airulefy."""
from pathlib import Path
from typing import List

from .base import ToolAdapter

class ClineAdapter(ToolAdapter):
    """Adapter for Cline tool."""
    
    @property
    def tool_name(self) -> str:
        return "cline"
        
    def _get_default_output_path(self, project_root: Path) -> Path:
        return project_root / ".cline-rules"
        
    def generate(self, markdown_files: List[Path], project_root: Path) -> bool:
        """Generate Cline rules.
        
        Args:
            markdown_files: List of markdown files to process
            project_root: Project root directory
            
        Returns:
            bool: True if generation succeeded
        """
        output_dir = self.get_output_path(project_root)
        self._ensure_output_directory(output_dir)
        
        success = True
        for md_file in markdown_files:
            output_path = output_dir / md_file.name
            if not self._create_rule_file(md_file, output_path):
                success = False
                
        return success 