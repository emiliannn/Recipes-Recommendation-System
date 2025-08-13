import pymongo
from bson import ObjectId
import random
import pandas as pd
import numpy as np
import json
import sys
from bson.objectid import ObjectId
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from flask import Flask, request, jsonify
from scipy.spatial.distance import cosine
from surprise import Dataset, Reader, SVD
from surprise.model_selection import cross_validate
import ast
import multiprocessing
import dask
from dask import delayed
import json
import ast

def recommend_recipes_hybrid(user_ingredients = [], user_dislikes =[], top_n=5, recipes_df = [] ,  users_interactions_df = [], user_interactions_df  = [],  user_id=None, user_recommendation_preference = 0):

    collaborative_filtering_recipes = []
    content_based_recipes = []
    recommendations = []
    num_cb_recipes = top_n
    num_cf_recipes = top_n

    
    if len(user_ingredients) > 0:

        if not user_interactions_df.empty:
       
            if len(user_interactions_df) > 0:
                num_cb_recipes = int(top_n * 0.6)
                num_cf_recipes = top_n - num_cb_recipes

                collaborative_filtering_recipes = recommend_recipes_collaborative_matrix_factorization(user_interactions_df = user_interactions_df, user_ingredients = user_ingredients, user_dislikes=user_dislikes, dislike_weight_factor = 0,top_n=num_cf_recipes,  recipes_df = recipes_df, users_interactions_df = users_interactions_df, user_id = user_id,user_recommendation_preference = 0)
                if (collaborative_filtering_recipes):
                    recommendations.extend(collaborative_filtering_recipes)
                else:
                    num_cb_recipes = top_n
           

        content_based_recipes = recommend_recipes_content_based(user_ingredients = user_ingredients,   user_dislikes=user_dislikes, recipes_df=recipes_df, users_interactions_df = users_interactions_df, user_id = user_id,  dislike_weight_factor = 0, user_recommendation_preference = user_recommendation_preference, top_n=top_n - len(collaborative_filtering_recipes))
        recommendations.extend(content_based_recipes)
  

    else:
        if not user_interactions_df.empty:
      
            if len(user_interactions_df) > 0:
        
                collaborative_filtering_recipes = recommend_recipes_collaborative_matrix_factorization(user_interactions_df = user_interactions_df, user_ingredients = user_ingredients, user_dislikes=user_dislikes, dislike_weight_factor = 0,top_n=num_cf_recipes,  recipes_df = recipes_df, users_interactions_df = users_interactions_df, user_id = user_id,user_recommendation_preference = 0)

                if (collaborative_filtering_recipes):
                    recommendations.extend(collaborative_filtering_recipes)

                else:
                    content_based_recipes = recommend_recipes_content_based(user_ingredients = user_ingredients,   user_dislikes=user_dislikes, recipes_df=recipes_df, users_interactions_df = users_interactions_df, user_id = user_id,  dislike_weight_factor = 0, user_recommendation_preference = user_recommendation_preference, top_n=top_n - len(collaborative_filtering_recipes))
                        
                    recommendations.extend(content_based_recipes)

            else:
                content_based_recipes = recommend_recipes_content_based(user_ingredients = user_ingredients,   user_dislikes=user_dislikes, recipes_df=recipes_df, users_interactions_df = users_interactions_df, user_id = user_id,  dislike_weight_factor = 0, user_recommendation_preference = user_recommendation_preference, top_n=top_n - len(collaborative_filtering_recipes))
                recommendations.extend(content_based_recipes)
        else:
            content_based_recipes = recommend_recipes_content_based(user_ingredients = user_ingredients,   user_dislikes=user_dislikes, recipes_df=recipes_df, users_interactions_df = users_interactions_df, user_id = user_id,  dislike_weight_factor = 0, user_recommendation_preference = user_recommendation_preference, top_n=top_n - len(collaborative_filtering_recipes))
            recommendations.extend(content_based_recipes)
    

    return recommendations

