from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.model_user import User
from flask_app.models.model_recipe import Recipe

@app.route('/recipes/')
def recipe_new():
    data = {
        'id': id #'id' is the keyname which must match the name of the keyname passed in the classmethod the second id is the variable from def dojo_delete
    }
    all_users = User.get_all()
    recipe = Recipe.get_one(data)
    user_id_from_session = {
        'id':session["uuid"]
    } 
    user = User.get_one(user_id_from_session)
    return render_template('recipe_create.html', all_users=all_users, recipe=recipe, user=user)

@app.route('/recipe/create', methods=['post'])
def create_recipe():
    data = {**request.form, # this is a data dictionary that is taking in request.form, user_id and pulling this user_id from session 
            "user_id":session["uuid"] 
    }
    if Recipe.validate_recipe(data):
        Recipe.create(data)
        return redirect('/')
    return redirect('/')

@app.route('/recipe/<int:id>')
def recipe_show(id):
    data = {
        'id': id #'id' is the keyname which must match the name of the keyname passed in the classmethod the second id is the variable from def dojo_delete
    }
    recipe = recipe.get_one(data)
    user_id_from_session = {
        'id':session["uuid"]
    } 
    user = User.get_one(user_id_from_session)
    return render_template('show_recipe.html', recipe=recipe, user=user)

@app.route('/recipe/<int:id>/edit/')
def recipe_edit(id):
    data = {
        'id': id #'id' is the keyname which must match the name of the keyname passed in the classmethod the second id is the variable from def dojo_delete
    }
    recipe = Recipe.get_one(data)
    user_id_from_session = {
        'id':session["uuid"]
    } 
    user = User.get_one(user_id_from_session)
    
    return render_template('recipe_edit.html', recipe=recipe, user=user)

@app.route('/recipe/<int:id>/update/', methods=['post'])
def recipe_update(id):
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/recipe/{id}/edit')
    Recipe.update(request.form)
    return redirect('/dashboard')

@app.route('/recipe/<int:id>/delete')
def recipe_delete(id):
    data = {
        'id': id #'id' is the keyname which must match the name of the keyname passed in the classmethod the second id is the variable from def dojo_delete
    }
    Recipe.delete_one(data) # instead of doing the above you can pass dictionary directly in here Dojo.delete_one({'id': id})
    return redirect('/dashboard')
