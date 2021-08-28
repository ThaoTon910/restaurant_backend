"""2021 aug 25

Revision ID: 5cf83e20d692
Revises: c43b11d1301d
Create Date: 2021-08-25 16:54:58.014713

"""
from alembic import op
import sqlalchemy as sa
import dbo_models

# revision identifiers, used by Alembic.
revision = '5cf83e20d692'
down_revision = 'c43b11d1301d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('extrapercentageall',
    sa.Column('id', dbo_models._helper.GUID(), nullable=False),
    sa.Column('promotiontype_id', dbo_models._helper.GUID(), nullable=False),
    sa.Column('percent_off', sa.Float(), nullable=False),
    sa.Column('updated_time', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['promotiontype_id'], ['promotiontype.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_extrapercentageall_promotiontype_id'), 'extrapercentageall', ['promotiontype_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_extrapercentageall_promotiontype_id'), table_name='extrapercentageall')
    op.drop_table('extrapercentageall')
    # ### end Alembic commands ###
