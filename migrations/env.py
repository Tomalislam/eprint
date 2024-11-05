from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from your_flask_app import app, db  # আপনার অ্যাপ্লিকেশনের নাম অনুযায়ী এই লাইনটি সংশোধন করুন

# হ্যালো সেশন তৈরির জন্য কনফিগারেশন
config = context.config

# লগ কনফিগারেশন
fileConfig(config.config_file_name)

# স্ক্রিপ্টের `target_metadata` সেট করুন
target_metadata = db.Model.metadata  # Flask-SQLAlchemy ব্যবহার করলে

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
