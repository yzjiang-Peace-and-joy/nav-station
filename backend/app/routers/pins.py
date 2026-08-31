from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import PinnedSite, Site
from .auth import current_user

router = APIRouter(prefix="/api/pins", tags=["pins"])
class PinsPayload(BaseModel): site_ids: list[str]

def get_pins(user, db):
    rows = db.scalars(select(PinnedSite).where(PinnedSite.user_id == user.id)).all()
    return [row.site.slug for row in rows if row.site]

def ensure_pins(user, db):
    if db.scalar(select(PinnedSite).where(PinnedSite.user_id == user.id)) is None:
        defaults = db.scalars(select(Site).where(Site.user_id == user.id, Site.default_pinned.is_(True))).all()
        db.add_all([PinnedSite(user_id=user.id, site_id=s.id) for s in defaults]); db.commit()

@router.get("")
def list_pins(user=Depends(current_user), db: Session = Depends(get_db)):
    ensure_pins(user, db); return {"site_ids": get_pins(user, db)}

@router.put("")
def replace_pins(payload: PinsPayload, user=Depends(current_user), db: Session = Depends(get_db)):
    sites = db.scalars(select(Site).where(Site.user_id == user.id, Site.slug.in_(set(payload.site_ids)))).all()
    db.execute(delete(PinnedSite).where(PinnedSite.user_id == user.id))
    db.add_all([PinnedSite(user_id=user.id, site_id=s.id) for s in sites]); db.commit()
    return {"site_ids": get_pins(user, db)}

@router.post("/{site_id}/toggle")
def toggle(site_id: str, user=Depends(current_user), db: Session = Depends(get_db)):
    site = db.scalar(select(Site).where(Site.user_id == user.id, Site.slug == site_id))
    if not site: raise HTTPException(404, "站点不存在")
    row = db.get(PinnedSite, (user.id, site.id))
    if row: db.delete(row)
    else: db.add(PinnedSite(user_id=user.id, site_id=site.id))
    db.commit(); return {"site_ids": get_pins(user, db)}
