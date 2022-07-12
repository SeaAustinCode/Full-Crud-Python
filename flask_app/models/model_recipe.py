from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import model_user
from flask import flash, session

DATABASE = 'test_practice_db'

class Recipe:
    def __init__( self , data ):
        self.id = data['id'] #data in this is a dictionary --- data['id'] is how we are accessing the key of 'id' in the dictionary data and setting it to self.id
        self.description = data['description'] #DB Columns --> need a minimum of the number of columns in our DB
        self.instructions = data['instructions']
        self.date_made_on = data['date_made_on']
        self.under_30_mins = data['under_30_mins']
        self.rating = data['rating']
        self.user_id = data['user_id']
        self.created_at = data['created_at'] 
        self.updated_at = data['updated_at'] 
    # Now we use class methods to query our database
    
    @classmethod
    def create(cls, data:dict): 
        query = "INSERT INTO recipes (description, instructions, date_made_on, under_30_mins, rating, user_id) VALUES (%(description)s, %(instructions)s, %(date_made_on)s, %(under_30_mins)s, %(rating)s, %(user_id)s);" #write the query in the workbench to test it 
        # database request
        recipe_id = connectToMySQL(DATABASE).query_db(query,data) #Target DB HERE city_id is variable name --> because insert query it'll return ID # of the row inserted
        return recipe_id
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes LEFT JOIN users ON users.id = recipes.user_id;" # users is on the right side so that is why we need to update the keys before creating the user ojbect
        results = connectToMySQL(DATABASE).query_db(query) #THE RETURN IS A LIST OF DICTIONARIES
        all_recipes = [] #becomes a list of instances or could be called an object 
        for row in results: # this will be one dictionary in our list of dictionaries. 
            this_recipe = cls(row) #row is the name of our dictionary this_recipe = an object ---> create our this_recipe dictionary off 
            data = {
                **row,
                'id': row['users.id'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            user = model_user.User(data)
            this_recipe.user = user
            all_recipes.append(this_recipe) # put our this_recipe object into our all_recipes list 
        return all_recipes

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;" #adding a join here only adds data thats why it doesnt effect where it is currently in use
        result = connectToMySQL(DATABASE).query_db(query,data)
        if not result:
            return False # this stops it from trying to return a class instance of nothing.
        recipe = cls(result[0])
        return recipe

    @classmethod
    def get_one_user_and_its_recipes(cls, data):
        query = "SELECT * FROM users LEFT JOIN recipes ON users.id = recipes.user_id WHERE users.id = %(id)s;" #Select all from (table 1) left join (table 2) on (table 1 .id) = (table2.foreign key) where (table 1.id)
        result = connectToMySQL(DATABASE).query_db(query,data)

        user = cls(result[0])

        recipes = []
        for row in result:
            recipe_data = {
                **row,
                'id': row['recipes.id'],
                'created_at': row['recipes.created_at'],
                'updated_at': row['recipes.updated_at']
            }
            this_recipe = Recipe(recipe_data)
            recipes.append(this_recipe)
        user.recipes = recipes
        return user

    @classmethod
    def update(cls, data):
        query = """UPDATE recipes SET
                description=%(description)s,
                instructions=%(instructions)s,
                date_made_on=%(date_made_on)s,
                under_30_mins=%(under_30_mins)s,
                rating=%(recipe)s,
                updated_at=NOW()
                WHERE recipes.id = %(id)s;"""
        result = connectToMySQL(DATABASE).query_db(query,data)
        return result

    @classmethod
    def delete_one(cls, data): #data is the dictionary
        query = "DELETE FROM recipes WHERE id = %(id)s;"# id is the keyname of the dictionary
        return connectToMySQL(DATABASE).query_db(query,data) #THE RETURN IS NOTHING

    @staticmethod
    def validate_recipe(data:dict) -> bool:
        is_valid = True

        if len(data['description']) < 10:
            is_valid = False
            flash("Please write at least one sentence describing your dish.")

        if len(data['instructions']) < 10:
            is_valid = False
            flash("Please provide instructions on how you created your dish.")

        if len(data['date_made_on']) < 1: # only needs to be one because we are just checking if they filled this out
            is_valid = False
            flash("Please input a date when you made the dish.")

        if len(data['rating']) < 1:
            is_valid = False
            flash("Please provide your rating of the dish.")
        elif int(data['number_of_sasquatches']) < 1:
            is_valid = False
            flash("The minimum rating allowed is 1 out of 5")
        return is_valid


