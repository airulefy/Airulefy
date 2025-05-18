"""Main CLI module for Airulefy."""
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from .config import AirulefyConfig
from .generator.cursor import CursorAdapter
from .generator.cline import ClineAdapter
from .generator.copilot import CopilotAdapter
from .generator.devin import DevinAdapter
from .fsutils import is_symlink_supported
from .watcher import AIWatcher

app = typer.Typer(help="AI rule file generator and symlink manager")
console = Console()

def find_markdown_files(ai_dir: Path) -> list[Path]:
    """Find all markdown files in .ai directory.
    
    Args:
        ai_dir: Path to .ai directory
        
    Returns:
        list[Path]: List of markdown files
    """
    if not ai_dir.exists():
        return []
    return list(ai_dir.rglob("*.md"))

@app.command()
def generate(
    project_root: Path = typer.Argument(
        default=Path.cwd(),
        help="Project root directory"
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Force overwrite existing files"
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Show what would be done without making changes"
    )
):
    """Generate rule files for all supported tools."""
    ai_dir = project_root / ".ai"
    config_path = project_root / ".ai-rules.yml"
    
    if not ai_dir.exists():
        console.print("[red]Error: .ai directory not found[/red]")
        sys.exit(1)
        
    config = AirulefyConfig.load(config_path)
    markdown_files = find_markdown_files(ai_dir)
    
    if not markdown_files:
        console.print("[yellow]Warning: No markdown files found in .ai directory[/yellow]")
        return
        
    # Initialize adapters
    adapters = [
        CursorAdapter(config),
        ClineAdapter(config),
        CopilotAdapter(config),
        DevinAdapter(config)
    ]
    
    if dry_run:
        table = Table(title="Dry Run Results")
        table.add_column("Tool")
        table.add_column("Output Path")
        table.add_column("Mode")
        
        for adapter in adapters:
            output_path = adapter.get_output_path(project_root)
            mode = config.get_tool_mode(adapter.tool_name)
            table.add_row(
                adapter.tool_name,
                str(output_path),
                mode.value
            )
            
        console.print(table)
        return
        
    # Generate rules
    success = True
    for adapter in adapters:
        if not adapter.generate(markdown_files, project_root):
            console.print(f"[red]Error: Failed to generate rules for {adapter.tool_name}[/red]")
            success = False
            
    if not success:
        sys.exit(1)

@app.command()
def watch(
    project_root: Path = typer.Argument(
        default=Path.cwd(),
        help="Project root directory"
    )
):
    """Watch .ai directory for changes and regenerate rules."""
    ai_dir = project_root / ".ai"
    
    def on_change():
        console.print("[blue]Change detected, regenerating rules...[/blue]")
        generate(project_root, force=True)
        
    try:
        with AIWatcher(ai_dir, on_change) as watcher:
            console.print("[green]Watching .ai directory for changes...[/green]")
            watcher.watch()
    except FileNotFoundError:
        console.print("[red]Error: .ai directory not found[/red]")
        sys.exit(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Stopping watch mode...[/yellow]")

@app.command()
def validate(
    project_root: Path = typer.Argument(
        default=Path.cwd(),
        help="Project root directory"
    )
):
    """Validate rule files and symlinks."""
    ai_dir = project_root / ".ai"
    if not ai_dir.exists():
        console.print("[red]Error: .ai directory not found[/red]")
        sys.exit(1)
        
    # Check symlink support
    if not is_symlink_supported():
        console.print("[yellow]Warning: Symlinks are not supported on this system[/yellow]")
        
    # Validate markdown files
    markdown_files = find_markdown_files(ai_dir)
    if not markdown_files:
        console.print("[yellow]Warning: No markdown files found in .ai directory[/yellow]")
        
    # Initialize adapters and validate their outputs
    config = AirulefyConfig.load(project_root / ".ai-rules.yml")
    adapters = [
        CursorAdapter(config),
        ClineAdapter(config),
        CopilotAdapter(config),
        DevinAdapter(config)
    ]
    
    table = Table(title="Validation Results")
    table.add_column("Tool")
    table.add_column("Status")
    table.add_column("Details")
    
    for adapter in adapters:
        output_path = adapter.get_output_path(project_root)
        if not output_path.exists():
            table.add_row(
                adapter.tool_name,
                "[red]Missing[/red]",
                f"Output file not found: {output_path}"
            )
        elif output_path.is_symlink() and not output_path.exists():
            table.add_row(
                adapter.tool_name,
                "[red]Broken[/red]",
                f"Broken symlink: {output_path}"
            )
        else:
            table.add_row(
                adapter.tool_name,
                "[green]OK[/green]",
                str(output_path)
            )
            
    console.print(table)

@app.command()
def list_tools():
    """List supported tools and their configurations."""
    table = Table(title="Supported Tools")
    table.add_column("Tool")
    table.add_column("Default Output")
    table.add_column("Mode")
    
    config = AirulefyConfig()
    adapters = [
        CursorAdapter(config),
        ClineAdapter(config),
        CopilotAdapter(config),
        DevinAdapter(config)
    ]
    
    for adapter in adapters:
        output_path = adapter._get_default_output_path(Path.cwd())
        mode = config.get_tool_mode(adapter.tool_name)
        table.add_row(
            adapter.tool_name,
            str(output_path),
            mode.value
        )
        
    console.print(table)

if __name__ == "__main__":
    app() 