def recommend_recipes_content_based(user_ingredients = [],   user_dislikes=[],  top_n=5, recipes_df=[], users_interactions_df = [], user_id = None,  dislike_weight_factor = 0, user_recommendation_preference = 1):

    user_recommendation_preference = 0
    disliked_ids = recipes_df.loc[recipes_df['name'].isin(user_dislikes), '_id']

    recipe_ids = users_interactions_df['recipe_id'].unique()
    
 
    rated_recipe_ids = users_interactions_df.loc[(users_interactions_df['_id'] == user_id) & (users_interactions_df['rating'] > 0), 'recipe_id']
    
   
    saved_recipe_ids = users_interactions_df.loc[(users_interactions_df['_id'] == user_id) & (users_interactions_df['save'] == 1), 'recipe_id']
    
    rated_saved_recipes_ids = np.union1d(rated_recipe_ids, saved_recipe_ids)
    rated_saved_disliked_recipes_ids = np.union1d(rated_saved_recipes_ids, disliked_ids.astype(str).to_numpy())    

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(recipes_df['features'])
    
    tfidf_matrix = pd.DataFrame(tfidf_matrix.toarray(), index=recipes_df.index)
   
    all_top_indices = set()

    
    if(len(user_ingredients) > 0):
        for ingredient in user_ingredients:
          
            filtered_recipes = recipes_df[[ingredient.lower() in name.lower() for name in recipes_df['name'].astype(str)]]
            
            if (len(filtered_recipes) == 0 ):
                return []

            masked_tfidf_matrix = tfidf_matrix.loc[filtered_recipes.index]
            recipe_scores = cosine_similarity(masked_tfidf_matrix, tfidf_matrix)
            
            recommendations_indices = recipe_scores.sum(axis=0)

            top_indices = np.argsort(recommendations_indices)[::-1][:top_n]
            all_top_indices.update(top_indices)

        all_top_indices = list(all_top_indices)

        random.shuffle(all_top_indices)
        all_top_indices = all_top_indices[:top_n]
        recipes = recipes_df.iloc[all_top_indices]     
        return recipes['name'].tolist()
    



def recommend_recipes_content_based_by_recipeID(recipe_id=None, user_dislikes=[], top_n=5, recipes_df=[], users_interactions_df=[], user_id=None, dislike_weight_factor=0, user_recommendation_preference=1):
    disliked_ids = recipes_df.loc[recipes_df['name'].isin(user_dislikes), '_id']

    rated_recipe_ids = users_interactions_df.loc[(users_interactions_df['_id'] == user_id) & (users_interactions_df['rating'] > 0), 'recipe_id']
    
    saved_recipe_ids = users_interactions_df.loc[(users_interactions_df['_id'] == user_id) & (users_interactions_df['save'] == 1), 'recipe_id']
    
    rated_saved_recipes_ids = np.union1d(rated_recipe_ids, saved_recipe_ids)
    rated_saved_disliked_recipes_ids = np.union1d(rated_saved_recipes_ids, disliked_ids.astype(str).to_numpy())

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(recipes_df['features'])
    
    tfidf_matrix = pd.DataFrame(tfidf_matrix.toarray(), index=recipes_df['_id'])
    
    all_top_indices = set()

    if recipe_id:
 
        recipe_id = ObjectId(recipe_id) if isinstance(recipe_id, str) else recipe_id

        if recipe_id not in tfidf_matrix.index:
            return []

        
        masked_tfidf_matrix = tfidf_matrix.loc[recipe_id]  # Index by recipe_id

        recipe_scores = cosine_similarity(masked_tfidf_matrix.values.reshape(1, -1), tfidf_matrix)
        
        recommendations_indices = recipe_scores.sum(axis=0)

        top_indices = np.argsort(recommendations_indices)[::-1][:top_n]
        all_top_indices.update(top_indices)

        all_top_indices = list(all_top_indices)

        all_top_indices = [idx for idx in all_top_indices if idx not in rated_saved_disliked_recipes_ids and recipes_df.iloc[idx]['_id'] != recipe_id]


        random.shuffle(all_top_indices)
        recommended_recipe_ids = all_top_indices[:top_n] 

        recommended_recipes_list = []
        for recipe_id in recommended_recipe_ids:
            recipe = recipes_df.iloc[recipe_id]  
            recommended_recipes_list.append({
            'id': str(recipe.loc["_id"]),
            'name': str(recipe.loc["name"]),
            'submitted': str(recipe.loc["submitted"]),
            'tags': eval(str(recipe['tags'])),
            'nutrition': eval(str(recipe.loc["nutrition"])),
            'n_steps': str(recipe.loc["n_steps"]),
            'steps': eval(str(recipe["steps"])),
            'minutes': str(recipe.loc["minutes"]),
            'description': str(recipe.loc["description"]),
            'ingredients': eval(str(recipe['ingredients'])),
            'n_ingredients': str(recipe.loc["n_ingredients"]),
            'algorithm': 'collaborative_item_based'
    })

        return recommended_recipes_list



