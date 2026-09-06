"""plaza schema and personal site source link"""
from alembic import op
import sqlalchemy as sa

revision = "0002_plaza"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "plaza_categories",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("slug", sa.String(100), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("sort_order", sa.Integer, server_default="0"),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.UniqueConstraint("slug"),
    )
    op.create_index("ix_plaza_categories_slug", "plaza_categories", ["slug"])

    op.create_table(
        "plaza_tags",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.UniqueConstraint("name"),
    )
    op.create_index("ix_plaza_tags_name", "plaza_tags", ["name"])

    op.create_table(
        "plaza_sites",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("slug", sa.String(150), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("url", sa.String(1000), nullable=False),
        sa.Column("desc", sa.String(500), server_default=""),
        sa.Column("detail", sa.Text, server_default=""),
        sa.Column("category_id", sa.Integer, sa.ForeignKey("plaza_categories.id"), nullable=True),
        sa.Column("status", sa.String(20), server_default="published", nullable=False),
        sa.Column("created_by", sa.Integer, sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("updated_by", sa.Integer, sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),
        sa.UniqueConstraint("slug"),
        sa.UniqueConstraint("url"),
    )
    op.create_index("ix_plaza_sites_slug", "plaza_sites", ["slug"])
    op.create_index("ix_plaza_sites_url", "plaza_sites", ["url"])
    op.create_index("ix_plaza_sites_status", "plaza_sites", ["status"])

    op.create_table(
        "plaza_site_tags",
        sa.Column("plaza_site_id", sa.Integer, sa.ForeignKey("plaza_sites.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("plaza_tag_id", sa.Integer, sa.ForeignKey("plaza_tags.id", ondelete="CASCADE"), primary_key=True),
    )

    with op.batch_alter_table("sites") as batch:
        batch.add_column(sa.Column("source_plaza_site_id", sa.Integer, sa.ForeignKey("plaza_sites.id", ondelete="SET NULL"), nullable=True))

    op.create_index(
        "uq_sites_user_source_plaza",
        "sites",
        ["user_id", "source_plaza_site_id"],
        unique=True,
        sqlite_where=sa.text("source_plaza_site_id IS NOT NULL"),
    )


def downgrade():
    op.drop_index("uq_sites_user_source_plaza", table_name="sites")
    with op.batch_alter_table("sites") as batch:
        batch.drop_column("source_plaza_site_id")
    op.drop_table("plaza_site_tags")
    op.drop_index("ix_plaza_sites_status", table_name="plaza_sites")
    op.drop_index("ix_plaza_sites_url", table_name="plaza_sites")
    op.drop_index("ix_plaza_sites_slug", table_name="plaza_sites")
    op.drop_table("plaza_sites")
    op.drop_index("ix_plaza_tags_name", table_name="plaza_tags")
    op.drop_table("plaza_tags")
    op.drop_index("ix_plaza_categories_slug", table_name="plaza_categories")
    op.drop_table("plaza_categories")
