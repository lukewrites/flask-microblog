"""empty message

Revision ID: 6836a69f78f
Revises: 4bdbb2deabda
Create Date: 2014-03-31 22:02:04.688129

"""

# revision identifiers, used by Alembic.
revision = '6836a69f78f'
down_revision = '4bdbb2deabda'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('author_id', sa.Integer(), nullable=True))
    op.drop_column('post', 'author')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('author', sa.INTEGER(), nullable=True))
    op.drop_column('post', 'author_id')
    ### end Alembic commands ###
