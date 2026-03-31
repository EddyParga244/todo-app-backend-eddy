from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, Integer, String
from database.db import db

class Todo(db.Model):
    __tablename__ = "todos"

    id = db.Column(String(36), primary_key=True)
    user_id = db.Column(String(50), db.ForeignKey('users.id'), nullable=False)
    text = db.Column(String(255))
    completed = db.Column(Boolean, default=False)
    position = db.Column(Integer, default=0)
    created_at = db.Column(DateTime, default=lambda: datetime.now(timezone.utc))
