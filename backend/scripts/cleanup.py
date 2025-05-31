from datetime import datetime, timezone
from app import create_app, db
from app.models import URL

app = create_app()

with app.app_context():
    now = datetime.now(timezone.utc)
    expired_urls = URL.query.filter(URL.expiration_date < now).all()
    for url in expired_urls:
        print(" - Deleting", url)
        db.session.delete(url)
    db.session.commit()
    print(f"Deleted {len(expired_urls)} expired URLs.")
