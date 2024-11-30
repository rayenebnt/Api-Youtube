from datetime import datetime
from models.user import serialize_user

def serialize_video(video, current_user=None):
    return {
        "id": str(video["_id"]),  # Assure-toi que l'ID est bien converti en string
        "source": video["source"],
        "created_at": video["created_at"].isoformat(),
        "views": video["views"],
        "enabled": video["enabled"],
        "user": serialize_user(video["user"], current_user),
        "format": video.get("format", {})
    }

def create_video(source, user, formats):
    return {
        "source": source,
        "created_at": datetime.utcnow(),
        "views": 0,
        "enabled": True,
        "user": user,
        "format": formats
    }
