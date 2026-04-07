from datetime import datetime, timezone
from flask import request
from flask_jwt_extended import decode_token, get_jwt
from database.db import db
from models.blacklist import Blacklist

def blacklist_tokens():
    # Get access token jti
    access_jti = get_jwt()['jti']
    expiration_access = datetime.fromtimestamp(get_jwt()['exp'], tz=timezone.utc)

    # Get refresh token jti from cookie
    refresh_cookie = request.cookies.get('refresh_token')
    if not refresh_cookie:
        raise ValueError("Refresh token cookie missing")
    refresh_token = decode_token(refresh_cookie)
    refresh_jti = refresh_token['jti']
    expiration_refresh = datetime.fromtimestamp(refresh_token['exp'], tz=timezone.utc)

    # Add tokens to blacklist
    blacklist_access = Blacklist(jti=access_jti, expired_at=expiration_access)
    blacklist_refresh = Blacklist(jti=refresh_jti, expired_at=expiration_refresh)
    db.session.add(blacklist_access)
    db.session.add(blacklist_refresh)
    db.session.commit()
