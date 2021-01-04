"""empty message

Revision ID: d9954330492f
Revises: 50825a617918
Create Date: 2021-01-04 19:38:36.948824

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9954330492f'
down_revision = '50825a617918'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('skill',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('skill_type', sa.String(length=120), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('skill')
    # ### end Alembic commands ###