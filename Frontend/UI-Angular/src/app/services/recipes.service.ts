import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class RecipesService {
  private apiUrl = 'http://localhost:5000';
  private user_id: string = "64f5b522b5997a1d1052aa01";

  constructor(private http: HttpClient) { }

  
  fetch_user_recommendations(user_id?: string, algorithm?: string, top_n?: number): Observable<any> {
    user_id = user_id;
    algorithm = algorithm || "matrix_factorization";
    top_n = top_n || 15;
    return this.http.get<any>(`${this.apiUrl}/fetch_user_recommendations?user_id=${user_id}&algorithm=${algorithm}&top_n=${top_n}`);
  }
    
  recommend_content_based(user_ingredients: string [], user_dislikes: string [], top_n: number ): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/content_based`, {user_ingredients: user_ingredients, user_dislikes: user_dislikes, top_n: top_n});
  }

  recommend_content_based_by_recipeID(top_n: number, recipe_id: string , user_id: string, user_dislikes: string []): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/recommend_content_based_by_id`, {recipe_id: recipe_id, user_dislikes: user_dislikes, top_n: top_n, user_id: user_id});
  }

  recommend_collaborative_matrix_factorization(top_n: number, user_id?: string, user_dislikes?: string []): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/collaborative/matrix_factorization`, {user_id: user_id,  user_dislikes: user_dislikes, top_n: top_n});
  }
  recommend_collaborative_item_based(top_n: number, user_id?: string, user_dislikes?: string []): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/collaborative/item_based`, {user_id: user_id,  user_dislikes: user_dislikes, top_n: top_n});
  }

  recommend_collaborative_user_based(top_n: number, user_id?: string, user_dislikes?: string []): Observable<any> {
      return this.http.post<any>(`${this.apiUrl}/collaborative/user_based`, {user_id: user_id,  user_dislikes: user_dislikes, top_n: top_n});
    }

  // recommend_recipes(user_id: string, algorithm: string): Observable<any> {
  //   return this.http.post<any>(`${this.apiUrl}/make_recommendations`, {user_id: user_id, algorithm: algorithm});
  // }

  add_disliked_recipe(user_id: string, recipe_id: string): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/add_disliked_recipe`, {user_id: user_id, recipe_id: recipe_id});
  }

  increment_user_recipe_views(user_id: string, recipe_id: string): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/increment_user_recipe_views`, {user_id: user_id, recipe_id: recipe_id});
  }

   add_recipe_rating(user_id: string, recipe_id: string, new_rating: number): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/add_recipe_rating`, {user_id: user_id, recipe_id: recipe_id, new_rating: new_rating});
  }

  add_recipe_comment(user_id: string, recipe_id: string, new_comment: string): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/add_recipe_comment`, {user_id: user_id, recipe_id: recipe_id, new_comment: new_comment});
  }

  save_user_recipe(user_id: string, recipe_id: string): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/save_user_recipe`, {user_id: user_id, recipe_id: recipe_id});
  }

  unsave_user_recipe(user_id: string, recipe_id: string): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/unsave_user_recipe`, {user_id: user_id, recipe_id: recipe_id});
  }
  
  checkIfUserLikedRecipe(user_id: string, recipe_id: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/checkIfUserLikedRecipe?user_id=${user_id}&recipe_id=${recipe_id}`);
  }
}