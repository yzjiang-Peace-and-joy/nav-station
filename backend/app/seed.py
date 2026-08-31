import json
from pathlib import Path
from sqlalchemy import select
from .database import Base, SessionLocal, engine
from .models import Category, Site, Tag, User
from .security import hash_password

ROOT = Path(__file__).resolve().parents[2]

def import_user(db, username, filename):
    user = db.scalar(select(User).where(User.username == username))
    if user: return
    data = json.loads((ROOT / "src" / "data" / filename).read_text())
    user = User(username=username, password_hash=hash_password("123456"))
    db.add(user); db.flush()
    cats = {}
    for i, item in enumerate(data.get("categories", [])):
        cat = Category(user_id=user.id, slug=item["id"], name=item["name"], sort_order=i)
        db.add(cat); cats[item["id"]] = cat
    tag_map = {}
    for name in data.get("tags", []):
        tag = Tag(user_id=user.id, name=name); db.add(tag); tag_map[name] = tag
    db.flush()
    for i, item in enumerate(data.get("sites", [])):
        site = Site(user_id=user.id, category=cats.get(item.get("category")), slug=item["id"], name=item["name"], url=item["url"], desc=item.get("desc", ""), detail=item.get("detail", ""), default_pinned=item.get("pinned", False), sort_order=i, tags=[tag_map[t] for t in item.get("tags", []) if t in tag_map])
        db.add(site)

def main():
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        import_user(db, "yzjiang", "sites.json")
        import_user(db, "test", "sites-test.json")
        db.commit()

if __name__ == "__main__": main()
