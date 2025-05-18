"""Configuration models for Airulefy."""
from enum import Enum
from pathlib import Path
from typing import Dict, Optional

from pydantic import BaseModel, Field

class ToolMode(str, Enum):
    """Mode for tool rule generation."""
    SYMLINK = "symlink"
    COPY = "copy"

class ToolConfig(BaseModel):
    """Configuration for a specific tool."""
    output: Optional[Path] = None
    mode: ToolMode = ToolMode.SYMLINK

class AirulefyConfig(BaseModel):
    """Main configuration model."""
    default_mode: ToolMode = Field(
        default=ToolMode.SYMLINK,
        description="Default mode for rule generation"
    )
    tools: Dict[str, ToolConfig] = Field(
        default_factory=dict,
        description="Tool-specific configurations"
    )

    @classmethod
    def load(cls, config_path: Path) -> "AirulefyConfig":
        """Load configuration from YAML file.
        
        Args:
            config_path: Path to config file
            
        Returns:
            AirulefyConfig: Loaded configuration
        """
        if not config_path.exists():
            return cls()
            
        import yaml
        with open(config_path) as f:
            data = yaml.safe_load(f)
            return cls.model_validate(data)

    def get_tool_config(self, tool_name: str) -> ToolConfig:
        """Get configuration for a specific tool.
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            ToolConfig: Tool configuration
        """
        return self.tools.get(tool_name, ToolConfig())

    def get_tool_mode(self, tool_name: str) -> ToolMode:
        """Get mode for a specific tool.
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            ToolMode: Tool mode
        """
        tool_config = self.get_tool_config(tool_name)
        return tool_config.mode or self.default_mode 