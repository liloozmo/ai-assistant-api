"""initial migration

Revision ID: 545bc312d9c6
Revises: 
Create Date: 2025-06-11 20:30:50.132243

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '545bc312d9c6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Step 1: Create new table with corrected column name
    op.create_table(
        'chats_new',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('when_created', sa.DateTime()),
        sa.Column('assistant_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['assistant_id'], ['assistants.id']),
    )

    # Step 2: Copy data over from old table, renaming column
    op.execute("""
        INSERT INTO chats_new (id, when_created, assistant_id)
        SELECT id, when_created, "Assistant_id" FROM chats;
    """)

    # Step 3: Drop old table
    op.drop_table('chats')

    # Step 4: Rename new table to old name
    op.rename_table('chats_new', 'chats')


def downgrade() -> None:
    # Step 1: Re-create old table with original column name
    op.create_table(
        'chats_old',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('when_created', sa.DateTime()),
        sa.Column('Assistant_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['Assistant_id'], ['assistants.id']),
    )

    # Step 2: Copy data back
    op.execute("""
        INSERT INTO chats_old (id, when_created, "Assistant_id")
        SELECT id, when_created, assistant_id FROM chats;
    """)

    # Step 3: Drop new table
    op.drop_table('chats')

    # Step 4: Rename old table back to original
    op.rename_table('chats_old', 'chats')
