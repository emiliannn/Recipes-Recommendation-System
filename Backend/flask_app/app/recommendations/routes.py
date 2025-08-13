import datetime
from bson import json_util, ObjectId
import json
from bson import ObjectId
from app.recommendations import bp
from flask import Flask, make_response, request, jsonify
from app.configuration.paralel_computing_recommendations import ParalelComputing
from app.configuration.database.dbs_manager import DBS_MANAGER


  


@bp.route('/collaborative/matrix_factorization', methods=['POST'])
def recommend_collaborative_matrix_factorization():
    data = request.json
    user_id = data['user_id']
    user_dislikes = data['user_dislikes']
    top_n = data['top_n']
    
    paralelComputing = ParalelComputing(user_id=user_id)
    recommended_recipes = paralelComputing.compute_recommendations(user_ingredients = [], user_dislikes = [], top_n=top_n, algorithm = 'collaborative_matrix_factorization')

    return recommended_recipes
 


@bp.route('/collaborative/item_based', methods=['POST'])
def recommend_collaborative_item_based():
    data = request.json
    
    user_id = data['user_id']
    user_dislikes = data['user_dislikes']
    top_n = data['top_n']

    paralelComputing = ParalelComputing(user_id=user_id)
    recommended_recipes = paralelComputing.compute_recommendations(user_ingredients = [], user_dislikes = [], top_n=top_n, algorithm = 'collaborative_item_based')

    return jsonify(recommended_recipes)



@bp.route('/collaborative/user_based', methods=['POST'])
def recommend_collaborative_user_based():
    data = request.json
    user_id = data['user_id']
    top_n = data['top_n']

    paralelComputing = ParalelComputing(user_id=user_id)
    recommended_recipes = paralelComputing.compute_recommendations(user_ingredients = [], user_dislikes = [], top_n=top_n, algorithm = 'collaborative_user_based')

    return jsonify(recommended_recipes)





@bp.route('/recommend_content_based_by_id', methods=['POST'])
def recommend_content_based_by_id():
    data = request.json
    recipe_id = data['recipe_id']
    user_dislikes = data['user_dislikes']
    top_n = data['top_n']
    user_id = data['user_id']
    paralelComputing = ParalelComputing(user_id=user_id)
    recommended_recipes = paralelComputing.compute_recommendations(recipe_id = recipe_id, user_dislikes = user_dislikes, top_n=top_n, algorithm = 'content_based_by_recipeID')

    return jsonify(recommended_recipes)





@bp.route('/fetch_user_recommendations', methods=['GET'])
def fetch_user_recommendations():
    try:
        user_id = request.args.get('user_id')
        algorithm = request.args.get('algorithm')
        top_n = int(request.args.get('top_n'))

        dbs_manager = DBS_MANAGER()
        recommendations = dbs_manager.fetch_user_recommendations(user_id, algorithm, top_n)
        
        return jsonify(recommendations), 200
    except (KeyError, TypeError, ValueError) as e:
        return jsonify({"error": str(e)}), 400




@bp.route('/add_disliked_recipe', methods=['POST'])
def add_disliked_recipe():
    if request.method == 'POST':
        data = request.get_json()
        user_id = data.get('user_id')
        recipe_id = data.get('recipe_id')
        
        dbs_manager = DBS_MANAGER()
        succes = dbs_manager.add_recipe_to_dislikes(user_id, recipe_id)
        
        if succes:
            return jsonify({"message": "Recipe added to dislikes successfully"})
        else:
            return jsonify({"message": "Recipe hasn't been added to dislikes"})
    


@bp.route('/increment_user_recipe_views', methods=['POST'])
def increment_user_recipe_views():
    try:
        data = request.get_json()
        user_id = ObjectId(data['user_id'])
        recipe_id = ObjectId(data['recipe_id'])

        dbs_manager = DBS_MANAGER()
        dbs_manager.increment_user_recipes_views_nosql(user_id, recipe_id)
        dbs_manager.increment_user_recipe_views_sql(user_id, recipe_id)
        
        paralelComputing = ParalelComputing(user_id = user_id)
        recommendations_user_based =  paralelComputing.compute_recommendations(user_ingredients = [], user_dislikes = [], top_n=15, algorithm = "collaborative_user_based")
        recommendations_item_based =  paralelComputing.compute_recommendations(user_ingredients = [], user_dislikes = [], top_n=15, algorithm = "collaborative_item_based")
        recommendations_matrix_factorization =  paralelComputing.compute_recommendations(user_ingredients = [], user_dislikes = [], top_n=15, algorithm = "collaborative_matrix_factorization")


        
        dbs_manager.add_user_recommendations(user_id, "collaborative_user_based", recommendations_user_based)
        dbs_manager.add_user_recommendations(user_id, "collaborative_item_based", recommendations_item_based)
        dbs_manager.add_user_recommendations(user_id, "collaborative_matrix_factorization", recommendations_matrix_factorization)


        return jsonify({"status": "success"}), 200
    except (KeyError, TypeError, ValueError) as e:
        return jsonify({"error": str(e)}), 400




