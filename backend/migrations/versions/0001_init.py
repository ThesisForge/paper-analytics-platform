"""initial tables

Revision ID: 0001
Revises: 
Create Date: 2024-05-01
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'publications',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.Text(), nullable=False),
        sa.Column('abstract', sa.Text()),
        sa.Column('venue', sa.String(length=255)),
        sa.Column('categories', postgresql.ARRAY(sa.String()), default=list),
        sa.Column('arxiv_id', sa.String(length=50), unique=True),
        sa.Column('doi', sa.String(length=255), unique=True),
        sa.Column('source', sa.String(length=50), nullable=False),
        sa.Column('url', sa.String(length=500)),
        sa.Column('published_at', sa.Date(), nullable=False),
        sa.Column('domain', sa.String(length=100), default='Other'),
        sa.Column('subtopics', postgresql.ARRAY(sa.String()), default=list),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        'authors',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False, unique=True)
    )

    op.create_table(
        'publication_authors',
        sa.Column('publication_id', sa.Integer(), sa.ForeignKey('publications.id'), primary_key=True),
        sa.Column('author_id', sa.Integer(), sa.ForeignKey('authors.id'), primary_key=True)
    )

    op.create_table(
        'raw_payloads',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('publication_id', sa.Integer(), sa.ForeignKey('publications.id'), nullable=False),
        sa.Column('source', sa.String(length=50), nullable=False),
        sa.Column('external_id', sa.String(length=255)),
        sa.Column('payload', postgresql.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        'ingestion_runs',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('source', sa.String(length=50), nullable=False),
        sa.Column('month', sa.String(length=7), nullable=False),
        sa.Column('status', sa.String(length=50), default='pending'),
        sa.Column('started_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('finished_at', sa.DateTime()),
        sa.Column('summary', postgresql.JSON(), default=dict),
        sa.UniqueConstraint('source', 'month', name='uq_source_month')
    )


def downgrade():
    op.drop_table('ingestion_runs')
    op.drop_table('raw_payloads')
    op.drop_table('publication_authors')
    op.drop_table('authors')
    op.drop_table('publications')
