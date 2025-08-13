from bson import ObjectId
from flask_cors import cross_origin
from app.management import bp
from flask import Flask, request, jsonify

from app.configuration.database.dbs_manager import DBS_MANAGER


from flask import make_response

@bp.route("/register_user", methods=["POST"])
def create_user():
    #...
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    
    if not username or not email or not password:
        return make_response({'message': 'Invalid request data'}, 400)

    dbs_manager = DBS_MANAGER()
    success = dbs_manager.insert_user(username, email, password)
    
    if success:
        return make_response({'message': 'User created successfully'}, 200)
    else:
        return make_response({'message': 'Failed to create user'}, 500)
    


    
@bp.route("/checkIfUserLikedRecipe", methods=["GET"])
def check_if_user_liked_recipe():
    user_id = request.args.get('user_id')
    recipe_id = request.args.get('recipe_id')

    dbs_manager = DBS_MANAGER()
    liked = dbs_manager.checkIfUserLikedRecipe(user_id, recipe_id)
    
    if liked:
        return make_response({'userLiked': True}, 200)
    else:
        return make_response({'userLiked': False}, 200)


@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    password = data.get("password")
    email = data.get("email")

    if not password or not email:
        return make_response({"message": "Email and password are required"}, 400)

    dbs_manager = DBS_MANAGER()

    user_authenticated = dbs_manager.login_user(email, password)

    if user_authenticated:
        response = {"message": "Authentication successful", "user": user_authenticated}
        return jsonify(response), 200
    else:
        response = {"message": "Authentication failed"}
        return make_response(response, 401)





@bp.route("/update_user_details", methods=["POST"])
def update_user_details():
    data = request.get_json()
    user_id = data.get("user_id")
    new_username = data.get("username")
    new_email = data.get("email")
    new_password = data.get("password")

    if not user_id or not (new_username or new_email or new_password):
        return make_response({"message": "Invalid request data"}, 400)

    dbs_manager = DBS_MANAGER()
    success = dbs_manager.update_user_details(user_id, new_username, new_email, new_password)

    if success:
        return make_response({"message": "User details updated successfully"}, 200)
    else:
        return make_response({"message": "Failed to update user details"}, 500)




@bp.route("/delete_user", methods=["DELETE"])
def delete_user():
    user_id = request.args.get("user_id")

    if not user_id:
        return make_response({"message": "User ID is required"}, 400)

    dbs_manager = DBS_MANAGER()
    success = dbs_manager.delete_user(user_id)

    if success:
        return make_response({"message": "User deleted successfully"}, 200)
    else:
        return make_response({"message": "Failed to delete user"}, 500)



@bp.route('/delete_recipe', methods=['DELETE'])
def delete_recipe():
    try:
        user_id = request.args.get("user_id")
        recipe_id = request.args.get('recipe_id')

        if recipe_id is None:
            return jsonify({"message": "Recipe ID is missing in query parameters"}), 400

        dbs_manager = DBS_MANAGER()
        succes = dbs_manager.delete_recipe(user_id, recipe_id)
        if succes:
            return jsonify({"message": "Recipe deleted successfully"})
        else:
            return jsonify({"message": "Recipe hasn't been deleted"})

    except Exception as e:
        return jsonify({"message": str(e)}), 500

@bp.route("/add_recipe", methods=["POST"])
def add_recipe_route():
    try:
        data = request.get_json()
        user_id = data["user_id"]
        recipe_id = data["recipe_id"]
        recipe = data["recipe"]
        recipe["_id"] = ObjectId()

        dbs_manager = DBS_MANAGER()
        dbs_manager.add_recipe(user_id, recipe_id, recipe)
        return make_response({"message": "Recipe added successfully"}, 200)
    except Exception as e:
        return jsonify({"message": str(e)}), 500

    


@bp.route('/add_disliked_recipe', methods=['POST'])
def add_disliked_recipe():
    if request.method == 'POST':
        data = request.get_json()
        user_id = data.get('user_id')
        recipe_id = data.get('recipe_id')
        
        dbs_manager = DBS_MANAGER()
        try:
            dbs_manager.add_recipe_to_dislikes(user_id, recipe_id)
            response = {
                "message": "Recipe added to dislikes successfully"
            }
            return make_response(jsonify(response), 200)  # 200 OK status code
        except Exception as e:
            response = {
                "message": "Failed to add recipe to dislikes",
                "error": str(e)
            }
            return make_response(jsonify(response), 500)
    




