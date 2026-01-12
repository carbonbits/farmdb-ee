import typer

from cli.migrations import app as migrations_app

app = typer.Typer(help="FarmDB CLI")

app.add_typer(migrations_app, name="migration", help="Database migration commands")


@app.command()
def create(
    resource: str = typer.Argument(..., help="Resource type to create (e.g., 'migration')"),
    name: str = typer.Argument(..., help="Name of the resource"),
):
    """Create a new resource (e.g., migration)."""
    if resource == "migration":
        from cli.migrations import create_migration
        create_migration(name)
    else:
        typer.echo(f"Unknown resource type: {resource}", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
