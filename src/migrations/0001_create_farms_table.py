"""
Migration: create_farms_table
"""
import duckdb


def up(conn: duckdb.DuckDBPyConnection) -> None:
    """Apply the migration."""
    # Create v1 schema
    conn.execute("CREATE SCHEMA IF NOT EXISTS v1")
    
    # Create configuration key-value store table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS v1.configuration (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)