import datetime
import pymongo
import random
import pandas as pd
import numpy as np
import json
import sys
from sklearn.preprocessing import MinMaxScaler
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
from app.configuration.database.dbs_manager import DBS_MANAGER 
from itertools import chain
from app.recommendations.compute_recommendations.recommendations import recommend_recipes_content_based_by_recipeID, recommend_recipes_hybrid, recommend_recipes_content_based, recommend_recipes_collaborative_user_based, recommend_recipes_collaborative_item_based, recommend_recipes_collaborative_matrix_factorization


class ParalelComputing:
    def __init__(self, user_id = '64f5d5f084de34f5c115788a'):


        self.user_id = ObjectId(user_id)

        self.users_interactions_df = None 

        dbs_manager = DBS_MANAGER()
   
        



        self.recipes_df = dbs_manager.get_collection_from_mongodb('recipes')
 

        users_interactions_collection = dbs_manager.get_mongodb_collection('users_interactions')

        cursor = users_interactions_collection.find({})
        user_ids = []
        recipe_ids = []
        dates = []
        ratings = []
        views = []
        saves = []
        comments = []

        for document in cursor:
            _id = str(document['_id'])
            user_interaction = document['user_interaction']
            
            for interaction in user_interaction:
                recipe_id = str(interaction['recipe_id'])
                if 'date' in interaction and isinstance(interaction['date'], datetime.datetime):
                    date = interaction['date'].strftime("%Y-%m-%d %H:%M:%S")
                else:
                  
                    date = "0000-00-00 00:00:00"

                rating = interaction.get('rating', 0)
                view = interaction.get('view', 0)
                save = interaction.get('save', 0)
                comment = interaction.get('comment', None)
                
                # Append data to the respective lists
                user_ids.append(_id)
                recipe_ids.append(recipe_id)
                dates.append(date)
                ratings.append(rating)
                views.append(view)
                saves.append(save)
                comments.append(comment)

        self.users_interactions_df = pd.DataFrame({
            '_id': user_ids,
            'recipe_id': recipe_ids,
            'date': dates,
            'rating': ratings,
            'views': views,
            'save': saves,
            'comment': comments
        })




        self.recipes_df['_id'] = self.recipes_df['_id'].astype(str)
        self.user_interactions_df = self.users_interactions_df.loc[self.users_interactions_df['_id'].isin([self.user_id])]
        self.user_interactions_df['recipe_id'].apply(str)
        self.recipes_df = pd.merge(self.recipes_df, self.user_interactions_df, left_on='_id', right_on='recipe_id', how='outer', suffixes=('', '_right'))
        self.recipes_df['_id'] = self.recipes_df['_id'].apply(lambda x: ObjectId(x))

        # Drop columns
        self.recipes_df = self.recipes_df.drop(['recipe_id', '_id_right', 'date'], axis=1)




        self.refine_data()


    def refine_data(self):

        self.recipes_df['name'] = self.recipes_df['name'].fillna('')
        self.recipes_df['description'] = self.recipes_df['description'].fillna('')
        self.recipes_df['views'] = self.recipes_df['views'].fillna(0)
        self.recipes_df['rating'] = self.recipes_df['rating'].fillna(0)
        self.recipes_df['save'] = self.recipes_df['save'].fillna(0)
        self.recipes_df['comment'] = self.recipes_df['comment'].fillna('')
        self.recipes_df['implicit_weight'] = 0
        self.recipes_df['explicit_weight'] = 0
        self.recipes_df['total_weight'] = 0


        

        self.recipes_df['views'] = (self.recipes_df['views'] - self.recipes_df['views'].min()) / max(1e-6, self.recipes_df['views'].max() - self.recipes_df['views'].min())

        self.recipes_df['rating'] = (self.recipes_df['rating'] - self.recipes_df['rating'].min()) / max(1e-6, self.recipes_df['rating'].max() - self.recipes_df['rating'].min())
      
        mean_rating = self.recipes_df['rating'].mean()
        mean_views = self.recipes_df['views'].mean()


        self.recipes_df['rating'].replace(0, mean_rating, inplace=True)
        self.recipes_df['views'].replace(0, mean_views, inplace=True)

        self.recipes_df['implicit_weight'] = 0.2 * self.recipes_df['views'] + 0.8 * self.recipes_df['save']
        mean_implicit_weight = round(self.recipes_df['implicit_weight'].mean())
        self.recipes_df['implicit_weight'].replace(0, mean_implicit_weight, inplace=True)


        self.recipes_df['explicit_weight'] =  self.recipes_df['rating']
        self.recipes_df['explicit_weight'].replace(0, mean_rating, inplace=True)


        self.recipes_df['total_weight'] = 0.8 * self.recipes_df['implicit_weight'] + 0.2 * self.recipes_df['explicit_weight']

        mean_total_weight = self.recipes_df['total_weight'].mean()
        self.recipes_df['total_weight'].replace(0, mean_total_weight, inplace=True)




        self.recipes_df['tags'] = self.recipes_df['tags'].apply(ast.literal_eval)
        self.recipes_df['ingredients'] = self.recipes_df['ingredients'].apply(ast.literal_eval)

        # Step 2: Feature Extraction
        self.recipes_df['features'] = self.recipes_df['name'] + ' ' + self.recipes_df['description'] + ' ' + self.recipes_df['tags'].apply(lambda x: ' '.join(x))
        self.recipes_df['features'] = self.recipes_df['features'].fillna('')  

        self.user_interactions = self.users_interactions_df[self.users_interactions_df['_id'] == self.user_id]

        self.users_interactions_df['recommendation_score'] = 0
        self.users_interactions_df['views'] = (self.users_interactions_df['views'] - self.users_interactions_df['views'].min()) / max(1e-6, self.users_interactions_df['views'].max() - self.users_interactions_df['views'].min())

        self.users_interactions_df['rating'] = (self.users_interactions_df['rating'] - self.users_interactions_df['rating'].min()) / (self.users_interactions_df['rating'].max() - self.users_interactions_df['rating'].min())
        self.users_interactions_df['rating'] = (self.users_interactions_df['rating'] - self.users_interactions_df['rating'].min()) / max(1e-6, self.users_interactions_df['rating'].max() - self.users_interactions_df['rating'].min())

     

        
        mean_rating = self.users_interactions_df['rating'].mean()
        mean_views = self.users_interactions_df['views'].mean()

        self.users_interactions_df['rating'].replace(0, mean_rating, inplace=True)
        self.users_interactions_df['views'].replace(0, mean_views, inplace=True)
        self.users_interactions_df['recommendation_score'] = 0.4 * self.users_interactions_df['rating'] + 0.1 * self.users_interactions_df['views'] + 0.5 * self.users_interactions_df['save']
        mean_recommendation_score = self.users_interactions_df['recommendation_score'].mean()
        self.users_interactions_df['recommendation_score'].replace(0, mean_recommendation_score, inplace=True)





    def calculate_index_ranges(self, total_items, num_workers):
        chunk_size = total_items // num_workers
        remainder = total_items % num_workers

        index_ranges = []
        start_index = 0
        for worker_id in range(num_workers):
            end_index = start_index + chunk_size - 1 + (1 if worker_id < remainder else 0)
            if worker_id == num_workers - 1:
                end_index = total_items - 1
            index_ranges.append((start_index, end_index))
            start_index = end_index + 1

        return index_ranges






    def generate_recommendations(self, user_ingredients, user_dislikes, top_n, start_idx, end_idx, recipes_df, user_recommendation_preference, algorithm, users_interactions_df, user_interactions_df, user_id, recipe_id):
        recommended_recipes = []
        if(algorithm == 'collaborative_user_based'):
            recommended_recipes = recommend_recipes_collaborative_user_based(user_ingredients=user_ingredients, user_dislikes=user_dislikes, top_n=top_n, recipes_df=recipes_df, users_interactions_df = users_interactions_df, user_interactions_df = user_interactions_df, user_id=str(user_id), user_recommendation_preference = user_recommendation_preference)
        elif(algorithm == 'collaborative_item_based'):
            recommended_recipes = recommend_recipes_collaborative_item_based(user_ingredients=user_ingredients, user_dislikes=user_dislikes, top_n=top_n, recipes_df=recipes_df, users_interactions_df = users_interactions_df, user_id=str(user_id), user_recommendation_preference = user_recommendation_preference, user_interactions_df = user_interactions_df)
        elif(algorithm == 'collaborative_matrix_factorization'):
            recommended_recipes = recommend_recipes_collaborative_matrix_factorization(user_ingredients=user_ingredients, user_dislikes=user_dislikes, top_n=top_n, recipes_df=recipes_df, users_interactions_df = users_interactions_df, user_id=user_id, user_recommendation_preference = user_recommendation_preference,user_interactions_df = user_interactions_df)
 
        
        return recommended_recipes


    @delayed
    def generate_recommendations_in_parallel(self, user_ingredients, user_dislikes, top_n, start_idx, end_idx, recipes_df, user_recommendation_preference, algorithm, users_interactions_df, user_interactions_df, user_id, recipe_id):
        recommended_recipes = []
        subset_recipes_df = recipes_df.loc[start_idx:end_idx]

        recommended_recipes = recommend_recipes_content_based_by_recipeID(recipe_id = recipe_id, user_dislikes=user_dislikes, top_n=top_n, recipes_df=subset_recipes_df, users_interactions_df = users_interactions_df, user_id=user_id, user_recommendation_preference = user_recommendation_preference)
        
        return recommended_recipes


    def compute_recommendations(self, user_ingredients=[], user_dislikes=[], top_n=5, algorithm='content_based', recipe_id=None):
        if algorithm == 'content_based_by_recipeID':
            delayed_results = []
            num_processes = 6 
            total_items = len(self.recipes_df)
            index_ranges = self.calculate_index_ranges(total_items, num_processes)

            for start_idx, end_idx in index_ranges:
                delayed_results.append(delayed(self.generate_recommendations_in_parallel)(self,
                    user_ingredients=user_ingredients, user_dislikes=user_dislikes, top_n=top_n, 
                    start_idx=start_idx, end_idx=end_idx, recipes_df=self.recipes_df, 
                    user_recommendation_preference=1, algorithm=algorithm, 
                    users_interactions_df=self.users_interactions_df, 
                    user_interactions_df=self.user_interactions_df, user_id=self.user_id, 
                    recipe_id=recipe_id
                ))

            results = dask.compute(*delayed_results)
            results = list(chain.from_iterable(results))
            return results
        else:   
            results = self.generate_recommendations(user_ingredients = user_ingredients, user_dislikes = user_dislikes, top_n = top_n, start_idx = 0, end_idx  = len(self.recipes_df), recipes_df = self.recipes_df, user_recommendation_preference = 1, algorithm = algorithm, users_interactions_df = self.users_interactions_df, user_interactions_df = self.user_interactions_df, user_id= self.user_id, recipe_id = recipe_id)
            return results











