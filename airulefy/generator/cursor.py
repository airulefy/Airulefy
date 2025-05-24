"""
Generator for Cursor rules.
"""

from pathlib import Path
from typing import List, Optional
import tempfile

from ..config import ToolConfig, SyncMode
from .base import RuleGenerator
from ..fsutils import sync_file


class CursorGenerator(RuleGenerator):
    """Generator for Cursor rules."""
    
    def __init__(self, tool_name: str, tool_config: ToolConfig, project_root: Path):
        super().__init__(tool_name, tool_config, project_root)
        self.last_generated_files = []

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

    def generate(
        self,
        input_files: List[Path],
        force_mode: Optional[SyncMode] = None,
        preserve_structure: bool = False
    ) -> bool:
        """
        Generate the rule file(s) for Cursor.

        Args:
            input_files: List of input Markdown files
            force_mode: Force a specific sync mode (overrides config)
            preserve_structure: If True, preserve directory structure and output multiple .mdc files

        Returns:
            bool: True if successful, False otherwise
        """
        self.last_generated_files = []
        if not preserve_structure:
            return super().generate(input_files, force_mode)

        if not input_files:
            return False

        # Determine sync mode
        mode = force_mode if force_mode is not None else self.config.mode

        # Set up project and output directories
        project_root = self.project_root
        input_root = project_root / ".ai"
        output_root = project_root / ".cursor/rules"

        # Remove all existing .mdc files in output_root
        if preserve_structure and output_root.exists():
            for f in output_root.rglob("*.mdc"):
                f.unlink()

        success = True

        for md_file in input_files:
            try:
                # Calculate the relative path for output
                rel_path = md_file.relative_to(input_root)
                out_path = output_root / rel_path.with_suffix(".mdc")

                # Make sure the output directory exists
                out_path.parent.mkdir(parents=True, exist_ok=True)

                # Read the content of the input Markdown file
                with open(md_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # Transform the content for Cursor's .mdc format
                transformed = self.transform_content(content)

                # Write the transformed content to a temporary file
                with tempfile.NamedTemporaryFile(mode='w+', encoding='utf-8', suffix='.mdc', delete=False) as tmp_file:
                    tmp_file.write(transformed)
                    tmp_file.flush()
                    temp_path = Path(tmp_file.name)

                # Synchronize the temporary file to the output path using the specified mode
                result = sync_file(temp_path, out_path, mode)

                # Clean up the temporary file
                temp_path.unlink()

                # If sync succeeded, add to list
                if result:
                    self.last_generated_files.append(out_path)
                else:
                    print(f"Error generating rule file for {md_file}")
                    success = False
            except Exception as e:
                # Print any exception that occurs and mark as unsuccessful
                print(f"Error generating rule file for {md_file}: {e}")
                success = False

        return success
