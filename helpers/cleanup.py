from datetime import datetime
from database.db import db
from models.blacklist import Blacklist

def Cleanup(app):
    with app.app_context():
        expired_tokens = Blacklist.query.filter(Blacklist.expired_at < datetime.now()).all()
        for token in expired_tokens:
            db.session.delete(token)
        db.session.commit()
        print("Cleanup completed")
