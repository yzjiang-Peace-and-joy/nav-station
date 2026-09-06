import json
from datetime import datetime
from pathlib import Path

from sqlalchemy import select

from .database import Base, SessionLocal, engine
from .models import PlazaCategory, PlazaSite, PlazaTag, User
from .security import hash_password

ROOT = Path(__file__).resolve().parents[2]


def ensure_user(db, username):
    user = db.scalar(select(User).where(User.username == username))
    if user:
        return user
    user = User(username=username, password_hash=hash_password("123456"))
    db.add(user)
    db.flush()
    return user


def seed_plaza_from_json(db, filename, created_by_user_id):
    if db.scalar(select(PlazaSite.id).limit(1)):
        return
    data = json.loads((ROOT / "src" / "data" / filename).read_text())
    now = datetime.utcnow()
    cats = {}
    for i, item in enumerate(data.get("categories", [])):
        cat = PlazaCategory(slug=item["id"], name=item["name"], sort_order=i, created_at=now)
        db.add(cat)
        cats[item["id"]] = cat
    tag_map = {}
    for name in data.get("tags", []):
        tag = PlazaTag(name=name)
        db.add(tag)
        tag_map[name] = tag
    db.flush()
    seen_urls = set()
    for item in data.get("sites", []):
        url = (item.get("url") or "").strip()
        if not url or url in seen_urls:
            continue
        seen_urls.add(url)
        site = PlazaSite(
            slug=item["id"],
            name=item["name"],
            url=url,
            desc=item.get("desc", ""),
            detail=item.get("detail", ""),
            category=cats.get(item.get("category")),
            status="published",
            created_by=created_by_user_id,
            updated_by=created_by_user_id,
            created_at=now,
            updated_at=now,
            tags=[tag_map[t] for t in item.get("tags", []) if t in tag_map],
        )
        db.add(site)


def main():
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        yzjiang = ensure_user(db, "yzjiang")
        ensure_user(db, "test")
        seed_plaza_from_json(db, "sites.json", yzjiang.id)
        db.commit()


if __name__ == "__main__":
    main()
