from bson import ObjectId
from datetime import datetime

def serialize_user(user, current_user=None):
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "pseudo": user["pseudo"],
        "created_at": user["created_at"].isoformat(),
        "email": user["email"] if current_user and current_user["_id"] == user["_id"] else None
    }

def create_user(username, pseudo, email):
    return {
        "username": username,
        "pseudo": pseudo,
        "email": email,
        "created_at": datetime.utcnow()
    }
