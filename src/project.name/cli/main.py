"""Main CLI interface for NetSuite-Learning-Path."""

import logging
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from .. import __version__
from ..core import LCMManager
from ..core.models import Resource, LifecycleStage, ResourceStatus

app = typer.Typer(help="NetSuite-Learning-Path CLI")
console = Console()

# Global manager instance
manager: Optional[LCMManager] = None


def get_manager() -> LCMManager:
    """Get or create LCM manager instance."""
    global manager
    if manager is None:
        manager = LCMManager()
    return manager


@app.command()
def version():
    """Show version information."""
    console.print(f"NetSuite-Learning-Path version: {__version__}")


@app.command()
def status():
    """Show current LCM status."""
    mgr = get_manager()
    status_info = mgr.get_status()

    table = Table(title="LCM Status")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")

    for key, value in status_info.items():
        if isinstance(value, list):
            value = ", ".join(str(v) for v in value)
        table.add_row(key.replace("_", " ").title(), str(value))

    console.print(table)


@app.group()
def resource():
    """Resource management commands."""
    pass


@resource.command("list")
def list_resources():
    """List all resources."""
    mgr = get_manager()
    resources = mgr.list_resources()

    if not resources:
        console.print("No resources found.")
        return

    table = Table(title="Resources")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Type", style="yellow")
    table.add_column("Status", style="red")

    for res in resources:
        table.add_row(res.id, res.name, res.type, res.status)

    console.print(table)


@resource.command("add")
def add_resource(
    resource_id: str = typer.Argument(..., help="Resource ID"),
    name: str = typer.Option(..., "--name", "-n", help="Resource name"),
    resource_type: str = typer.Option(..., "--type", "-t", help="Resource type"),
):
    """Add a new resource."""
    mgr = get_manager()

    new_resource = Resource(
        id=resource_id, name=name, type=resource_type, status=ResourceStatus.CREATED
    )

    try:
        mgr.add_resource(new_resource)
        console.print(f"✅ Resource '{resource_id}' added successfully.")
    except Exception as e:
        console.print(f"❌ Error adding resource: {e}")
        raise typer.Exit(1)


@resource.command("remove")
def remove_resource(
    resource_id: str = typer.Argument(..., help="Resource ID to remove"),
):
    """Remove a resource."""
    mgr = get_manager()

    try:
        mgr.remove_resource(resource_id)
        console.print(f"✅ Resource '{resource_id}' removed successfully.")
    except Exception as e:
        console.print(f"❌ Error removing resource: {e}")
        raise typer.Exit(1)


@resource.command("show")
def show_resource(resource_id: str = typer.Argument(..., help="Resource ID to show")):
    """Show resource details."""
    mgr = get_manager()

    try:
        res = mgr.get_resource(resource_id)

        table = Table(title=f"Resource: {resource_id}")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("ID", res.id)
        table.add_row("Name", res.name)
        table.add_row("Type", res.type)
        table.add_row("Status", res.status)
        table.add_row("Created", res.created_at.isoformat())
        if res.updated_at:
            table.add_row("Updated", res.updated_at.isoformat())
        table.add_row("Tags", ", ".join(res.tags) if res.tags else "None")

        console.print(table)

    except Exception as e:
        console.print(f"❌ Error showing resource: {e}")
        raise typer.Exit(1)


@app.group()
def stage():
    """Lifecycle stage management commands."""
    pass


@stage.command("add")
def add_stage(
    name: str = typer.Argument(..., help="Stage name"),
    description: str = typer.Option(
        None, "--description", "-d", help="Stage description"
    ),
    order: int = typer.Option(1, "--order", "-o", help="Execution order"),
):
    """Add a new lifecycle stage."""
    mgr = get_manager()

    new_stage = LifecycleStage(name=name, description=description, order=order)

    mgr.add_stage(new_stage)
    console.print(f"✅ Stage '{name}' added successfully.")


@stage.command("execute")
def execute_stage(
    stage_name: str = typer.Argument(..., help="Stage name to execute"),
    resource_id: str = typer.Argument(..., help="Resource ID to process"),
):
    """Execute a lifecycle stage for a resource."""
    mgr = get_manager()

    try:
        result = mgr.execute_stage(stage_name, resource_id)
        console.print(
            f"✅ Stage '{stage_name}' executed successfully for resource '{resource_id}'"
        )
        console.print(f"Result: {result}")
    except Exception as e:
        console.print(f"❌ Error executing stage: {e}")
        raise typer.Exit(1)


@app.command()
def validate():
    """Validate current configuration."""
    mgr = get_manager()

    try:
        mgr.validate_config()
        console.print("✅ Configuration is valid.")
    except Exception as e:
        console.print(f"❌ Configuration validation failed: {e}")
        raise typer.Exit(1)


def main():
    """Main entry point."""
    app()


if __name__ == "__main__":
    main()
