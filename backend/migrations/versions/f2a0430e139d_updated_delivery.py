"""updated delivery

Revision ID: f2a0430e139d
Revises: aa54e6a49c55
Create Date: 2021-09-21 14:00:13.330137

"""
from alembic import op
import sqlalchemy as sa
import dbo_models


# revision identifiers, used by Alembic.
revision = 'f2a0430e139d'
down_revision = 'aa54e6a49c55'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pickup',
    sa.Column('time', sa.DateTime(timezone=True), nullable=False),
    sa.Column('merchant_id', dbo_models._helper.GUID(), nullable=False),
    sa.Column('id', dbo_models._helper.GUID(), nullable=False),
    sa.ForeignKeyConstraint(['merchant_id'], ['merchant.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('delivery',
    sa.Column('fee', sa.Float(), nullable=False),
    sa.Column('pick_up_id', dbo_models._helper.GUID(), nullable=True),
    sa.Column('delivery_type', sa.VARCHAR(length=50), nullable=False),
    sa.Column('order_id', dbo_models._helper.GUID(), nullable=True),
    sa.Column('id', dbo_models._helper.GUID(), nullable=False),
    sa.Column('created_time', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], ),
    sa.ForeignKeyConstraint(['pick_up_id'], ['pickup.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('delivery')
    op.drop_table('pickup')
    # ### end Alembic commands ###