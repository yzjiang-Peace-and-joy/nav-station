import re
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, selectinload

from ..database import get_db
from ..models import Category, PlazaCategory, PlazaSite, PlazaTag, Site, Tag, User
from .auth import current_user

router = APIRouter(prefix="/api/plaza", tags=["plaza"])

STATUS_PUBLISHED = "published"
STATUS_ARCHIVED = "archived"


class PlazaSitePayload(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    url: str = Field(min_length=1, max_length=1000)
    desc: str = ""
    detail: str = ""
    category: str | None = None
    tags: list[str] = Field(default_factory=list)


class AddToNavPayload(BaseModel):
    category: str | None = None


def normalize_url(url: str) -> str:
    value = url.strip()
    while value.endswith("/") and value.count("/") > 2:
        value = value[:-1]
    return value


def slugify(value: str, max_len: int = 140) -> str:
    text_value = value.strip().lower()
    text_value = re.sub(r"[^\w\u4e00-\u9fff]+", "-", text_value, flags=re.UNICODE)
    text_value = re.sub(r"-{2,}", "-", text_value).strip("-")
    if not text_value:
        text_value = "site"
    return text_value[:max_len]


def unique_plaza_slug(db: Session, base: str) -> str:
    candidate = slugify(base)
    if not db.scalar(select(PlazaSite.id).where(PlazaSite.slug == candidate)):
        return candidate
    for i in range(2, 1000):
        suffix = f"-{i}"
        candidate = f"{slugify(base, max_len=140 - len(suffix))}{suffix}"
        if not db.scalar(select(PlazaSite.id).where(PlazaSite.slug == candidate)):
            return candidate
    raise HTTPException(500, "无法生成唯一 slug")


def unique_personal_slug(db: Session, user_id: int, base: str) -> str:
    candidate = slugify(base)
    if not db.scalar(select(Site.id).where(Site.user_id == user_id, Site.slug == candidate)):
        return candidate
    for i in range(2, 1000):
        suffix = f"-{i}"
        candidate = f"{slugify(base, max_len=140 - len(suffix))}{suffix}"
        if not db.scalar(select(Site.id).where(Site.user_id == user_id, Site.slug == candidate)):
            return candidate
    raise HTTPException(500, "无法生成唯一 slug")


def get_or_create_plaza_category(db: Session, name_or_slug: str | None) -> PlazaCategory | None:
    if not name_or_slug or not name_or_slug.strip():
        return None
    raw = name_or_slug.strip()
    slug = slugify(raw, max_len=100)
    cat = db.scalar(select(PlazaCategory).where(or_(PlazaCategory.slug == slug, PlazaCategory.name == raw)))
    if cat:
        return cat
    max_order = db.scalar(select(func.max(PlazaCategory.sort_order))) or 0
    cat = PlazaCategory(slug=slug, name=raw, sort_order=max_order + 1)
    db.add(cat)
    db.flush()
    return cat


def get_or_create_plaza_tags(db: Session, names: list[str]) -> list[PlazaTag]:
    result = []
    for name in names:
        clean = name.strip()
        if not clean:
            continue
        tag = db.scalar(select(PlazaTag).where(PlazaTag.name == clean))
        if not tag:
            tag = PlazaTag(name=clean)
            db.add(tag)
            db.flush()
        result.append(tag)
    return result


def plaza_site_query():
    return select(PlazaSite).options(
        selectinload(PlazaSite.tags),
        selectinload(PlazaSite.category),
        selectinload(PlazaSite.creator),
        selectinload(PlazaSite.updater),
    )


def serialize_plaza_site(site: PlazaSite, added: bool = False) -> dict:
    return {
        "id": site.slug,
        "name": site.name,
        "url": site.url,
        "desc": site.desc,
        "detail": site.detail,
        "category": site.category.slug if site.category else None,
        "category_name": site.category.name if site.category else None,
        "tags": [t.name for t in site.tags],
        "status": site.status,
        "added": added,
        "created_by": site.creator.username if site.creator else None,
        "updated_by": site.updater.username if site.updater else None,
        "created_at": site.created_at.isoformat() if site.created_at else None,
        "updated_at": site.updated_at.isoformat() if site.updated_at else None,
    }


def serialize_personal_site(site: Site) -> dict:
    return {
        "id": site.slug,
        "name": site.name,
        "url": site.url,
        "desc": site.desc,
        "detail": site.detail,
        "category": site.category.slug if site.category else "__uncategorized",
        "tags": [t.name for t in site.tags],
        "pinned": site.default_pinned,
        "source_plaza_id": site.source_plaza.slug if site.source_plaza else None,
    }


def added_plaza_ids(db: Session, user_id: int) -> set[int]:
    rows = db.scalars(
        select(Site.source_plaza_site_id).where(
            Site.user_id == user_id,
            Site.source_plaza_site_id.is_not(None),
        )
    ).all()
    return set(rows)


def get_plaza_by_slug(db: Session, slug: str) -> PlazaSite:
    site = db.scalar(plaza_site_query().where(PlazaSite.slug == slug))
    if not site:
        raise HTTPException(404, "广场站点不存在")
    return site


def resolve_personal_category(
    db: Session,
    user: User,
    requested_slug: str | None,
    plaza_category: PlazaCategory | None,
) -> Category | None:
    if requested_slug and requested_slug != "__uncategorized":
        cat = db.scalar(select(Category).where(Category.user_id == user.id, Category.slug == requested_slug))
        if not cat:
            raise HTTPException(400, "个人分类不存在")
        return cat
    if requested_slug == "__uncategorized":
        return None
    if plaza_category:
        by_slug = db.scalar(select(Category).where(Category.user_id == user.id, Category.slug == plaza_category.slug))
        if by_slug:
            return by_slug
        by_name = db.scalar(select(Category).where(Category.user_id == user.id, Category.name == plaza_category.name))
        if by_name:
            return by_name
        max_order = db.scalar(select(func.max(Category.sort_order)).where(Category.user_id == user.id)) or 0
        cat = Category(
            user_id=user.id,
            slug=plaza_category.slug,
            name=plaza_category.name,
            sort_order=max_order + 1,
        )
        db.add(cat)
        db.flush()
        return cat
    return None


def get_or_create_personal_tags(db: Session, user_id: int, names: list[str]) -> list[Tag]:
    result = []
    for name in names:
        clean = name.strip()
        if not clean:
            continue
        tag = db.scalar(select(Tag).where(Tag.user_id == user_id, Tag.name == clean))
        if not tag:
            tag = Tag(user_id=user_id, name=clean)
            db.add(tag)
            db.flush()
        result.append(tag)
    return result


@router.get("/meta")
def plaza_meta(user: User = Depends(current_user), db: Session = Depends(get_db)):
    cats = db.scalars(select(PlazaCategory).order_by(PlazaCategory.sort_order, PlazaCategory.id)).all()
    tags = db.scalars(select(PlazaTag).order_by(PlazaTag.name)).all()
    return {
        "categories": [{"id": c.slug, "name": c.name} for c in cats],
        "tags": [t.name for t in tags],
    }


@router.get("")
def list_plaza(
    q: str | None = None,
    category: str | None = None,
    tag: str | None = None,
    include_archived: bool = Query(False),
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
):
    stmt = plaza_site_query()
    if not include_archived:
        stmt = stmt.where(PlazaSite.status == STATUS_PUBLISHED)
    if category:
        stmt = stmt.join(PlazaSite.category).where(PlazaCategory.slug == category)
    if tag:
        stmt = stmt.join(PlazaSite.tags).where(PlazaTag.name == tag)
    if q:
        like = f"%{q.strip()}%"
        stmt = stmt.where(
            or_(
                PlazaSite.name.ilike(like),
                PlazaSite.url.ilike(like),
                PlazaSite.desc.ilike(like),
                PlazaSite.detail.ilike(like),
            )
        )
    stmt = stmt.order_by(PlazaSite.updated_at.desc(), PlazaSite.id.desc())
    sites = db.scalars(stmt).unique().all()
    added = added_plaza_ids(db, user.id)
    cats = db.scalars(select(PlazaCategory).order_by(PlazaCategory.sort_order, PlazaCategory.id)).all()
    tags = db.scalars(select(PlazaTag).order_by(PlazaTag.name)).all()
    return {
        "categories": [{"id": c.slug, "name": c.name} for c in cats],
        "tags": [t.name for t in tags],
        "sites": [serialize_plaza_site(s, added=s.id in added) for s in sites],
    }


@router.post("")
def create_plaza_site(
    payload: PlazaSitePayload,
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
):
    url = normalize_url(payload.url)
    if db.scalar(select(PlazaSite.id).where(PlazaSite.url == url)):
        raise HTTPException(409, "该网址已在广场中")
    now = datetime.utcnow()
    site = PlazaSite(
        slug=unique_plaza_slug(db, payload.name),
        name=payload.name.strip(),
        url=url,
        desc=payload.desc or "",
        detail=payload.detail or "",
        category=get_or_create_plaza_category(db, payload.category),
        status=STATUS_PUBLISHED,
        created_by=user.id,
        updated_by=user.id,
        created_at=now,
        updated_at=now,
        tags=get_or_create_plaza_tags(db, payload.tags),
    )
    db.add(site)
    db.commit()
    site = get_plaza_by_slug(db, site.slug)
    return serialize_plaza_site(site, added=False)


@router.get("/{slug}")
def get_plaza_site(slug: str, user: User = Depends(current_user), db: Session = Depends(get_db)):
    site = get_plaza_by_slug(db, slug)
    added = site.id in added_plaza_ids(db, user.id)
    return serialize_plaza_site(site, added=added)


@router.put("/{slug}")
def update_plaza_site(
    slug: str,
    payload: PlazaSitePayload,
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
):
    site = get_plaza_by_slug(db, slug)
    url = normalize_url(payload.url)
    conflict = db.scalar(select(PlazaSite.id).where(PlazaSite.url == url, PlazaSite.id != site.id))
    if conflict:
        raise HTTPException(409, "该网址已在广场中")
    site.name = payload.name.strip()
    site.url = url
    site.desc = payload.desc or ""
    site.detail = payload.detail or ""
    site.category = get_or_create_plaza_category(db, payload.category)
    site.tags = get_or_create_plaza_tags(db, payload.tags)
    site.updated_by = user.id
    site.updated_at = datetime.utcnow()
    db.commit()
    site = get_plaza_by_slug(db, slug)
    added = site.id in added_plaza_ids(db, user.id)
    return serialize_plaza_site(site, added=added)


@router.post("/{slug}/archive")
def archive_plaza_site(slug: str, user: User = Depends(current_user), db: Session = Depends(get_db)):
    site = get_plaza_by_slug(db, slug)
    site.status = STATUS_ARCHIVED
    site.updated_by = user.id
    site.updated_at = datetime.utcnow()
    db.commit()
    site = get_plaza_by_slug(db, slug)
    added = site.id in added_plaza_ids(db, user.id)
    return serialize_plaza_site(site, added=added)


@router.post("/{slug}/restore")
def restore_plaza_site(slug: str, user: User = Depends(current_user), db: Session = Depends(get_db)):
    site = get_plaza_by_slug(db, slug)
    site.status = STATUS_PUBLISHED
    site.updated_by = user.id
    site.updated_at = datetime.utcnow()
    db.commit()
    site = get_plaza_by_slug(db, slug)
    added = site.id in added_plaza_ids(db, user.id)
    return serialize_plaza_site(site, added=added)


@router.post("/{slug}/add")
def add_plaza_to_nav(
    slug: str,
    payload: AddToNavPayload | None = None,
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
):
    payload = payload or AddToNavPayload()
    plaza = get_plaza_by_slug(db, slug)
    if plaza.status != STATUS_PUBLISHED:
        raise HTTPException(400, "已下架的广场站点不能添加")
    existing = db.scalar(
        select(Site).where(Site.user_id == user.id, Site.source_plaza_site_id == plaza.id)
    )
    if existing:
        raise HTTPException(409, "已添加到个人目录")
    category = resolve_personal_category(db, user, payload.category, plaza.category)
    max_order = db.scalar(select(func.max(Site.sort_order)).where(Site.user_id == user.id)) or 0
    site = Site(
        user_id=user.id,
        category=category,
        source_plaza_site_id=plaza.id,
        slug=unique_personal_slug(db, user.id, plaza.slug),
        name=plaza.name,
        url=plaza.url,
        desc=plaza.desc,
        detail=plaza.detail,
        default_pinned=False,
        sort_order=max_order + 1,
        tags=get_or_create_personal_tags(db, user.id, [t.name for t in plaza.tags]),
    )
    db.add(site)
    db.commit()
    site = db.scalar(
        select(Site)
        .options(selectinload(Site.tags), selectinload(Site.category), selectinload(Site.source_plaza))
        .where(Site.id == site.id)
    )
    return serialize_personal_site(site)
