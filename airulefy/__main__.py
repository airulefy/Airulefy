"""
Main entry point for the Airulefy CLI.
"""

import sys
from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console
from rich.table import Table

from . import __version__
from .config import SyncMode, load_config
from .fsutils import find_markdown_files
from .generator.cline import ClineGenerator
from .generator.copilot import CopilotGenerator
from .generator.cursor import CursorGenerator
from .generator.devin import DevinGenerator
from .watcher import watch_directory

app = typer.Typer(
    help="Airulefy - Unify your AI rules across multiple AI coding agents.",
    add_completion=False,
)

console = Console()


def get_project_root() -> Path:
    """Get the current project root."""
    return Path.cwd()


@app.command()
def generate(
    copy: bool = typer.Option(
        False, "--copy", "-c", help="Force copy mode instead of symlink"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Show verbose output"
    ),
):
    """Generate tool-specific rule files from .ai/ directory."""
    project_root = get_project_root()
    config = load_config(project_root)
    
    # Find markdown files in the input directory
    input_dir = project_root / config.input_path
    md_files = find_markdown_files(input_dir)
    
    if not md_files:
        console.print(f"[yellow]No Markdown files found in {input_dir}[/yellow]")
        return
    
    if verbose:
        console.print(f"Found {len(md_files)} Markdown files in {input_dir}")
        for file in md_files:
            console.print(f"  - {file.relative_to(project_root)}")
    
    # Force copy mode if requested
    force_mode = SyncMode.COPY if copy else None
    
    # Generate for each tool
    success_count = 0
    for tool_name, tool_config in config.tools.items():
        generator = get_generator(tool_name, tool_config, project_root)
        if not generator:
            if verbose:
                console.print(f"[yellow]Skipping unknown tool: {tool_name}[/yellow]")
            continue
        
        if verbose:
            console.print(f"Generating rules for {tool_name}...")
        
        success = generator.generate(md_files, force_mode)
        
        if success:
            success_count += 1
            mode_text = "copied to" if force_mode == SyncMode.COPY or tool_config.mode == SyncMode.COPY else "linked to"
            rel_path = generator.output_path.relative_to(project_root)
            console.print(f"[green]✓[/green] {tool_name}: {mode_text} [blue]{rel_path}[/blue]")
        else:
            console.print(f"[red]✗[/red] {tool_name}: Failed to generate rules")
    
    if success_count == 0:
        console.print("[red]No rules were generated successfully.[/red]")
    else:
        console.print(f"[green]Successfully generated rules for {success_count} tools.[/green]")


@app.command()
def watch(
    copy: bool = typer.Option(
        False, "--copy", "-c", help="Force copy mode instead of symlink"
    ),
):
    """Watch .ai/ directory for changes and regenerate rules automatically."""
    project_root = get_project_root()
    config = load_config(project_root)
    
    input_dir = project_root / config.input_path
    
    if not input_dir.exists():
        console.print(f"[red]Directory not found: {input_dir}[/red]")
        console.print(f"Create [blue]{input_dir}[/blue] and add Markdown files to get started.")
        return
    
    console.print(f"Watching [blue]{config.input_path}[/blue] for changes...")
    console.print("Press Ctrl+C to stop.")
    
    # Initial generation
    generate(copy=copy, verbose=False)
    
    # Start watching
    watch_directory(input_dir, lambda: generate(copy=copy, verbose=False))


@app.command()
def validate():
    """Validate the configuration and rule files."""
    project_root = get_project_root()
    config = load_config(project_root)
    
    # Find markdown files in the input directory
    input_dir = project_root / config.input_path
    md_files = find_markdown_files(input_dir)
    
    # Validation checks
    errors = []
    warnings = []
    
    # Check if input directory exists
    if not input_dir.exists():
        errors.append(f"Input directory not found: {input_dir}")
    
    # Check if there are any markdown files
    if not md_files:
        warnings.append(f"No Markdown files found in {input_dir}")
    
    # Check tool configurations
    for tool_name, tool_config in config.tools.items():
        generator = get_generator(tool_name, tool_config, project_root)
        if not generator:
            warnings.append(f"Unknown tool: {tool_name}")
            continue
        
        # Check if output path is valid
        output_path = generator.output_path
        if output_path.exists() and not output_path.is_file() and not output_path.is_symlink():
            errors.append(f"Output path for {tool_name} exists but is not a file: {output_path}")
    
    # Display results
    if not errors and not warnings:
        console.print("[green]✓ All checks passed![/green]")
        return
    
    if errors:
        console.print("[red]Errors:[/red]")
        for error in errors:
            console.print(f"  [red]✗[/red] {error}")
    
    if warnings:
        console.print("[yellow]Warnings:[/yellow]")
        for warning in warnings:
            console.print(f"  [yellow]![/yellow] {warning}")
    
    if errors:
        sys.exit(1)


@app.command(name="list-tools")
def list_tools():
    """List supported AI tools and their configurations."""
    project_root = get_project_root()
    config = load_config(project_root)
    
    table = Table(title="Supported AI Tools")
    table.add_column("Tool", style="cyan")
    table.add_column("Mode", style="green")
    table.add_column("Output Path", style="blue")
    table.add_column("Status", style="yellow")
    
    for tool_name, tool_config in config.tools.items():
        generator = get_generator(tool_name, tool_config, project_root)
        
        if not generator:
            table.add_row(tool_name, str(tool_config.mode), "Unknown", "⚠️ Not supported")
            continue
        
        output_path = generator.output_path
        output_rel = output_path.relative_to(project_root)
        
        if output_path.exists():
            if output_path.is_symlink():
                status = "✓ Linked"
            else:
                status = "✓ Exists"
        else:
            status = "Not generated"
        
        table.add_row(tool_name, str(tool_config.mode), str(output_rel), status)
    
    console.print(table)


def get_generator(tool_name: str, tool_config, project_root: Path):
    """Get the generator for the specified tool."""
    generators = {
        "cursor": CursorGenerator,
        "cline": ClineGenerator,
        "copilot": CopilotGenerator,
        "devin": DevinGenerator,
    }
    
    generator_class = generators.get(tool_name)
    if not generator_class:
        return None
    
    return generator_class(tool_name, tool_config, project_root)


@app.callback(invoke_without_command=True)
def main(
    version: bool = typer.Option(False, "--version", "-V", help="Show version and exit."),
    ctx: typer.Context = typer.Context
):
    """Airulefy - Unify your AI rules across multiple AI coding agents."""
    if version:
        console.print(f"Airulefy v{__version__}")
        raise typer.Exit(0)


if __name__ == "__main__":
    app()
