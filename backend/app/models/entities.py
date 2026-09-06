from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Index, Integer, String, Table, Text, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base

site_tags = Table(
    "site_tags", Base.metadata,
    Column("site_id", ForeignKey("sites.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)

plaza_site_tags = Table(
    "plaza_site_tags", Base.metadata,
    Column("plaza_site_id", ForeignKey("plaza_sites.id", ondelete="CASCADE"), primary_key=True),
    Column("plaza_tag_id", ForeignKey("plaza_tags.id", ondelete="CASCADE"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    categories: Mapped[list["Category"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    tags: Mapped[list["Tag"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    sites: Mapped[list["Site"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    pinned: Mapped[list["PinnedSite"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Category(Base):
    __tablename__ = "categories"
    __table_args__ = (UniqueConstraint("user_id", "slug"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    slug: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(200))
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    user: Mapped[User] = relationship(back_populates="categories")
    sites: Mapped[list["Site"]] = relationship(back_populates="category")


class Tag(Base):
    __tablename__ = "tags"
    __table_args__ = (UniqueConstraint("user_id", "name"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(100))
    user: Mapped[User] = relationship(back_populates="tags")
    sites: Mapped[list["Site"]] = relationship(secondary=site_tags, back_populates="tags")


class PlazaCategory(Base):
    __tablename__ = "plaza_categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(200))
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    sites: Mapped[list["PlazaSite"]] = relationship(back_populates="category")


class PlazaTag(Base):
    __tablename__ = "plaza_tags"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    sites: Mapped[list["PlazaSite"]] = relationship(secondary=plaza_site_tags, back_populates="tags")


class PlazaSite(Base):
    __tablename__ = "plaza_sites"
    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(200))
    url: Mapped[str] = mapped_column(String(1000), unique=True, index=True)
    desc: Mapped[str] = mapped_column(String(500), default="")
    detail: Mapped[str] = mapped_column(Text, default="")
    category_id: Mapped[int | None] = mapped_column(ForeignKey("plaza_categories.id"), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="published", index=True)
    created_by: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    updated_by: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    category: Mapped[PlazaCategory | None] = relationship(back_populates="sites")
    tags: Mapped[list[PlazaTag]] = relationship(secondary=plaza_site_tags, back_populates="sites")
    creator: Mapped[User | None] = relationship(foreign_keys=[created_by])
    updater: Mapped[User | None] = relationship(foreign_keys=[updated_by])


class Site(Base):
    __tablename__ = "sites"
    __table_args__ = (
        UniqueConstraint("user_id", "slug"),
        Index(
            "uq_sites_user_source_plaza",
            "user_id",
            "source_plaza_site_id",
            unique=True,
            sqlite_where=text("source_plaza_site_id IS NOT NULL"),
            postgresql_where=text("source_plaza_site_id IS NOT NULL"),
        ),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"), nullable=True)
    source_plaza_site_id: Mapped[int | None] = mapped_column(
        ForeignKey("plaza_sites.id", ondelete="SET NULL"), nullable=True
    )
    slug: Mapped[str] = mapped_column(String(150))
    name: Mapped[str] = mapped_column(String(200))
    url: Mapped[str] = mapped_column(String(1000))
    desc: Mapped[str] = mapped_column(String(500), default="")
    detail: Mapped[str] = mapped_column(Text, default="")
    default_pinned: Mapped[bool] = mapped_column(Boolean, default=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    user: Mapped[User] = relationship(back_populates="sites")
    category: Mapped[Category | None] = relationship(back_populates="sites")
    source_plaza: Mapped[PlazaSite | None] = relationship()
    tags: Mapped[list[Tag]] = relationship(secondary=site_tags, back_populates="sites")


class PinnedSite(Base):
    __tablename__ = "user_pinned_sites"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    site_id: Mapped[int] = mapped_column(ForeignKey("sites.id", ondelete="CASCADE"), primary_key=True)
    user: Mapped[User] = relationship(back_populates="pinned")
    site: Mapped[Site] = relationship()
