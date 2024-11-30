from datetime import datetime
from models.user import serialize_user

def serialize_comment(comment, current_user=None):
    return {
        "id": str(comment["_id"]),
        "body": comment["body"],
        "user": serialize_user(comment["user"], current_user)
    }

def create_comment(body, user):
    return {
        "body": body,
        "user": user,
        "created_at": datetime.utcnow()
    }
