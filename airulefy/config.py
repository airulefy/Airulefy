"""
Configuration handling for Airulefy.
"""

from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Union

import yaml
from pydantic import BaseModel, Field, field_validator, model_validator


class SyncMode(str, Enum):
    """Synchronization mode for AI rule files."""

    SYMLINK = "symlink"
    COPY = "copy"


class ToolConfig(BaseModel):
    """Configuration for a specific AI tool."""

    mode: SyncMode = Field(default=SyncMode.SYMLINK, description="Mode for file synchronization")
    output: Optional[str] = Field(
        default=None, description="Output file path (relative to project root)"
    )


class AirulefyConfig(BaseModel):
    """Main configuration for Airulefy."""

    default_mode: SyncMode = Field(
        default=SyncMode.SYMLINK, description="Default mode for file synchronization"
    )
    tools: Dict[str, ToolConfig] = Field(
        default_factory=dict, description="Tool-specific configurations"
    )
    input_path: str = Field(
        default=".ai", description="Path to directory containing AI rule files (relative to project root)"
    )

    @model_validator(mode="after")
    def ensure_tool_configs(self) -> "AirulefyConfig":
        """Ensure all supported tools have a configuration."""
        supported_tools = ["cursor", "cline", "copilot", "devin"]
        
        for tool in supported_tools:
            if tool not in self.tools:
                # Create default config for missing tools
                self.tools[tool] = ToolConfig(mode=self.default_mode)
            else:
                # Ensure existing tools have the proper mode set
                if not self.tools[tool] or self.tools[tool].mode is None:
                    self.tools[tool] = ToolConfig(mode=self.default_mode)
                
        return self
    
    @field_validator("input_path")
    @classmethod
    def validate_input_path(cls, v: str) -> str:
        """Validate input path."""
        if not v:
            return ".ai"
        
        # Normalize path
        return v.rstrip("/\\")


def load_config(project_root: Union[str, Path]) -> AirulefyConfig:
    """
    Load configuration from .ai-rules.yml in the project root.
    
    Args:
        project_root: Path to the project root directory
        
    Returns:
        AirulefyConfig: Configuration object
    """
    project_root = Path(project_root)
    config_path = project_root / ".ai-rules.yml"
    
    if not config_path.exists():
        # Return default config if no config file exists
        return AirulefyConfig()
    
    with open(config_path, "r", encoding="utf-8") as f:
        config_data = yaml.safe_load(f) or {}
    
    # Get the default mode before processing tools
    default_mode = config_data.get("default_mode", SyncMode.SYMLINK)
    
    # Parse tool configs from raw data
    if "tools" in config_data and isinstance(config_data["tools"], dict):
        tools_data = {}
        for tool_name, tool_config in config_data["tools"].items():
            if tool_config is None:
                # For None values, use default mode from config
                tools_data[tool_name] = {"mode": default_mode}
            elif not isinstance(tool_config, dict):
                # Convert other non-dict configs to dict with default mode
                tools_data[tool_name] = {"mode": default_mode}
            elif "mode" not in tool_config:
                # If mode is not specified, use default mode
                tool_config_copy = dict(tool_config)
                tool_config_copy["mode"] = default_mode
                tools_data[tool_name] = tool_config_copy
            else:
                # Keep as is
                tools_data[tool_name] = tool_config
                
        # Replace the tools data in config
        config_data["tools"] = tools_data
    
    return AirulefyConfig(**config_data)


def get_default_output_path(tool_name: str) -> str:
    """
    Get the default output path for a specific tool.
    
    Args:
        tool_name: Name of the tool
        
    Returns:
        str: Default output path relative to project root
    """
    default_paths = {
        "cursor": ".cursor/rules/core.mdc",
        "cline": ".cline-rules",
        "copilot": ".github/copilot-instructions.md",
        "devin": "devin-guidelines.md",
    }
    
    return default_paths.get(tool_name, f".{tool_name}-rules.md")
