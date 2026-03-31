from sqlalchemy import DateTime, String
from database.db import db

class Blacklist(db.Model):
    __tablename__="blacklists"

    jti = db.Column(String(36), primary_key=True, nullable=False)
    expired_at = db.Column(DateTime)
