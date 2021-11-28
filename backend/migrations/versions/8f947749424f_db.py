"""db

Revision ID: 8f947749424f
Revises: 
Create Date: 2021-07-10 23:19:00.475509

"""
from alembic import op
import sqlalchemy as sa
import dbo_models


# revision identifiers, used by Alembic.
# revision = '8f947749424f'
revision = '8f947749424f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('addongroup',
    sa.Column('name', sa.VARCHAR(length=100), nullable=False),
    sa.Column('max_quantity', sa.Integer(), nullable=True),
    sa.Column('min_quantity', sa.Integer(), nullable=True),
    sa.Column('id', dbo_models._helper.GUID(), nullable=False),
    sa.Column('created_time', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_time', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('category',
    sa.Column('name', sa.VARCHAR(length=100), nullable=False),
    sa.Column('index', sa.Integer(), nullable=True),
    sa.Column('id', dbo_models._helper.GUID(), nullable=False),
    sa.Column('created_time', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_time', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('addon',
    sa.Column('addon_group_id', dbo_models._helper.GUID(), nullable=False),
    sa.Column('id', dbo_models._helper.GUID(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), nullable=False),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('description', sa.VARCHAR(length=100), nullable=True),
    sa.Column('is_taxable', sa.Boolean(), nullable=False),
    sa.Column('created_time', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_time', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['addon_group_id'], ['addongroup.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_addon_addon_group_id'), 'addon', ['addon_group_id'], unique=False)
    op.create_table('menuitem',
    sa.Column('category_id', dbo_models._helper.GUID(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), nullable=False),
    sa.Column('description', sa.VARCHAR(length=100), nullable=True),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('image_url', sa.String(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('is_taxable', sa.Boolean(), nullable=False),
    sa.Column('size', sa.VARCHAR(length=100), nullable=False),
    sa.Column('tax_rate', sa.Float(), nullable=True),
    sa.Column('id', dbo_models._helper.GUID(), nullable=False),
    sa.Column('created_time', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_time', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_menuitem_category_id'), 'menuitem', ['category_id'], unique=False)
    op.create_table('menuitemtoaddongroup',
    sa.Column('menu_item_id', dbo_models._helper.GUID(), nullable=False),
    sa.Column('addon_group_id', dbo_models._helper.GUID(), nullable=False),
    sa.ForeignKeyConstraint(['addon_group_id'], ['addongroup.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['menu_item_id'], ['menuitem.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('menu_item_id', 'addon_group_id')
    )
    op.create_index(op.f('ix_menuitemtoaddongroup_addon_group_id'), 'menuitemtoaddongroup', ['addon_group_id'], unique=False)
    op.create_index(op.f('ix_menuitemtoaddongroup_menu_item_id'), 'menuitemtoaddongroup', ['menu_item_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_menuitemtoaddongroup_menu_item_id'), table_name='menuitemtoaddongroup')
    op.drop_index(op.f('ix_menuitemtoaddongroup_addon_group_id'), table_name='menuitemtoaddongroup')
    op.drop_table('menuitemtoaddongroup')
    op.drop_index(op.f('ix_menuitem_category_id'), table_name='menuitem')
    op.drop_table('menuitem')
    op.drop_index(op.f('ix_addon_addon_group_id'), table_name='addon')
    op.drop_table('addon')
    op.drop_table('category')
    op.drop_table('addongroup')
    # ### end Alembic commands ###
