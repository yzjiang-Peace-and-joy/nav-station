from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from ..database import get_db
from ..models import Category, Site, Tag
from .auth import current_user

router = APIRouter(prefix="/api/nav", tags=["nav"])

@router.get("")
def nav(user=Depends(current_user), db: Session = Depends(get_db)):
    cats = db.scalars(select(Category).where(Category.user_id == user.id).order_by(Category.sort_order)).all()
    tags = db.scalars(select(Tag).where(Tag.user_id == user.id).order_by(Tag.id)).all()
    sites = db.scalars(select(Site).options(selectinload(Site.tags), selectinload(Site.category)).where(Site.user_id == user.id).order_by(Site.sort_order)).all()
    return {"categories": [{"id": c.slug, "name": c.name} for c in cats], "tags": [t.name for t in tags], "sites": [{"id": s.slug, "name": s.name, "url": s.url, "desc": s.desc, "detail": s.detail, "category": s.category.slug if s.category else "__uncategorized", "tags": [t.name for t in s.tags], "pinned": s.default_pinned} for s in sites]}
