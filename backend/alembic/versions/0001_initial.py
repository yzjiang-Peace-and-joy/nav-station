"""initial schema"""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table("users", sa.Column("id", sa.Integer, primary_key=True), sa.Column("username", sa.String(100), nullable=False), sa.Column("password_hash", sa.String(255), nullable=False), sa.Column("created_at", sa.DateTime, nullable=False), sa.UniqueConstraint("username"))
    op.create_table("categories", sa.Column("id", sa.Integer, primary_key=True), sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE")), sa.Column("slug", sa.String(100)), sa.Column("name", sa.String(200)), sa.Column("sort_order", sa.Integer, server_default="0"), sa.UniqueConstraint("user_id", "slug"))
    op.create_table("tags", sa.Column("id", sa.Integer, primary_key=True), sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE")), sa.Column("name", sa.String(100)), sa.UniqueConstraint("user_id", "name"))
    op.create_table("sites", sa.Column("id", sa.Integer, primary_key=True), sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE")), sa.Column("category_id", sa.Integer, sa.ForeignKey("categories.id")), sa.Column("slug", sa.String(150)), sa.Column("name", sa.String(200)), sa.Column("url", sa.String(1000)), sa.Column("desc", sa.String(500), server_default=""), sa.Column("detail", sa.Text, server_default=""), sa.Column("default_pinned", sa.Boolean, server_default=sa.false()), sa.Column("sort_order", sa.Integer, server_default="0"), sa.UniqueConstraint("user_id", "slug"))
    op.create_table("site_tags", sa.Column("site_id", sa.Integer, sa.ForeignKey("sites.id", ondelete="CASCADE"), primary_key=True), sa.Column("tag_id", sa.Integer, sa.ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True))
    op.create_table("user_pinned_sites", sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True), sa.Column("site_id", sa.Integer, sa.ForeignKey("sites.id", ondelete="CASCADE"), primary_key=True))

def downgrade():
    for table in ("user_pinned_sites", "site_tags", "sites", "tags", "categories", "users"):
        op.drop_table(table)
