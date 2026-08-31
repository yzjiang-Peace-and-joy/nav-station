from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Table, Text, UniqueConstraint, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base

site_tags = Table(
    "site_tags", Base.metadata,
    Column("site_id", ForeignKey("sites.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
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


class Site(Base):
    __tablename__ = "sites"
    __table_args__ = (UniqueConstraint("user_id", "slug"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"), nullable=True)
    slug: Mapped[str] = mapped_column(String(150))
    name: Mapped[str] = mapped_column(String(200))
    url: Mapped[str] = mapped_column(String(1000))
    desc: Mapped[str] = mapped_column(String(500), default="")
    detail: Mapped[str] = mapped_column(Text, default="")
    default_pinned: Mapped[bool] = mapped_column(Boolean, default=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    user: Mapped[User] = relationship(back_populates="sites")
    category: Mapped[Category | None] = relationship(back_populates="sites")
    tags: Mapped[list[Tag]] = relationship(secondary=site_tags, back_populates="sites")


class PinnedSite(Base):
    __tablename__ = "user_pinned_sites"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    site_id: Mapped[int] = mapped_column(ForeignKey("sites.id", ondelete="CASCADE"), primary_key=True)
    user: Mapped[User] = relationship(back_populates="pinned")
    site: Mapped[Site] = relationship()
