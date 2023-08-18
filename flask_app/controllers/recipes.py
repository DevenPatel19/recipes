from flask import redirect, render_template, request, session, flash
from flask_app import app
from flask_app.models.recipe import Recipe
from flask_app.models.user import User


@app.route("/recipes/all")
def index_recipe():
    """call the get all classmethod to get all recipes"""
    recipes = Recipe.get_all_recipes_with_creator()
    user = User.get_by_user_id(session["user_id"])
    print(recipes)
    return render_template("dashboard.html", user=user, recipes=recipes)


@app.route("/recipes/<int:recipe_id>")
def recipe_details(recipe_id):
    """Displays details of one recipe"""

    recipe = Recipe.get_one_with_creator({"id": recipe_id})
    user = User.get_by_user_id(session["user_id"])

    return render_template("details_recipe.html", user=user, recipe=recipe)


@app.get("/recipes/new")
def new_recipe():
    """Displays the new recipe form template"""
    user = User.get_by_user_id(session["user_id"])

    return render_template("create_recipe.html")


@app.post("/recipes/create")
def create_recipe():
    """Process the submitted form and creates a recipe."""

    if not Recipe.new_recipe_is_valid(request.form):
        return redirect("/recipes/new")

    user = User.get_by_user_id(session["user_id"])
    recipe_id = Recipe.create_recipe(request.form)

    return redirect(f"/recipes/{recipe_id}")


@app.get("/recipes/<int:recipe_id>/edit_recipe")
def edit_recipe(recipe_id):
    """Displays the edit recipe form template"""
    user = User.get_by_user_id(session["user_id"])
    recipe = Recipe.get_one(recipe_id)

    return render_template("edit_recipe.html", user=user, recipe=recipe)


@app.post("/recipes/<int:recipe_id>/update_recipe")
def update_recipe(recipe_id):
    """Processes the submitted edit form and updates a recipe."""

    if not Recipe.recipe_is_valid(request.form):
        return redirect(f"/recipes/{recipe_id}/edit_recipe")

    Recipe.update_recipe(request.form)
    return redirect(f"/recipes/{recipe_id}")


@app.post("/recipes/<int:recipe_id>/delete")
def delete_recipe(recipe_id):
    """Delete a recipe. Processes the delete recipe form."""

    Recipe.delete(recipe_id)
    return redirect("/recipes/all")
