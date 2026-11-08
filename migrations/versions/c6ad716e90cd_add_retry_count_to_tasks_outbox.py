"""add retry_count to tasks_outbox

Revision ID: c6ad716e90cd
Revises: 
Create Date: ...
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c6ad716e90cd'
down_revision = 'bdc2e7f27245'  # ← ЗАМЕНИ на ID предыдущей миграции (см. ниже)
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'tasks_outbox',
        sa.Column('retry_count', sa.Integer(), nullable=False, server_default='0')
    )
    op.create_index(
        'ix_tasks_outbox_retry_count',
        'tasks_outbox',
        ['retry_count']
    )


def downgrade() -> None:
    op.drop_index('ix_tasks_outbox_retry_count', table_name='tasks_outbox')
    op.drop_column('tasks_outbox', 'retry_count')
