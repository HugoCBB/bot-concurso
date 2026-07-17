import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

load_dotenv()

from infra.db import Base, DATABASE_URL

# Fail fast with a readable message when the DATABASE_URL secret is missing.
# An unset GitHub secret is passed as "", so the config falls back to the
# localhost default -- which never exists on a CI runner.
if "localhost" in DATABASE_URL or "127.0.0.1" in DATABASE_URL:
    raise SystemExit(
        "DATABASE_URL is not set (fell back to localhost). "
        "Set the DATABASE_URL secret in the workflow to your Supabase "
        "Session pooler URL: "
        "postgresql+psycopg://postgres.<ref>:<password>@aws-...pooler.supabase.com:5432/postgres?sslmode=require"
    )

# Show the sanitized target so misconfig is obvious in the CI log.
from sqlalchemy.engine import make_url
_safe_url = make_url(DATABASE_URL).render_as_string(hide_password=True)
print(f"[alembic] connecting to: {_safe_url}")

config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
