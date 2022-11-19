"""Initial

Revision ID: 7e0f6553a455
Revises: 
Create Date: 2022-11-12 17:44:37.700076

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7e0f6553a455'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('history',
    sa.Column('telegram_id', sa.BigInteger(), nullable=False),
    sa.Column('record_id', postgresql.UUID(), nullable=False),
    sa.Column('check_in', sa.Date(), nullable=False),
    sa.Column('check_out', sa.Date(), nullable=False),
    sa.Column('city', sa.String(), nullable=False),
    sa.Column('command', sa.String(), nullable=False),
    sa.Column('date_time', sa.DateTime(), nullable=False),
    sa.Column('distance', sa.Integer(), nullable=True),
    sa.Column('error', sa.Boolean(), nullable=False),
    sa.Column('period', sa.Integer(), nullable=False),
    sa.Column('price_max', sa.Integer(), nullable=True),
    sa.Column('price_min', sa.Integer(), nullable=True),
    sa.Column('quantity_display', sa.Integer(), nullable=False),
    sa.Column('quantity_photo', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('record_id')
    )
    op.create_index(op.f('ix_history_telegram_id'), 'history', ['telegram_id'], unique=False)
    op.create_table('photo',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('hotel_id', sa.BigInteger(), nullable=False),
    sa.Column('photo', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_photo_hotel_id'), 'photo', ['hotel_id'], unique=False)
    op.create_table('hotels',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('history_id', postgresql.UUID(), nullable=False),
    sa.Column('hotel_id', sa.BigInteger(), nullable=False),
    sa.Column('center', sa.Numeric(), nullable=False),
    sa.Column('coordinates', sa.String(), nullable=False),
    sa.Column('adress', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('price', sa.Numeric(), nullable=False),
    sa.Column('star_rates', sa.Numeric(), nullable=True),
    sa.Column('user_rates', sa.Numeric(), nullable=True),
    sa.ForeignKeyConstraint(['history_id'], ['history.record_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_hotels_history_id'), 'hotels', ['history_id'], unique=False)
    op.create_index(op.f('ix_hotels_hotel_id'), 'hotels', ['hotel_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_hotels_hotel_id'), table_name='hotels')
    op.drop_index(op.f('ix_hotels_history_id'), table_name='hotels')
    op.drop_table('hotels')
    op.drop_index(op.f('ix_photo_hotel_id'), table_name='photo')
    op.drop_table('photo')
    op.drop_index(op.f('ix_history_telegram_id'), table_name='history')
    op.drop_table('history')
    # ### end Alembic commands ###