import typer
from pathlib import Path

app = typer.Typer()


def get_migrations_dir() -> Path:
    """Get the migrations directory path."""
    # Navigate from src/cli to src/migrations
    return Path(__file__).parent.parent / "migrations"


def get_next_sequence_number() -> int:
    """Get the next available migration sequence number."""
    migrations_dir = get_migrations_dir()
    if not migrations_dir.exists():
        return 1
    
    existing = list(migrations_dir.glob("[0-9][0-9][0-9][0-9]_*.py"))
    if not existing:
        return 1
    
    # Extract sequence numbers from filenames
    numbers = []
    for f in existing:
        try:
            num = int(f.stem.split("_")[0])
            numbers.append(num)
        except (ValueError, IndexError):
            continue
    
    return max(numbers, default=0) + 1


def create_migration(name: str) -> None:
    """Create a new migration file."""
    migrations_dir = get_migrations_dir()
    migrations_dir.mkdir(parents=True, exist_ok=True)
    
    seq_num = get_next_sequence_number()
    # Sanitize name: lowercase, replace spaces/hyphens with underscores
    safe_name = name.lower().replace("-", "_").replace(" ", "_")
    filename = f"{seq_num:04d}_{safe_name}.py"
    filepath = migrations_dir / filename
    
    template = '''"""
Migration: {name}
"""
import duckdb


def up(conn: duckdb.DuckDBPyConnection) -> None:
    """Apply the migration."""
    # TODO: Implement migration
    pass
'''
    
    filepath.write_text(template.format(name=name))
    typer.echo(f"✓ Created migration: {filepath.relative_to(migrations_dir.parent.parent)}")


@app.command()
def apply() -> None:
    """Apply all pending migrations."""
    from core.storage.database import DB
    from core.storage.migrations.runner import apply_migrations
    
    typer.echo("Connecting to database...")
    DB.connect()
    
    try:
        conn = DB.get_connection()
        applied_count = apply_migrations(conn)
        
        if applied_count == 0:
            typer.echo("No pending migrations.")
        else:
            typer.echo(f"\n✓ Applied {applied_count} migration(s) successfully.")
    except Exception as e:
        typer.echo(f"✗ Migration failed: {e}", err=True)
        raise typer.Exit(1)
    finally:
        DB.disconnect()


@app.command()
def status() -> None:
    """Show migration status."""
    from core.storage.database import DB
    from core.storage.migrations.runner import (
        ensure_migrations_table,
        get_applied_migrations,
        discover_migrations,
    )
    
    DB.connect()
    
    try:
        conn = DB.get_connection()
        ensure_migrations_table(conn)
        
        applied = get_applied_migrations(conn)
        all_migrations = discover_migrations()
        
        if not all_migrations:
            typer.echo("No migrations found.")
            return
        
        typer.echo("Migration status:\n")
        for name, _ in all_migrations:
            status = "✓ applied" if name in applied else "○ pending"
            typer.echo(f"  {status}  {name}")
        
        pending_count = len([m for m in all_migrations if m[0] not in applied])
        typer.echo(f"\n{len(applied)} applied, {pending_count} pending")
    finally:
        DB.disconnect()
