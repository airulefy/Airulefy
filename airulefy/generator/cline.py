"""
Generator for Cline rules.
"""

from pathlib import Path

from ..config import ToolConfig
from .base import RuleGenerator


class ClineGenerator(RuleGenerator):
    """Generator for Cline rules."""
    
    def transform_content(self, content: str) -> str:
        """
        Transform Markdown content for Cline format.
        
        Args:
            content: Original Markdown content
            
        Returns:
            str: Transformed content for Cline
        """
        # Cline uses standard Markdown format, so no special transformation is needed
        return content
