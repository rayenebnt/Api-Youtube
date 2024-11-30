from marshmallow import Schema, fields

# Modèle pour l'utilisateur
class UserSchema(Schema):
    id = fields.Str(required=True)  # Utilisation de Str pour l'id (ObjectId dans MongoDB)
    username = fields.Str(required=True)
    pseudo = fields.Str(required=True)
    created_at = fields.DateTime()
    email = fields.Email(required=False)

# Modèle pour les vidéos
class VideoSchema(Schema):
    id = fields.Str(required=True)  # Utilisation de Str pour l'id
    source = fields.Str(required=True)
    created_at = fields.DateTime()
    views = fields.Int(required=True)
    enabled = fields.Bool(required=True)
    user = fields.Nested(UserSchema)  # L'utilisateur est un objet imbriqué
    format = fields.Dict(keys=fields.Str(), values=fields.Str())  # Formats de vidéo sous forme de dictionnaire

# Modèle pour les commentaires
class CommentSchema(Schema):
    id = fields.Str(required=True)  # Utilisation de Str pour l'id
    body = fields.Str(required=True)
    user = fields.Nested(UserSchema)  # L'utilisateur est un objet imbriqué
