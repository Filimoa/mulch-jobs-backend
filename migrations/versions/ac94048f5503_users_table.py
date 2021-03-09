"""users table

Revision ID: ac94048f5503
Revises: 
Create Date: 2020-11-26 23:10:34.968198

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ac94048f5503'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('job_type')
    op.drop_table('mulch_job')
    op.drop_table('user')
    op.drop_table('grass_job')
    op.drop_table('estimate')
    op.drop_table('mulch_form_response')
    op.drop_table('form_info')
    op.drop_table('job')
    op.drop_table('mulch_estimate')
    op.drop_table('edge_form_response')
    op.drop_table('mulch_job_config')
    op.drop_table('form_response')
    op.drop_table('config')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('config',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('config_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('job_type', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('userID', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('hourly_wage', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('gross_profit_target', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('manager_hourly_wage', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['job_type'], ['job_type.name'], name='config_job_type_fkey'),
    sa.ForeignKeyConstraint(['userID'], ['user.userID'], name='config_userID_fkey'),
    sa.PrimaryKeyConstraint('id', name='config_pkey'),
    sa.UniqueConstraint('job_type', 'userID', name='config_job_type_userID_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('form_response',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('user_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('address', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('timestamp', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.Column('time_start', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('time_end', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('num_ppl', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('job_difficulty', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('notes', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('crew_lead', sa.VARCHAR(length=40), autoincrement=False, nullable=True),
    sa.Column('is_job_done', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('type', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('url_id', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
    sa.Column('job_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['url_id'], ['form_info.url_id'], name='form_response_url_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='form_response_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('mulch_job_config',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('wheelbarrows_in_yd', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('mulch_cost_per_yd', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('revenue_per_yd', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('revenue_per_ft', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('edge_form_url_id', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.Column('mulch_form_url_id', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['edge_form_url_id'], ['form_info.url_id'], name='mulch_job_config_edge_form_url_id_fkey'),
    sa.ForeignKeyConstraint(['id'], ['config.id'], name='mulch_job_config_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['mulch_form_url_id'], ['form_info.url_id'], name='mulch_job_config_mulch_form_url_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='mulch_job_config_pkey')
    )
    op.create_table('edge_form_response',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('sprinklers_hit', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('sprinklers_unfixed', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('is_cable_cut', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['id'], ['form_response.id'], name='edge_form_response_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='edge_form_response_pkey')
    )
    op.create_table('mulch_estimate',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('yds', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('ft', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['id'], ['estimate.id'], name='mulch_estimate_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='mulch_estimate_pkey')
    )
    op.create_table('job',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('job_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('address', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('price', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('man_hours', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('labour_cost', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('material_cost', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('cost', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('gross_profit', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('gross_profit_pct', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('suggested_price', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('type', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('userID', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['type'], ['job_type.name'], name='job_type_fkey'),
    sa.ForeignKeyConstraint(['userID'], ['user.userID'], name='job_userID_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='job_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('form_info',
    sa.Column('url_id', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('job_type', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('userID', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['job_type'], ['job_type.name'], name='form_info_job_type_fkey'),
    sa.ForeignKeyConstraint(['userID'], ['user.userID'], name='form_info_userID_fkey'),
    sa.PrimaryKeyConstraint('url_id', name='form_info_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('mulch_form_response',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('wheelbarrows', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['id'], ['form_response.id'], name='mulch_form_response_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='mulch_form_response_pkey')
    )
    op.create_table('estimate',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('address', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('price', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('note', sa.VARCHAR(length=1000), autoincrement=False, nullable=True),
    sa.Column('job_type', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('job_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('userID', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['job_type'], ['job_type.name'], name='estimate_job_type_fkey'),
    sa.PrimaryKeyConstraint('id', name='estimate_pkey')
    )
    op.create_table('grass_job',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('address', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('price', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('man_hours', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('labour_cost', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('material_cost', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('cost', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('gross_profit', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('gross_profit_pct', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('suggested_price', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('finish_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('userID', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('job_type', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['job_type'], ['job_type.name'], name='grass_job_job_type_fkey'),
    sa.PrimaryKeyConstraint('id', name='grass_job_pkey')
    )
    op.create_table('user',
    sa.Column('userID', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('company_name', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('userID', name='user_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('mulch_job',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('revenue_estimate', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('ft', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('yds_est', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('yds_used', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('yds_extra', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('mulch_crew_labour_cost', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('edge_crew_labour_cost', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('cost_per_yd', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('cost_per_ft', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('sprinklers_hit', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('sprinklers_unfixed', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('is_cable_cut', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('finish_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('crew_lead_edge', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('crew_lead_mulch', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['id'], ['job.id'], name='mulch_job_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='mulch_job_pkey')
    )
    op.create_table('job_type',
    sa.Column('name', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('reccurring', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.UniqueConstraint('name', name='job_type_name_key')
    )
    # ### end Alembic commands ###