@bp.route('/unsave_user_recipe', methods=['POST'])
def unsave_user_recipe():
    try:
        data = request.get_json()
        user_id = data['user_id']
        recipe_id = data['recipe_id']

        dbs_manager = DBS_MANAGER()
        dbs_manager.unsave_user_recipe_mongodb(user_id, recipe_id)
        dbs_manager.unsave_user_recipe_mysql(user_id, recipe_id)

        paralelComputing = ParalelComputing(user_id = user_id)
        recommendations_user_based =  paralelComputing.compute_recommendations(user_ingredients = [], user_dislikes = [], top_n=15, algorithm = "collaborative_user_based")
        recommendations_item_based =  paralelComputing.compute_recommendations(user_ingredients = [], user_dislikes = [], top_n=15, algorithm = "collaborative_item_based")
        recommendations_matrix_factorization =  paralelComputing.compute_recommendations(user_ingredients = [], user_dislikes = [], top_n=15, algorithm = "collaborative_matrix_factorization")

        
        dbs_manager.add_user_recommendations(user_id, "collaborative_user_based", recommendations_user_based);
        dbs_manager.add_user_recommendations(user_id, "collaborative_item_based", recommendations_item_based);
        dbs_manager.add_user_recommendations(user_id, "collaborative_matrix_factorization", recommendations_matrix_factorization);

        return jsonify({"status": "success"}), 200
    except (KeyError, TypeError, ValueError) as e:
        return jsonify({"error": str(e)}), 400

@bp.route('/save_user_recipe', methods=['POST'])
def save_user_recipe():
    try:
        data = request.get_json()
        user_id = data['user_id']
        recipe_id = data['recipe_id']

        dbs_manager = DBS_MANAGER()
        dbs_manager.save_user_recipe_mongodb(user_id, recipe_id)
        dbs_manager.save_user_recipe_mysql(user_id, recipe_id)

        paralelComputing = ParalelComputing(user_id = user_id)
        recommendations_user_based =  paralelComputing.compute_recommendations(user_ingredients = [], user_dislikes = [], top_n=15, algorithm = "collaborative_user_based")
        recommendations_item_based =  paralelComputing.compute_recommendations(user_ingredients = [], user_dislikes = [], top_n=15, algorithm = "collaborative_item_based")
        recommendations_matrix_factorization =  paralelComputing.compute_recommendations(user_ingredients = [], user_dislikes = [], top_n=15, algorithm = "collaborative_matrix_factorization")

        
        dbs_manager.add_user_recommendations(user_id, "collaborative_user_based", recommendations_user_based);
        dbs_manager.add_user_recommendations(user_id, "collaborative_item_based", recommendations_item_based);
        dbs_manager.add_user_recommendations(user_id, "collaborative_matrix_factorization", recommendations_matrix_factorization);

        return jsonify({"status": "success"}), 200
    except (KeyError, TypeError, ValueError) as e:
        return jsonify({"error": str(e)}), 400
    

@bp.route('/add_recipe_rating', methods=['POST'])
def add_recipe_rating():
    try:
        data = request.get_json()
        user_id = ObjectId(data['user_id'])
        recipe_id = ObjectId(data['recipe_id'])
        new_rating = int(data['new_rating'])  

        dbs_manager = DBS_MANAGER()
        dbs_manager.add_recipe_rating_nosql(user_id, recipe_id, new_rating)


        paralelComputing = ParalelComputing(user_id = user_id)
        recommendations_user_based =  paralelComputing.compute_recommendations(user_ingredients = [], user_dislikes = [], top_n=15, algorithm = "collaborative_user_based")
        recommendations_item_based =  paralelComputing.compute_recommendations(user_ingredients = [], user_dislikes = [], top_n=15, algorithm = "collaborative_item_based")
        recommendations_matrix_factorization =  paralelComputing.compute_recommendations(user_ingredients = [], user_dislikes = [], top_n=15, algorithm = "collaborative_matrix_factorization")

        
        dbs_manager.add_user_recommendations(user_id, "collaborative_user_based", recommendations_user_based)
        dbs_manager.add_user_recommendations(user_id, "collaborative_item_based", recommendations_item_based)
        dbs_manager.add_user_recommendations(user_id, "collaborative_matrix_factorization", recommendations_matrix_factorization)

        return jsonify({"status": "success"}), 200
    except (KeyError, TypeError, ValueError) as e:
        return jsonify({"error": str(e)}), 400


@bp.route('/add_recipe_comment', methods=['POST'])
def add_recipe_comment():
    try:
        data = request.get_json()
        user_id = ObjectId(data['user_id'])
        recipe_id = ObjectId(data['recipe_id'])
        new_comment = data['new_comment']  

        dbs_manager = DBS_MANAGER()
        dbs_manager.add_recipe_comment_nosql(user_id, recipe_id, new_comment)

        return jsonify({"status": "success"}), 200
    except (KeyError, TypeError, ValueError) as e:
        return jsonify({"error": str(e)}), 400
        


