"""
Base generator class for Airulefy.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import List, Optional, Union

from ..config import SyncMode, ToolConfig, get_default_output_path
from ..fsutils import combine_markdown_files, sync_file


class RuleGenerator(ABC):
    """Base class for AI rule generators."""

    def __init__(self, tool_name: str, tool_config: ToolConfig, project_root: Path):
        """
        Initialize the generator.
        
        Args:
            tool_name: Name of the AI tool
            tool_config: Configuration for the AI tool
            project_root: Path to the project root
        """
        self.tool_name = tool_name
        self.config = tool_config
        self.project_root = project_root
        self.output_path = self._resolve_output_path()
    
    def _resolve_output_path(self) -> Path:
        """
        Resolve the output path for the rule file.
        
        Returns:
            Path to the output file
        """
        # Use the configured output path or the default
        output_rel = self.config.output or get_default_output_path(self.tool_name)
        return self.project_root / output_rel
    
    @abstractmethod
    def transform_content(self, content: str) -> str:
        """
        Transform the content for the specific tool format.
        
        Args:
            content: Original content
            
        Returns:
            Transformed content
        """
        # Default implementation: return the content as-is
        return content
    
    def generate(self, input_files: List[Path], force_mode: Optional[SyncMode] = None) -> bool:
        """
        Generate the rule file for the AI tool.
        
        Args:
            input_files: List of input Markdown files
            force_mode: Force a specific sync mode (overrides config)
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not input_files:
            return False
        
        # Determine sync mode
        mode = force_mode if force_mode is not None else self.config.mode
        
        # Make sure the output directory exists
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # For a single input file, we can directly sync it
        if len(input_files) == 1 and mode == SyncMode.SYMLINK:
            # Skip transformation for symlink if possible
            return sync_file(input_files[0], self.output_path, mode)
        
        # For multiple files or when transformation is needed
        try:
            # Create a temporary file for the combined/transformed content
            with NamedTemporaryFile(mode='w+', encoding='utf-8', suffix='.md', delete=False) as tmp_file:
                temp_path = Path(tmp_file.name)
                
                # Combine input files
                if len(input_files) == 1:
                    with open(input_files[0], 'r', encoding='utf-8') as f:
                        content = f.read()
                else:
                    # Create temporary combined file
                    combined_path = Path(tmp_file.name + '.combined')
                    combine_markdown_files(input_files, combined_path)
                    
                    with open(combined_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Clean up the combined file
                    combined_path.unlink()
                
                # Transform content for the specific tool
                transformed_content = self.transform_content(content)
                
                # Write the transformed content to the temporary file
                tmp_file.write(transformed_content)
                tmp_file.flush()
            
            # Sync the temporary file to the output path
            result = sync_file(temp_path, self.output_path, mode)
            
            # Clean up the temporary file
            temp_path.unlink()
            
            return result
        
        except Exception as e:
            print(f"Error generating rule file for {self.tool_name}: {e}")
            return False
