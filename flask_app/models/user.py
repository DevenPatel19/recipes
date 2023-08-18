import re
from flask import flash
from flask_app.config.mysql_connection import connect_to_mysql

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")

DATABASE = "recipes_db"


class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @staticmethod
    def registration_is_valid(form_data):
        """Validates the registration form"""

        is_valid = True

        if len(form_data["first_name"].strip()) == 0:
            is_valid = False
            flash("Please enter first name.", "register")
        elif len(form_data["first_name"].strip()) < 2:
            is_valid = False
            flash("First name must be at least two characters.", "register")
        if len(form_data["last_name"].strip()) == 0:
            is_valid = False
            flash("Please enter last name.", "register")
        elif len(form_data["last_name"].strip()) < 2:
            is_valid = False
            flash("Last name must be at least two characters.", "register")
        if len(form_data["email"].strip()) == 0:
            is_valid = False
            flash("Please enter email.", "register")
        elif not EMAIL_REGEX.match(form_data["email"]):
            is_valid = False
            flash("Invalid email.", "register")
        if len(form_data["password"].strip()) == 0:
            is_valid = False
            flash("Please enter password.", "register")
        elif len(form_data["password"].strip()) < 8:
            is_valid = False
            flash("Password must be at least eight characters.", "register")
        elif len(form_data["confirm_password"].strip()) == 0:
            is_valid = False
            flash("Please confirm password.", "register")
        elif form_data["confirm_password"] != form_data["password"]:
            is_valid = False
            flash("Passwords do not match.", "register")

        return is_valid

    @staticmethod
    def login_is_valid(form_data):
        """Validates the login form"""

        is_valid = True

        if len(form_data["email"].strip()) == 0:
            is_valid = False
            flash("Please enter email.", "login")
        elif not EMAIL_REGEX.match(form_data["email"]):
            is_valid = False
            flash("Invalid email.", "login")

        if len(form_data["password"].strip()) == 0:
            is_valid = False
            flash("Please enter password.", "login")
        elif len(form_data["password"].strip()) < 8:
            is_valid = False
            flash("Password must be at least eight characters.", "login")
        return is_valid

    @classmethod
    def create(cls, data):
        """Create/Register a new user in the users table."""

        query = """
        INSERT INTO users (first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
        """

        user_id = connect_to_mysql(DATABASE).query_db(query, data)
        return user_id

    @classmethod
    def get_by_email(cls, email):
        """Finds a user by email address"""

        query = """
        SELECT * FROM users
        WHERE email = %(email)s;
        """

        data = {"email": email}

        results = connect_to_mysql(DATABASE).query_db(query, data)

        print(results)

        if len(results) < 1:
            return None

        else:
            return User(results[0])

    @classmethod
    def get_by_user_id(cls, user_id):
        """Finds a user by user_id address"""

        query = """
        SELECT * FROM users
        WHERE id = %(user_id)s;
        """

        data = {"user_id": user_id}

        results = connect_to_mysql(DATABASE).query_db(query, data)

        print(results)

        if len(results) < 1:
            return None

        else:
            return User(results[0])
