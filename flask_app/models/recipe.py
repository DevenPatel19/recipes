# import the function that will return an instance of a connection
from pprint import pprint
from flask import flash
from flask_app.config.mysql_connection import connect_to_mysql
from flask_app.models.user import User

DATABASE = "recipes_db"


def __repr__(self) -> str:
    return f"<Recipe: {self.name} {self.description}>"


# model the class after the recipe table from our database
class Recipe:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.instruction = data["instruction"]
        self.is_under_30 = data["is_under_30"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        # self.user = data["creator"]

    @staticmethod
    def recipe_is_valid(form_data):
        """Validates the recipe form"""

        is_valid = True

        if len(form_data["name"].strip()) == 0:
            is_valid = False
            flash("Please enter a name.", "update")
        elif len(form_data["name"].strip()) < 3:
            is_valid = False
            flash(
                "Please enter a name that is at least three characters long.", "update"
            )
        if len(form_data["description"].strip()) == 0:
            is_valid = False
            flash("Please enter a description.", "update")
        elif len(form_data["description"].strip()) < 3:
            is_valid = False
            flash("Description must be at least three characters.", "update")
        if len(form_data["instruction"].strip()) == 0:
            is_valid = False
            flash("Please enter instructions", "update")
        elif len(form_data["instruction"].strip()) < 3:
            is_valid = False
            flash("Instructions must be at least three characters.", "update")

        return is_valid

    @staticmethod
    def new_recipe_is_valid(form_data):
        """Validates the recipe form"""

        is_valid = True

        if len(form_data["name"].strip()) == 0:
            is_valid = False
            flash("Please enter a name.", "create_recipe")
        elif len(form_data["description"].strip()) < 3:
            is_valid = False
            flash("Description must be at least 3 characters.", "create_recipe")
        if len(form_data["description"].strip()) == 0:
            is_valid = False
            flash("Please enter instructions", "create_recipe")
        elif len(form_data["instruction"].strip()) < 2:
            is_valid = False
            flash("Instructions must be at least three characters.", "create_recipe")

        return is_valid

    # Create a New Recipe
    @classmethod
    def create_recipe(cls, form_data):
        """Creates a new Recipe row in the Recipe table"""

        query = """
        INSERT INTO recipes (name, description, instruction, is_under_30,user_id)
        VALUES (%(name)s,%(description)s,%(instruction)s,%(is_under_30)s, %(user_id)s)
        """

        recipe_id = connect_to_mysql(DATABASE).query_db(query, form_data)
        return recipe_id

    # Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connect_to_mysql(DATABASE).query_db(query)
        pprint(results)
        # Create an empty list to append our instances of recipes
        recipes = []
        # Iterate over the db results and create instances of recipes with cls.
        for dictionary in results:
            recipes.append(Recipe(dictionary))
        return recipes

    @classmethod
    def get_all_recipes_with_creator(cls):
        query = """
                SELECT * FROM recipes
                JOIN users
                ON recipes.user_id = users.id
                """
        results = connect_to_mysql(DATABASE).query_db(query)
        all_recipes = []  # create empty list to hold recipe objects
        if results:
            for row in results:
                recipe = cls(row)  # create recipe object
                creator_data = {
                    "id": row["users.id"],
                    "first_name": row["first_name"],
                    "last_name": row["last_name"],
                    "email": row["email"],
                    "password": row["password"],
                    "created_at": row["users.created_at"],
                    "updated_at": row["users.updated_at"],
                }
                recipe.creator = User(creator_data)  # create user object
                all_recipes.append(recipe)
        return all_recipes

    @classmethod
    def get_one(cls, recipe_id):
        query = """
        SELECT * FROM recipes
        WHERE id = %(recipe_id)s;
        """

        data = {"recipe_id": recipe_id}

        results = connect_to_mysql(DATABASE).query_db(query, data)
        recipe = Recipe(results[0])
        return recipe

    @classmethod
    def get_one_with_creator(cls, data):
        query = """
                SELECT * FROM recipes
                JOIN users 
                ON recipes.user_id = users.id
                WHERE recipes.id = %(id)s;
                """
        results = connect_to_mysql(DATABASE).query_db(query, data)
        if results:
            row = results[0]  # store the first row in a variable
            recipe = cls(row)  # create the recipe object
            creator_data = {
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": row["password"],
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"],
            }
            recipe.creator = User(creator_data)  # create the user object
            return recipe

    @classmethod
    def update_recipe(cls, form_data):
        """Update a row in the recipe table"""
        query = """
        UPDATE recipes
        SET name = %(name)s,  description = %(description)s, instruction = %(instruction)s, is_under_30 =  %(is_under_30)s
        WHERE id = %(recipe_id)s;
        """

        connect_to_mysql(DATABASE).query_db(query, form_data)
        return

    @classmethod
    def delete(cls, recipe_id):
        """Deletes one recipe in the recipe table"""

        query = "DELETE FROM recipes WHERE id = %(recipe_id)s;"

        data = {"recipe_id": recipe_id}

        connect_to_mysql(DATABASE).query_db(query, data)
        return
