from flask_pymongo import PyMongo

mongo = PyMongo()  # Initialisation de l'objet MongoDB

def init_app(app):
    # Cette fonction initialise MongoDB avec Flask
    mongo.init_app(app)
