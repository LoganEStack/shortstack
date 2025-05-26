from app import create_app, db
from app.models import URL
from datetime import datetime

app = create_app()

with app.app_context():
    expired_urls = URL.query.filter(URL.expiration_date < datetime.utcnow()).all()
    for url in expired_urls:
        db.session.delete(url)
    db.session.commit()
    print(f"Deleted {len(expired_urls)} expired URLs.")
