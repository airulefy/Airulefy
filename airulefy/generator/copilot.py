"""
Generator for GitHub Copilot rules.
"""

from pathlib import Path

from ..config import ToolConfig
from .base import RuleGenerator


class CopilotGenerator(RuleGenerator):
    """Generator for GitHub Copilot rules."""
    
    def transform_content(self, content: str) -> str:
        """
        Transform Markdown content for GitHub Copilot format.
        
        Args:
            content: Original Markdown content
            
        Returns:
            str: Transformed content for GitHub Copilot
        """
        # Copilot uses standard Markdown format, so no special transformation is needed
        return content
