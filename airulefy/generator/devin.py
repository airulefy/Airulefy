"""
Generator for Devin rules.
"""

from pathlib import Path

from ..config import ToolConfig
from .base import RuleGenerator


class DevinGenerator(RuleGenerator):
    """Generator for Devin rules."""
    
    def transform_content(self, content: str) -> str:
        """
        Transform Markdown content for Devin format.
        
        Args:
            content: Original Markdown content
            
        Returns:
            str: Transformed content for Devin
        """
        # Devin uses standard Markdown format, so no special transformation is needed
        return content
