"""empty message

Revision ID: 4fb92f3ede9e
Revises: 2b269c4557de
Create Date: 2014-03-14 12:12:41.912515

"""

# revision identifiers, used by Alembic.
revision = '4fb92f3ede9e'
down_revision = '2b269c4557de'

from alembic import op
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('permission',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('reader', sa.Boolean(), nullable=True),
    sa.Column('editor', sa.Boolean(), nullable=True),
    sa.Column('admin', sa.Boolean(), nullable=True),
    sa.Column('account_id', sa.Integer(), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['account_id'], ['account.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    #op.drop_table('role')
    ### end Alembic commands ###

    projects = sa.sql.table('project',
        sa.sql.column('id', sa.Integer),
        sa.sql.column('author_id', sa.Integer)
    )

    perms = sa.sql.table('permission',
        sa.sql.column('project_id', sa.Integer),
        sa.sql.column('account_id', sa.Integer),
        sa.sql.column('reader', sa.Boolean),
        sa.sql.column('editor', sa.Boolean),
        sa.sql.column('admin', sa.Boolean),
        sa.sql.column('created_at', sa.DateTime),
        sa.sql.column('updated_at', sa.DateTime)
    )
    
    
    connection = op.get_bind()
    rp = connection.execute(projects.select())

    perm_seed = []
    for row in rp.fetchall():
        row = dict(zip(row.keys(), tuple(row)))
        perm_seed.append({
            'account_id': row.get('author_id'),
            'project_id': row.get('id'),
            'admin': True,
            'reader': True,
            'editor': True,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
            })

    op.bulk_insert(perms, perm_seed)


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('permission')
    ### end Alembic commands ###
