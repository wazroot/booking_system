"""empty message

Revision ID: 0bcd0988a96c
Revises: 12f95772abe6
Create Date: 2020-12-02 13:29:30.167998

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0bcd0988a96c'
down_revision = '12f95772abe6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'role',
               existing_type=sa.VARCHAR(length=200),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'role',
               existing_type=sa.VARCHAR(length=200),
               nullable=True)
    # ### end Alembic commands ###