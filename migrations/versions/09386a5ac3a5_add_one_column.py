"""add one column

Revision ID: 09386a5ac3a5
Revises: 64527620a9ce
Create Date: 2020-04-17 16:26:29.730453

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09386a5ac3a5'
down_revision = '64527620a9ce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('who_owes_whom', sa.Column('debt_amount', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('who_owes_whom', 'debt_amount')
    # ### end Alembic commands ###
