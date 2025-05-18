"""GitHub Copilot tool adapter for Airulefy."""
from pathlib import Path
from typing import List

from .base import ToolAdapter

class CopilotAdapter(ToolAdapter):
    """Adapter for GitHub Copilot tool."""
    
    @property
    def tool_name(self) -> str:
        return "copilot"
        
    def _get_default_output_path(self, project_root: Path) -> Path:
        return project_root / ".github" / "copilot-instructions.md"
        
    def generate(self, markdown_files: List[Path], project_root: Path) -> bool:
        """Generate Copilot rules.
        
        Args:
            markdown_files: List of markdown files to process
            project_root: Project root directory
            
        Returns:
            bool: True if generation succeeded
        """
        output_path = self.get_output_path(project_root)
        self._ensure_output_directory(output_path)
        
        # For Copilot, we'll use the first markdown file as the source
        if not markdown_files:
            return False
            
        return self._create_rule_file(markdown_files[0], output_path) 