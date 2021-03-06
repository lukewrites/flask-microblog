"""empty message

Revision ID: 2c04ccc25365
Revises: 32e258b9c17f
Create Date: 2014-03-25 23:08:08.196233

"""

# revision identifiers, used by Alembic.
revision = '2c04ccc25365'
down_revision = '32e258b9c17f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=80), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('author', sa.String(), nullable=True),
    sa.Column('pub_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('posts')
    ### end Alembic commands ###
