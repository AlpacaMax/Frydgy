"""Add ondelete for Item.compartmentId

Revision ID: 866f85f39416
Revises: 
Create Date: 2022-01-23 16:34:09.400441

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '866f85f39416'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint(
        "fk_items_compartmentId_compartments",
        "items",
        "foreignkey",
    )
    op.create_foreign_key(
        None,
        "items",
        "compartments",
        ["compartmentId"],
        ["id"],
        ondelete="DELETE"
    )

def downgrade():
    op.drop_constraint(
        "fk_items_compartmentId_compartments",
        "items",
        "foreignkey",
    )
    op.create_foreign_key(
        None,
        "items",
        "compartments",
        ["compartmentId"],
        ["id"],
    )
