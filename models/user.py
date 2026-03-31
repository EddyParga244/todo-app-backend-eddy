from datetime import datetime, timezone
from sqlalchemy import DateTime, String
from database.db import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(String(36), primary_key=True)
    email = db.Column(String(191), unique=True, nullable=False)
    password = db.Column(String(255))
    created_at = db.Column(DateTime, default=lambda: datetime.now(timezone.utc))