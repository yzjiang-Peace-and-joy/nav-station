from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from ..database import get_db
from ..models import Category, PlazaSite, Site, Tag
from .auth import current_user
from .plaza import STATUS_PUBLISHED, get_or_create_personal_tags, serialize_personal_site

router = APIRouter(prefix="/api/nav", tags=["nav"])


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
