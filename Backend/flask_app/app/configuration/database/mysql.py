import pymysql.cursors

class MySQL:
    def __init__(self, mongo_connection_string='mongodb://localhost:27017', mongo_database_name='rs_db',
                 mysql_connection_config=None):
        if mysql_connection_config is None:
            self.mysql_connection_config = {
                'host': 'localhost',
                'user': 'your_mysql_username',
                'password': 'your_mysql_password',
                'db': 'rs_db',
                'charset': 'utf8mb4',
                'cursorclass': pymysql.cursors.DictCursor
            }
        else:
            self.mysql_connection_config = mysql_connection_config

    def add_recipe_to_favorites(self, user_id, recipe_id):


        # Add the logic to add a recipe to user_recipe_favorites in MySQL
        connection = pymysql.connect(**self.mysql_connection_config)
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO users_recipes_favorites (user_id, recipe_id) VALUES (%s, %s)"
                cursor.execute(sql, (user_id, recipe_id))
            connection.commit()
        finally:
            connection.close()

    def add_recipe_to_dislikes(self, user_id, recipe_id):

        connection = pymysql.connect(**self.mysql_connection_config)
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO users_recipes_dislikes (user_id, recipe_id) VALUES (%s, %s)"
                cursor.execute(sql, (user_id, recipe_id))
            connection.commit()
        finally:
            connection.close()

    def add_recipes(self, user_id, recipe_id):
        connection = pymysql.connect(**self.mysql_connection_config)
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO users_added_recipes (user_id, recipe_id) VALUES (%s, %s)"
                cursor.execute(sql, (user_id, recipe_id))
            connection.commit()
        finally:
            connection.close()


    