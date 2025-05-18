"""
Generator for Cursor rules.
"""

from pathlib import Path

from ..config import ToolConfig
from .base import RuleGenerator


class CursorGenerator(RuleGenerator):
    """Generator for Cursor rules."""
    
    def transform_content(self, content: str) -> str:
        """
        Transform Markdown content for Cursor's .mdc format.
        
        Args:
            content: Original Markdown content
            
        Returns:
            str: Transformed content for Cursor
        """
        # Cursor's .mdc format has some special handling:
        # 1. Make sure there's a title at the top (if none exists)
        # 2. Convert any header format to be compatible with .mdc
        # 3. Handle any special Cursor-specific formatting
        
        lines = content.split("\n")
        transformed_lines = []
        
        # Check if there's a title at the top (# Title)
        has_title = False
        for line in lines[:5]:  # Check first few lines
            if line.strip().startswith("# "):
                has_title = True
                break
        
        # If no title found, add a default one
        if not has_title:
            transformed_lines.append("# Cursor Rules")
            transformed_lines.append("")
        
        # Process the rest of the content
        for line in lines:
            # Append the line (no special transformations needed for .mdc format)
            transformed_lines.append(line)
        
        return "\n".join(transformed_lines)
