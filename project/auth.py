import jwt
from flask import request, jsonify
from functools import wraps
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash
from db import mongo  # Import de MongoDB depuis db.py

# Clé secrète pour signer les tokens JWT
SECRET_KEY = "super-secret-key"

# Décorateur pour protéger les routes avec JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({"message": "Unauthorized"}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = data['user']
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401
        return f(current_user, *args, **kwargs)
    return decorated

# Fonction pour générer un token JWT
def generate_token(user):
    payload = {
        'user': user,
        'exp': datetime.utcnow() + timedelta(hours=1)  # Token expire après 1 heure
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# Fonction d'authentification
def authenticate(username, password):
    # Recherche de l'utilisateur dans la base MongoDB
    user = mongo.db.users.find_one({"username": username})
    
    if user and check_password_hash(user['password'], password):
        # Si l'authentification réussit, on génère un token JWT avec les infos utilisateur
        return generate_token({"username": username})
    
    # Retourne None si l'utilisateur n'existe pas ou si le mot de passe est incorrect
    return None
