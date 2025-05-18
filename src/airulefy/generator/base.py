"""Base generator module for Airulefy."""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from ..config import AirulefyConfig, ToolMode
from ..fsutils import create_link_or_copy, ensure_directory

class ToolAdapter(ABC):
    """Abstract base class for tool adapters."""
    
    def __init__(self, config: AirulefyConfig):
        """Initialize adapter.
        
        Args:
            config: Airulefy configuration
        """
        self.config = config
        
    @property
    @abstractmethod
    def tool_name(self) -> str:
        """Get tool name.
        
        Returns:
            str: Tool name
        """
        pass
        
    @abstractmethod
    def generate(self, markdown_files: List[Path], project_root: Path) -> bool:
        """Generate tool-specific rules.
        
        Args:
            markdown_files: List of markdown files to process
            project_root: Project root directory
            
        Returns:
            bool: True if generation succeeded
        """
        pass
        
    def get_output_path(self, project_root: Path) -> Path:
        """Get output path for tool rules.
        
        Args:
            project_root: Project root directory
            
        Returns:
            Path: Output path
        """
        tool_config = self.config.get_tool_config(self.tool_name)
        if tool_config.output:
            return project_root / tool_config.output
        return self._get_default_output_path(project_root)
        
    @abstractmethod
    def _get_default_output_path(self, project_root: Path) -> Path:
        """Get default output path for tool rules.
        
        Args:
            project_root: Project root directory
            
        Returns:
            Path: Default output path
        """
        pass
        
    def _ensure_output_directory(self, output_path: Path) -> None:
        """Ensure output directory exists.
        
        Args:
            output_path: Output path
        """
        ensure_directory(output_path.parent)
        
    def _create_rule_file(
        self,
        source: Path,
        destination: Path,
        force: bool = False
    ) -> bool:
        """Create rule file using configured mode.
        
        Args:
            source: Source file path
            destination: Destination file path
            force: If True, overwrite existing file
            
        Returns:
            bool: True if operation succeeded
        """
        mode = self.config.get_tool_mode(self.tool_name)
        return create_link_or_copy(
            source=source,
            destination=destination,
            mode=mode.value,
            force=force
        ) 