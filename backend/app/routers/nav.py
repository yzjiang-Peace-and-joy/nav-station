from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from ..database import get_db
from ..models import Category, PlazaSite, Site, Tag, User
from .auth import current_user
from .plaza import (
    STATUS_PUBLISHED,
    get_or_create_personal_category,
    get_or_create_personal_tags,
    get_or_create_plaza_category,
    get_or_create_plaza_tags,
    normalize_url,
    serialize_personal_site,
    unique_personal_slug,
    unique_plaza_slug,
)

router = APIRouter(prefix="/api/nav", tags=["nav"])


class PersonalSitePayload(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    url: str = Field(min_length=1, max_length=1000)
    desc: str = ""
    detail: str = ""
    category: str | None = None
    tags: list[str] = Field(default_factory=list)
    publish_to_plaza: bool = False


@router.get("")
def nav(user=Depends(current_user), db: Session = Depends(get_db)):
    cats = db.scalars(select(Category).where(Category.user_id == user.id).order_by(Category.sort_order)).all()
    tags = db.scalars(select(Tag).where(Tag.user_id == user.id).order_by(Tag.id)).all()
    sites = db.scalars(
        select(Site)
        .options(selectinload(Site.tags), selectinload(Site.category), selectinload(Site.source_plaza))
        .where(Site.user_id == user.id)
        .order_by(Site.sort_order)
    ).all()
    return {
        "categories": [{"id": c.slug, "name": c.name} for c in cats],
        "tags": [t.name for t in tags],
        "sites": [serialize_personal_site(s) for s in sites],
    }


@router.post("/sites")
def create_personal_site(
    payload: PersonalSitePayload,
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
):
    url = normalize_url(payload.url)
    plaza = None
    if payload.publish_to_plaza:
        plaza = db.scalar(select(PlazaSite).where(PlazaSite.url == url))
        if plaza is None:
            plaza = PlazaSite(
                slug=unique_plaza_slug(db, payload.name),
                name=payload.name.strip(),
                url=url,
                desc=payload.desc or "",
                detail=payload.detail or "",
                category=get_or_create_plaza_category(db, payload.category),
                status=STATUS_PUBLISHED,
                created_by=user.id,
                updated_by=user.id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                tags=get_or_create_plaza_tags(db, payload.tags),
            )
            db.add(plaza)
            db.flush()
        existing = db.scalar(select(Site).where(Site.user_id == user.id, Site.source_plaza_site_id == plaza.id))
        if existing:
            raise HTTPException(409, "已添加到个人目录")

    category = get_or_create_personal_category(db, user, payload.category)
    max_order = db.scalar(select(func.max(Site.sort_order)).where(Site.user_id == user.id)) or 0
    site = Site(
        user_id=user.id,
        category=category,
        source_plaza_site_id=plaza.id if plaza else None,
        slug=unique_personal_slug(db, user.id, payload.name),
        name=payload.name.strip(),
        url=url,
        desc=payload.desc or "",
        detail=payload.detail or "",
        default_pinned=False,
        sort_order=max_order + 1,
        tags=get_or_create_personal_tags(db, user.id, payload.tags),
    )
    db.add(site)
    db.commit()
    site = db.scalar(
        select(Site)
        .options(selectinload(Site.tags), selectinload(Site.category), selectinload(Site.source_plaza))
        .where(Site.id == site.id)
    )
    return serialize_personal_site(site)


@router.post("/sites/{site_slug}/sync-from-plaza")
def sync_from_plaza(site_slug: str, user=Depends(current_user), db: Session = Depends(get_db)):
    site = db.scalar(
        select(Site)
        .options(selectinload(Site.tags), selectinload(Site.category), selectinload(Site.source_plaza))
        .where(Site.user_id == user.id, Site.slug == site_slug)
    )
    if not site:
        raise HTTPException(404, "站点不存在")
    if not site.source_plaza_site_id:
        raise HTTPException(400, "该站点不是从广场导入的")
    plaza = db.scalar(
        select(PlazaSite)
        .options(selectinload(PlazaSite.tags))
        .where(PlazaSite.id == site.source_plaza_site_id)
    )
    if not plaza or plaza.status != STATUS_PUBLISHED:
        raise HTTPException(400, "来源广场站点不可用")
    site.name = plaza.name
    site.url = plaza.url
    site.desc = plaza.desc
    site.detail = plaza.detail
    site.tags = get_or_create_personal_tags(db, user.id, [t.name for t in plaza.tags])
    db.commit()
    site = db.scalar(
        select(Site)
        .options(selectinload(Site.tags), selectinload(Site.category), selectinload(Site.source_plaza))
        .where(Site.id == site.id)
    )
    return serialize_personal_site(site)
