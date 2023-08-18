# import the app from flask_app
from flask_app import app

# import the classes from recipe.py
import flask_app.controllers.users
import flask_app.controllers.recipes


if __name__ == "__main__":
    app.run(debug=True)