def recommend_recipes_collaborative_user_based(user_ingredients=[], user_dislikes=[], top_n=5, recipes_df=[], users_interactions_df = [], user_interactions_df = [], user_recommendation_preference = [], n_similar_users = 5, user_id = None):

    disliked_ids = recipes_df.loc[recipes_df['name'].isin(user_dislikes), '_id']

    recipe_ids = users_interactions_df['recipe_id'].unique()

    rated_recipe_ids = users_interactions_df.loc[(users_interactions_df['_id'] == user_id) & (users_interactions_df['rating'] > 0), 'recipe_id']

    saved_recipe_ids = users_interactions_df.loc[(users_interactions_df['_id'] == user_id) & (users_interactions_df['save'] == 1), 'recipe_id']
    
    rated_saved_disliked_recipes_ids = np.union1d(rated_recipe_ids, saved_recipe_ids)
    rated_saved_disliked_recipes_ids = np.union1d(rated_saved_disliked_recipes_ids, disliked_ids.astype(str).to_numpy())






    users_interactions_df.drop_duplicates(subset=['_id', 'recipe_id'], inplace=True)


    pivot_matrix = users_interactions_df.pivot(index='_id', columns='recipe_id', values='recommendation_score').fillna(0)
    user_similarity = pd.DataFrame(cosine_similarity(pivot_matrix), index=pivot_matrix.index, columns=pivot_matrix.index)



    user_index = pivot_matrix.index.get_loc(user_id)

    similar_users = (user_similarity.iloc[user_index]).drop(user_id)
  
    top_similar_users_idx = similar_users[similar_users > 0]
    top_similar_users_idx = (top_similar_users_idx.nlargest(n_similar_users)).index

    recommended_recipe_indices = []

    for user_idx in top_similar_users_idx:
        user_recipes_recommendation_score = (pivot_matrix.loc[user_idx]) 


        recipes_ids = (user_recipes_recommendation_score.sort_values(ascending=False)).index        # Filter out the recipes that the current user has disliked

        unrated_unsaved_recipe_indices = set(recipes_ids).difference(rated_saved_disliked_recipes_ids)
        unrated_unsaved_recipe_indices = list(unrated_unsaved_recipe_indices)[:top_n]
        recommended_recipe_indices.extend(unrated_unsaved_recipe_indices)

     

    recommended_recipe_indices = list(set(recommended_recipe_indices))
    random.shuffle(recommended_recipe_indices)

    top_recipe_ids = (recommended_recipe_indices[:top_n])
    top_recipe_ids = [ObjectId(x) for x in top_recipe_ids]

    recommended_recipes_list = []
    for recipe_id in top_recipe_ids:
        recipe = recipes_df.loc[recipes_df['_id'].isin(top_recipe_ids)].iloc[0]  # Assuming a single match
        recommended_recipes_list.append({
        'id': str(recipe.loc["_id"]),
        'name': str(recipe.loc["name"]),
        'submitted': str(recipe.loc["submitted"]),
        'tags': eval(str(recipe['tags'])),
        'nutrition': eval(str(recipe.loc["nutrition"])),
        'n_steps': str(recipe.loc["n_steps"]),
        'steps': eval(str(recipe["steps"])),
        'description': str(recipe.loc["description"]),
        'ingredients': eval(str(recipe['ingredients'])),
        'n_ingredients': str(recipe.loc["n_ingredients"]),
        'algorithm': 'collaborative_user_based'
    })

    return recommended_recipes_list







