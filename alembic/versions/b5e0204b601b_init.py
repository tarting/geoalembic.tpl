"""init

Revision ID: b5e0204b601b
Revises: 
Create Date: 2024-04-11 23:27:02.285434

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import geoalchemy2
from geoalchemy2 import Geometry

# revision identifiers, used by Alembic.
revision: str = 'b5e0204b601b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_geospatial_table('projects',
    sa.Column('fid', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('geom', Geometry(geometry_type='POINT', srid=25832, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry', nullable=False), nullable=False),
    sa.PrimaryKeyConstraint('fid'),
    sa.UniqueConstraint('name')
    )
    op.create_geospatial_index('idx_projects_geom', 'projects', ['geom'], unique=False, postgresql_using='gist', postgresql_ops={})
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_geospatial_index('idx_projects_geom', table_name='projects', postgresql_using='gist', column_name='geom')
    op.drop_geospatial_table('projects')
    # ### end Alembic commands ###
