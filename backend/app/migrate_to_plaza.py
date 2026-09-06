"""One-shot: copy yzjiang personal sites into plaza, then clear personal nav for both users."""
from datetime import datetime

from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload

from .database import Base, SessionLocal, engine
from .models import (
    Category,
    PinnedSite,
    PlazaCategory,
    PlazaSite,
    PlazaTag,
    Site,
    Tag,
    User,
    plaza_site_tags,
    site_tags,
)


def clear_plaza(db):
    db.execute(delete(plaza_site_tags))
    db.execute(delete(PlazaSite))
    db.execute(delete(PlazaTag))
    db.execute(delete(PlazaCategory))
    db.flush()


def clear_user_nav(db, user_id: int):
    site_ids = list(db.scalars(select(Site.id).where(Site.user_id == user_id)).all())
    if site_ids:
        db.execute(delete(PinnedSite).where(PinnedSite.user_id == user_id))
        db.execute(delete(site_tags).where(site_tags.c.site_id.in_(site_ids)))
        db.execute(delete(Site).where(Site.user_id == user_id))
    db.execute(delete(Category).where(Category.user_id == user_id))
    db.execute(delete(Tag).where(Tag.user_id == user_id))
    db.flush()


def migrate_yzjiang_to_plaza(db):
    user = db.scalar(select(User).where(User.username == "yzjiang"))
    if not user:
        raise SystemExit("用户 yzjiang 不存在，无法迁移")

    cats = db.scalars(
        select(Category).where(Category.user_id == user.id).order_by(Category.sort_order, Category.id)
    ).all()
    plaza_cats = {}
    now = datetime.utcnow()
    for cat in cats:
        pc = PlazaCategory(slug=cat.slug, name=cat.name, sort_order=cat.sort_order, created_at=now)
        db.add(pc)
        plaza_cats[cat.id] = pc
    db.flush()

    tags = db.scalars(select(Tag).where(Tag.user_id == user.id).order_by(Tag.id)).all()
    plaza_tags = {}
    for tag in tags:
        pt = PlazaTag(name=tag.name)
        db.add(pt)
        plaza_tags[tag.id] = pt
    db.flush()

    sites = db.scalars(
        select(Site)
        .options(selectinload(Site.tags))
        .where(Site.user_id == user.id)
        .order_by(Site.sort_order, Site.id)
    ).all()
    seen_urls = set()
    seen_slugs = set()
    migrated = 0
    for site in sites:
        url = (site.url or "").strip()
        if not url or url in seen_urls:
            print(f"skip duplicate/empty url: {site.slug} -> {site.url}")
            continue
        slug = site.slug
        if slug in seen_slugs:
            base = slug
            i = 2
            while f"{base}-{i}" in seen_slugs:
                i += 1
            slug = f"{base}-{i}"
        seen_urls.add(url)
        seen_slugs.add(slug)
        ps = PlazaSite(
            slug=slug,
            name=site.name,
            url=url,
            desc=site.desc or "",
            detail=site.detail or "",
            category=plaza_cats.get(site.category_id) if site.category_id else None,
            status="published",
            created_by=user.id,
            updated_by=user.id,
            created_at=now,
            updated_at=now,
            tags=[plaza_tags[t.id] for t in site.tags if t.id in plaza_tags],
        )
        db.add(ps)
        migrated += 1
    db.flush()
    return migrated


def main():
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        clear_plaza(db)
        count = migrate_yzjiang_to_plaza(db)
        for username in ("yzjiang", "test"):
            user = db.scalar(select(User).where(User.username == username))
            if user:
                clear_user_nav(db, user.id)
                print(f"cleared personal nav for {username}")
        db.commit()
        print(f"migrated {count} sites from yzjiang into plaza")


if __name__ == "__main__":
    main()
