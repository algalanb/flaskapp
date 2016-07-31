
from flask import Flask
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config["MONGODB_SETINGS"] = {'DB': "flaskapp"}
app.config["SECRET_KEY"] = "KeepThisS3cr3t"

db = MongoEngine(app)

if __name__ == '__main__':
	app.run()

def register_blueprints(app):
    # Prevents circular imports
    from app.views import plates
    app.register_blueprint(plates)

register_blueprints(app)
