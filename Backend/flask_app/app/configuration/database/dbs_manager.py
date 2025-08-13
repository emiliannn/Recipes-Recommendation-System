# database/mongodb.py
import datetime
from bson import ObjectId
import pymongo
import pandas as pd
import pymysql.cursors
import json

class DBS_MANAGER:
    def __init__(self, connection_string='mongodb://localhost:27017', database_name='rs_db5', mysql_connection_config=None):
            self.client = pymongo.MongoClient(connection_string)
            self.db = self.client[database_name]

            if mysql_connection_config is None:
                self.mysql_connection_config = {
                    'host': 'localhost',
                    'user': 'root',
                    'password': '',
                    'db': 'rs_db',
                    'charset': 'utf8mb4',
                    'cursorclass': pymysql.cursors.DictCursor
                }
            else:
                self.mysql_connection_config = mysql_connection_config

 

    def fetch_recipes_from_mongo(self):
        collection = self.db['recipes']
        return collection.find()

    def insert_recipes_into_mysql(self, recipes):
        connection = pymysql.connect(**self.mysql_connection_config)
        try:
            with connection.cursor() as cursor:
                for recipe in recipes:
                    sql = """
                    INSERT INTO recipes (recipe_id, name, minutes, submitted, tags, nutrition, n_steps, steps, description, ingredients, n_ingredients)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        name = VALUES(name),
                        minutes = VALUES(minutes),
                        submitted = VALUES(submitted),
                        tags = VALUES(tags),
                        nutrition = VALUES(nutrition),
                        n_steps = VALUES(n_steps),
                        steps = VALUES(steps),
                        description = VALUES(description),
                        ingredients = VALUES(ingredients),
                        n_ingredients = VALUES(n_ingredients),
                        updated_at = CURRENT_TIMESTAMP
                    """
                    cursor.execute(sql, (
                        str(recipe['_id']),
                        recipe.get('name', ''),
                        recipe.get('minutes', 0),
                        recipe.get('submitted', None),
                        recipe.get('tags', ''),
                        json.dumps(recipe.get('nutrition', [])),
                        recipe.get('n_steps', 0),
                        json.dumps(recipe.get('steps', [])),
                        recipe.get('description', ''),
                        recipe.get('ingredients', ''),
                        recipe.get('n_ingredients', 0)
                    ))
                connection.commit()
        finally:
            connection.close()    

    def get_collection_from_mongodb(self, collection_name):
            collection = self.db[collection_name]  
            cursor = collection.find({})  
            df = pd.DataFrame(list(cursor))
            return df
    
    def get_mongodb_collection(self, collection_name):
        return self.db[collection_name]




    def add_recipe_to_dislikes(self, user_id, recipe_id):
        success= False
        connection = pymysql.connect(**self.mysql_connection_config)
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO users_recipes_dislikes (user_id, recipe_id, added_on) VALUES (%s, %s, NOW())"
                cursor.execute(sql, (user_id, recipe_id))
            connection.commit()
            success = True
        finally:
            connection.close()
        return success

    def add_recipes_to_mysql(self, user_id, recipe_id):
        connection = pymysql.connect(**self.mysql_connection_config)
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO users_added_recipes (user_id, recipe_id) VALUES (%s, %s)"
                cursor.execute(sql, (user_id, recipe_id))
            connection.commit()
        finally:
            connection.close()
    
    def add_recipes_to_mongodb(self, recipe):
        recipes_collection = self.db["recipes"]
        recipes_collection.insert_one(recipe)
    
    def add_recipe(self, user_id, recipe_id, recipe):
        self.insert_recipes_into_mysql([recipe])
        self.add_recipes_to_mysql(user_id, recipe._id)
        self.add_recipes_to_mongodb(recipe)

    def delete_recipe_from_mongodb(self, recipe_id):
        recipes_collection = self.db["recipe"] 
        recipes_collection.delete_one({"_id": ObjectId(recipe_id)}) 

        users_interactions_collection = self.db["users_interactions"]
        users_interactions_collection.update_many({}, {"$pull": {"user_interaction": {"recipe_id": ObjectId(recipe_id)}}})

    def delete_recipe_from_mysql(self,user_id, recipe_id):
        status = False
        connection = pymysql.connect(**self.mysql_connection_config)
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM users_added_recipes WHERE recipe_id = %s AND user_id = %s;"
                cursor.execute(sql, (recipe_id,user_id))
            connection.commit()

            with connection.cursor() as cursor:
                sql2 = "DELETE FROM `recipes` WHERE recipe_id = %s ;"
                cursor.execute(sql2, (recipe_id))
            connection.commit()
            status = True
        finally:
            connection.close()
        return status

    def delete_recipe(self,user_id, recipe_id):
        self.delete_recipe_from_mongodb(user_id, recipe_id)
        self.delete_recipe_from_mysql(user_id, recipe_id)


    def increment_user_recipes_views_nosql(self, user_id, recipe_id):
        collection = self.get_mongodb_collection("users_interactions") 
        
        existing_interaction = collection.find_one(
            {"_id": user_id, "user_interaction.recipe_id": recipe_id}
        )

        if existing_interaction:
            result = collection.update_one(
                {"_id": user_id, "user_interaction.recipe_id": recipe_id},
                {"$inc": {"user_interaction.$.view": 1}}
            )
        else:
            new_interaction = {
                "recipe_id": recipe_id,
                "date": datetime.datetime.now(),  
                "rating": 0, 
                "view": 1,  
                "save": 0,  
                "comment": ""  
            }

            result = collection.update_one(
                {"_id": user_id},
                {"$push": {"user_interaction": new_interaction}}
            )
        if result.modified_count == 1:
            return True
        else:
            return False        

    def increment_user_recipe_views_sql(self, user_id, recipe_id):
        result = False
        connection = pymysql.connect(**self.mysql_connection_config)
        try:
            with connection.cursor() as cursor:
                sql = """INSERT INTO user_recipe_views (user_id, recipe_id, views, last_view_at) VALUES (%s, %s, 1, NOW()) ON DUPLICATE KEY UPDATE views = views + 1, last_view_at = NOW()"""
                    
                val_views = (user_id, recipe_id)

                cursor.execute(sql, val_views)
            connection.commit()
            result = True
        finally:
            connection.close()
        return result
    

    def fetch_user_recommendations(self, user_id, algorithm, top_n):
        result = []
        connection = pymysql.connect(**self.mysql_connection_config)
        try:
            with connection.cursor() as cursor:
                sql = """SELECT ur.recipe_id as id, ur.algorithm_name as algorithm, r.name, r.minutes, r.submitted, r.tags, r.minutes, r.nutrition, r.n_steps, r.steps, r.description, r.ingredients, r.n_ingredients, r.created_at
                        FROM user_recommendations ur
                        INNER JOIN recipes r ON ur.recipe_id = r.recipe_id
                        LEFT JOIN (
                            SELECT recipe_id, MAX(last_view_at) as latest_view
                            FROM user_recipe_views
                            WHERE user_id = %s
                            GROUP BY recipe_id
                            ORDER BY latest_view DESC
                            LIMIT 3
                        ) urv ON ur.recipe_id = urv.recipe_id
                        WHERE ur.user_id = %s 
                        AND ur.algorithm_name = %s 
                        AND ur.recipe_id NOT IN (
                            SELECT recipe_id 
                            FROM users_recipes_dislikes 
                            WHERE user_id = %s
                        )
                        ORDER BY urv.latest_view DESC, ur.recommended_at DESC
                        LIMIT 15;
                """
                val_sql = (user_id, user_id, algorithm,  user_id)
                cursor.execute(sql, val_sql)
                rows = cursor.fetchall()

                
                for row in rows:
                    
                    result.append({
                    'id': str(row["id"]),
                    'name': str(row["name"]),
                    'submitted': str(row["submitted"]),
                    'tags': eval(str(row['tags'])),
                    'nutrition': eval(str(row["nutrition"])),
                    'n_steps': str(row["n_steps"]),
                    'steps': eval(str(row["steps"])),
                    'description': str(row["description"]),
                    'minutes': row["minutes"],
                    'ingredients': eval(row['ingredients']),
                    'n_ingredients': str(row["n_ingredients"]),
                    'algorithm': 'collaborative_item_based'
                    })

        except Exception as e:
            print("Error:", e)  
        finally:
            connection.close()
        return result



    def add_recipe_rating_nosql(self, user_id, recipe_id, new_rating):
        collection = self.get_mongodb_collection("users_interactions") 
        
        existing_interaction = collection.find_one(
            {"_id": user_id, "user_interaction.recipe_id": recipe_id}
        )

        if existing_interaction:
            result = collection.update_one(
                {"_id": user_id, "user_interaction.recipe_id": recipe_id},
                {"$set": {"user_interaction.$.rating": new_rating}}
            )
        else:
         
            new_interaction = {
                "recipe_id": recipe_id,
                "date": datetime.datetime.now(),  
                "rating": new_rating, 
                "view": 0, 
                "save": 0,  
                "comment": ""  
            }

            result = collection.update_one(
                {"_id": user_id},
                {"$push": {"user_interaction": new_interaction}}
            )
        if result.modified_count == 1:
            return True
        else:
             return False

    def add_recipe_comment_nosql(self, user_id, recipe_id, new_comment):
        collection = self.get_mongodb_collection("users_interactions") 
        
        existing_interaction = collection.find_one(
            {"_id": user_id, "user_interaction.recipe_id": recipe_id}
        )

        if existing_interaction:
            result = collection.update_one(
                {"_id": user_id, "user_interaction.recipe_id": recipe_id},
                {"$set": {"user_interaction.$.comment": new_comment}}
            )
        else:
            new_interaction = {
                "recipe_id": recipe_id,
                "date": datetime.datetime.now(), 
                "rating": new_comment, 
                "view": 0,  
                "save": 0, 
                "comment": ""  
            }

            result = collection.update_one(
                {"_id": user_id},
                {"$push": {"user_interaction": new_interaction}}
            )
        if result.modified_count == 1:
            return True
        else:
             return False
        


    def add_user_recommendations(self, user_id, algorithm, recommendations):
        result = False
        connection = pymysql.connect(**self.mysql_connection_config)
        try:
            with connection.cursor() as cursor:
                sql_recommendations = """
                INSERT INTO user_recommendations (user_id, recipe_id, algorithm_name, recommended_at)
                SELECT %s, %s, %s, NOW()
                FROM DUAL
                WHERE NOT EXISTS (
                    SELECT 1
                    FROM user_recommendations
                    WHERE user_id = %s AND recipe_id = %s AND algorithm_name = %s
                )
                """

                for recommendation in recommendations:
                    val_recommendations = (str(user_id), str(recommendation['id']), algorithm,str(user_id), str(recommendation['id']), algorithm)
                    cursor.execute(sql_recommendations, val_recommendations)
                    connection.commit()

                sql_count_recommendations = "SELECT SUM(1) FROM user_recommendations WHERE user_id = %s AND algorithm_name = %s"
                cursor.execute(sql_count_recommendations, (str(user_id), algorithm))
                count = cursor._rows[0]
                cursor._clear_result()
                count = int(count['SUM(1)'])


                if count is None:
                    count = 0

                if count >= 25: 
                    sql_latest_date = "SELECT MAX(recommended_at) FROM user_recommendations WHERE user_id = %s AND algorithm_name = %s"
                    cursor.execute(sql_latest_date, (str(user_id), algorithm))
                    latest_date = cursor._rows[0]['MAX(recommended_at)']
                    sql_delete_older = "DELETE FROM user_recommendations WHERE user_id = %s AND algorithm_name = %s AND recommended_at < %s"
                    cursor.execute(sql_delete_older, (str(user_id), algorithm, latest_date.strftime('%Y-%m-%d')))
                    connection.commit()
                    result = True

        finally:
            connection.close()
        return result

    def unsave_user_recipe_mysql(self, user_id, recipe_id):
        result = False
        connection = pymysql.connect(**self.mysql_connection_config)
        try:
            with connection.cursor() as cursor:
                sql = """DELETE FROM `user_saved_recipes` WHERE user_id = %s and recipe_id = %s"""
                
                cursor.execute(sql, (user_id, recipe_id))
            connection.commit()
            result = True
        finally:
            connection.close()
        return result

    def unsave_user_recipe_mongodb(self, user_id, recipe_id):   
        dbs_manager = DBS_MANAGER()
        collection = dbs_manager.get_mongodb_collection("users_interactions") 
        existing_interaction = collection.find_one(
        {"_id": user_id, "user_interaction.recipe_id": recipe_id}
    )

        if existing_interaction:
            result = collection.update_one(
                {"_id": user_id, "user_interaction.recipe_id": recipe_id},
                {"$set": {"user_interaction.$.save": 0}}
            )

            if result.modified_count == 1:
                return True
            else:
                return False
        else:
            new_interaction = {
                "recipe_id": recipe_id,
                "date": datetime.datetime.now(),  
                "rating": 0, 
                "view": 0, 
                "save": 0,  
                "comment": ""  
            }

            result = collection.update_one(
                {"_id": user_id},
                {"$push": {"user_interaction": new_interaction}}
            )
        if result.modified_count == 1:
            return True 
        else:
            return False   
    
    def save_user_recipe_mongodb(self, user_id, recipe_id):   
        dbs_manager = DBS_MANAGER()
        collection = dbs_manager.get_mongodb_collection("users_interactions") 
        existing_interaction = collection.find_one(
        {"_id": user_id, "user_interaction.recipe_id": recipe_id}
    )

        if existing_interaction:
            result = collection.update_one(
                {"_id": user_id, "user_interaction.recipe_id": recipe_id},
                {"$set": {"user_interaction.$.save": 1}}
            )

            if result.modified_count == 1:
                return True
            else:
                return False
        else:
            new_interaction = {
                "recipe_id": recipe_id,
                "date": datetime.datetime.now(), 
                "rating": 0, 
                "view": 0,  
                "save": 1, 
                "comment": ""  
            }

            result = collection.update_one(
                {"_id": user_id},
                {"$push": {"user_interaction": new_interaction}}
            )
        if result.modified_count == 1:
            return True 
        else:
            return False  

    def save_user_recipe_mysql(self, user_id, recipe_id):
        result = False
        connection = pymysql.connect(**self.mysql_connection_config)
        try:
            with connection.cursor() as cursor:
                sql = """INSERT INTO user_saved_recipes (user_id, recipe_id, saved_at) 
                         VALUES (%s, %s, %s)"""
                
                saved_at = datetime.datetime.now()  # Current timestamp
                val_saved_recipe = (user_id, recipe_id, saved_at)
                cursor.execute(sql, val_saved_recipe)

            connection.commit()
            result = True
        finally:
            connection.close()
        return result


    def checkIfUserLikedRecipe(self, user_id, recipe_id ):
        connection = pymysql.connect(**self.mysql_connection_config)
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `user_saved_recipes` WHERE user_id = %s and recipe_id = %s;"
                cursor.execute(sql, (user_id, recipe_id))
                user_mysql_data = cursor.fetchone()

            if user_mysql_data:
                return True

            return False 
        finally:
            connection.close()
    
    def login_user(self, email, password ):
      

        connection = pymysql.connect(**self.mysql_connection_config)
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM users WHERE  password = %s AND email = %s"
                cursor.execute(sql, (password, email))
                user_mysql_data = cursor.fetchone()

            if user_mysql_data:
                if user_mysql_data["id"]:
                    user_id = user_mysql_data["id"]
                    username = user_mysql_data["username"]
                    return {
                        "id": user_id,
                        "username": username,
                        "email": email
                    }

            return None  

        finally:
            connection.close()
        
    def insert_user(self, username, email, password):
        status = False
        user_id = ObjectId()
        interactions_collection = self.db["users_interactions"]
        user_doc = {
            "_id": user_id,
            "user_interaction": []
        }
        interactions_collection.insert_one(user_doc)

        connection = pymysql.connect(**self.mysql_connection_config)
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO users (id, username, email, password) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (str(user_id), username, email, password))
            connection.commit()
            status = True
        finally:
            connection.close()
        return status

    def update_user_details(self, user_id, new_username, new_email, new_password):
        success = False
        interactions_collection = self.db["users_interactions"]
        interactions_collection.update_one({"_id": user_id}, {"$set": {"username": new_username, "email": new_email, "password": new_password}})

        connection = pymysql.connect(**self.mysql_connection_config)
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE users SET username = %s, email = %s, password = %s WHERE id = %s"
                cursor.execute(sql, (new_username, new_email, new_password, user_id))
            connection.commit()
            success = True
        finally:
            connection.close()
        return success 

    def get_user_added_recipes(self, user_id):
        connection = pymysql.connect(**self.mysql_connection_config)
        try:
            with connection.cursor() as cursor:
                sql = "SELECT recipe_id FROM users_added_recipes WHERE user_id = %s"
                cursor.execute(sql, (user_id,))
                result = cursor.fetchall()
                return [row["recipe_id"] for row in result]
        finally:
            connection.close()

    def delete_user(self, user_id):
        try:
            recipes_collection = self.db["recipes"]
            user_added_recipes = self.get_user_added_recipes(user_id)

            with pymysql.connect(**self.mysql_connection_config) as connection:
                cursor = connection.cursor()


                for recipe_id in user_added_recipes:
                    recipes_collection.delete_one({"_id": ObjectId(recipe_id)})

                sql_user = "DELETE FROM users WHERE id = %s"
                cursor.execute(sql_user, (str(user_id),))

                sql_added_recipes = "DELETE FROM users_added_recipes WHERE user_id = %s"
                cursor.execute(sql_added_recipes, (str(user_id),))

                interactions_collection = self.db["users_interactions"]
                interactions_collection.delete_one({"_id": ObjectId(user_id)})

            return True  
        except Exception as e:

            print(f"Error deleting user: {str(e)}")
            return False  


