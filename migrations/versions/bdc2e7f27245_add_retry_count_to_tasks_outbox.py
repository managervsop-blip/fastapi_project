"""add retry_count to tasks_outbox

Revision ID: bdc2e7f27245
Revises: b567e79a02bb
Create Date: 2026-11-09 00:55:45.124076

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bdc2e7f27245'
down_revision: Union[str, Sequence[str], None] = 'b567e79a02bb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