def recommend_recipes_collaborative_item_based(user_ingredients=[], user_interactions_df=pd.DataFrame(), user_dislikes=[], dislike_weight_factor=0, top_n=5, recipes_df=pd.DataFrame(), users_interactions_df=pd.DataFrame(), user_id=None, user_recommendation_preference=0):
    users_interactions_df.drop_duplicates(subset=['_id', 'recipe_id'], inplace=True)


    pivot_matrix = users_interactions_df.pivot(index='recipe_id', columns='_id', values='recommendation_score').fillna(0)

    item_similarity = pd.DataFrame(cosine_similarity(pivot_matrix), index=pivot_matrix.index, columns=pivot_matrix.index)


    user_rated_saved_recipe_ids = users_interactions_df.loc[(users_interactions_df['_id'] == user_id) & ((users_interactions_df['rating'] > 0) | (users_interactions_df['save'] == 1)), 'recipe_id']


    unrated_recipe_ids = users_interactions_df['recipe_id'].loc[~users_interactions_df['recipe_id'].isin(user_rated_saved_recipe_ids)]


    weighted_avg_similarity = item_similarity.loc[unrated_recipe_ids, user_rated_saved_recipe_ids].sum(axis=1) / user_rated_saved_recipe_ids.shape[0]


    top_recipe_ids = np.argsort(weighted_avg_similarity)[::-1][:top_n]
    recommended_recipes_list = []
    for recipe_id in top_recipe_ids:
        recipe = recipes_df.iloc[recipe_id]  # Assuming a single match
 
        recommended_recipes_list.append({
        'id': str(recipe.loc["_id"]),
        'name': str(recipe.loc["name"]),
        'submitted': str(recipe.loc["submitted"]),
        'tags': eval(str(recipe['tags'])),
        'nutrition': eval(str(recipe.loc["nutrition"])),
        'n_steps': str(recipe.loc["n_steps"]),
        'steps': eval(str(recipe["steps"])),
        'description': str(recipe.loc["description"]),
        'ingredients': eval(str(recipe['ingredients'])),
        'n_ingredients': str(recipe.loc["n_ingredients"]),
        'algorithm': 'collaborative_item_based'
    })
    return recommended_recipes_list






def recommend_recipes_collaborative_matrix_factorization(user_interactions_df = [], user_ingredients = [], user_dislikes=[], dislike_weight_factor = 0,top_n=5,  recipes_df = [], users_interactions_df = [], user_id = None,user_recommendation_preference = 0): 

    reader = Reader(rating_scale=(users_interactions_df['recommendation_score'].min(), users_interactions_df['recommendation_score'].max()))

    data = Dataset.load_from_df(users_interactions_df[['_id', 'recipe_id', 'recommendation_score']], reader)

    algo = SVD()


    cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)

    trainset = data.build_full_trainset()
    algo.fit(trainset)

    recipe_ids = users_interactions_df['recipe_id'].unique()
    
    rated_recipe_ids = users_interactions_df.loc[(users_interactions_df['_id'] == user_id) & (users_interactions_df['rating'] > 0), 'recipe_id']
    
    saved_recipe_ids = users_interactions_df.loc[(users_interactions_df['_id'] == user_id) & (users_interactions_df['save'] == 1), 'recipe_id']
    
    unrated_unsaved_recipe_ids = np.setdiff1d(recipe_ids, np.union1d(rated_recipe_ids, saved_recipe_ids))

    
    predictions = [algo.predict(user_id, recipe_id) for recipe_id in unrated_unsaved_recipe_ids]
    
    predictions.sort(key=lambda x: x.est, reverse=True)

   
  
    recommended_recipe_ids = [ObjectId(prediction.iid) for prediction in predictions[:top_n]]

    recommended_recipes_list = []
    for recipe_id in recommended_recipe_ids:
        recipe = recipes_df.loc[recipes_df['_id'] == recipe_id].iloc[0]  # Assuming a single match
        recommended_recipes_list.append({
        'id': str(recipe.loc["_id"]),
        'name': str(recipe.loc["name"]),
        'submitted': str(recipe.loc["submitted"]),
        'tags': eval(str(recipe['tags'])),
        'nutrition': eval(str(recipe.loc["nutrition"])),
        'n_steps': str(recipe.loc["n_steps"]),
        'steps': eval(str(recipe["steps"])),
        'description': str(recipe.loc["description"]),
        'ingredients': eval(str(recipe['ingredients'])),
        'n_ingredients': str(recipe.loc["n_ingredients"]),
        'algorithm': 'collaborative_item_based'
    })

    return recommended_recipes_list
















