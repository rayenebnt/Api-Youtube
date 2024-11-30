from flask import Flask, jsonify, request
from flask_restful import Api
from auth import token_required, authenticate  # Gestion de l'authentification
from db import mongo, init_app  # Initialisation de MongoDB
from werkzeug.security import generate_password_hash
from models import UserSchema, VideoSchema, CommentSchema  # Importer les schémas Marshmallow
from bson import ObjectId  # Pour manipuler les ObjectId dans MongoDB
from datetime import datetime

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/ytb"
app.secret_key = "super-secret-key"

# Initialisation de MongoDB
init_app(app)

api = Api(app)

# Initialisation des schémas Marshmallow
user_schema = UserSchema()
video_schema = VideoSchema()
comment_schema = CommentSchema()


# Fonction pour sérialiser une vidéo avec son ID
def serialize_video(video):
    video_data = video_schema.dump(video)
    video_data['id'] = str(video['_id'])  # Inclure l'ID comme string
    return video_data


# Route d'inscription (signup)
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Vérifier si l'utilisateur existe déjà
    if mongo.db.users.find_one({"username": username}):
        return jsonify({"message": "User already exists"}), 400

    # Hash du mot de passe pour plus de sécurité
    hashed_password = generate_password_hash(password)

    # Créer l'utilisateur
    new_user = {
        "username": username,
        "password": hashed_password,
        "created_at": datetime.utcnow()
    }
    mongo.db.users.insert_one(new_user)

    # Utiliser Marshmallow pour sérialiser l'utilisateur
    user_data = user_schema.dump(new_user)
    return jsonify(user_data), 201


# Route de connexion (login)
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Appel à la fonction authenticate pour vérifier les informations d'identification
    token = authenticate(username, password)
    if token:
        return jsonify({"token": token}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401


# Route pour poster une vidéo
@app.route('/videos', methods=['POST'])
@token_required
def post_video(current_user):
    data = request.get_json()
    source = data.get('source')
    formats = data.get('formats', {})

    if not source:
        return jsonify({"message": "Video source is required"}), 400

    # Créer la vidéo
    new_video = {
        "source": source,
        "created_at": datetime.utcnow(),
        "views": 0,
        "enabled": True,
        "user": current_user,
        "format": formats
    }

    # Insérer la vidéo et récupérer l'ID
    video_id = mongo.db.videos.insert_one(new_video).inserted_id
    new_video['_id'] = video_id

    # Sérialiser la vidéo avec l'ID inclus
    return jsonify(serialize_video(new_video)), 201


# Route pour récupérer une vidéo par ID
@app.route('/videos/<string:video_id>', methods=['GET'])
def get_video(video_id):
    video = mongo.db.videos.find_one({"_id": ObjectId(video_id)})
    if not video:
        return jsonify({"message": "Video not found"}), 404

    return jsonify(serialize_video(video))


# Route pour récupérer les vidéos postées par l'utilisateur connecté
@app.route('/my_videos', methods=['GET'])
@token_required
def get_my_videos(current_user):
    videos = mongo.db.videos.find({"user.username": current_user['username']})
    video_data = [serialize_video(video) for video in videos]
    return jsonify(video_data), 200


# Route pour poster un commentaire sur une vidéo
@app.route('/videos/<string:video_id>/comments', methods=['POST'])
@token_required
def post_comment(current_user, video_id):
    video = mongo.db.videos.find_one({"_id": ObjectId(video_id)})
    if not video:
        return jsonify({"message": "Video not found"}), 404

    data = request.get_json()
    body = data.get('body')

    if not body:
        return jsonify({"message": "Comment body is required"}), 400

    new_comment = {
        "body": body,
        "user": current_user,
        "created_at": datetime.utcnow(),
        "video_id": ObjectId(video_id)
    }
    mongo.db.comments.insert_one(new_comment)

    comment_data = comment_schema.dump(new_comment)
    return jsonify(comment_data), 201


# Route pour récupérer les commentaires d'une vidéo
@app.route('/videos/<string:video_id>/comments', methods=['GET'])
def get_comments(video_id):
    comments = mongo.db.comments.find({"video_id": ObjectId(video_id)})
    return jsonify([comment_schema.dump(comment) for comment in comments])


if __name__ == "__main__":
    app.run(debug=True)
