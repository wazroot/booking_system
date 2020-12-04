"""empty message

Revision ID: b5142dba8bc5
Revises: 0bcd0988a96c
Create Date: 2020-12-04 15:19:47.182305

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b5142dba8bc5'
down_revision = '0bcd0988a96c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('reservation', 'updated_at')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reservation', sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
