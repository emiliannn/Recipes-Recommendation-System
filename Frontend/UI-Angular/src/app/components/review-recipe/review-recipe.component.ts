import { Component, Inject, Input } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { RecipesService } from '../../services/recipes.service';
import { RatingChangeEvent } from 'angular-star-rating';
@Component({
  selector: 'app-review-recipe',
  templateUrl: './review-recipe.component.html',
  styleUrl: './review-recipe.component.css'
})
export class ReviewRecipeComponent {

  recipeRating: number = 0;
  reciepeComment: string = '';
  recipe: any | undefined;
  user_id:  string = "6678f64d68c8b09fe477b57d";

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any,
    private dialogRef: MatDialogRef<ReviewRecipeComponent>,
    private recipesService: RecipesService,
  ) {
    this.recipe = data.recipe;
  }

  onRatingChange($event: RatingChangeEvent) {
    this.recipeRating = $event.rating;
  }

  submitReview(): void {
    this.dialogRef.close();
    if(this.recipeRating > 0) {
      this.recipesService
      .add_recipe_rating(this.user_id, this.recipe.id, this.recipeRating).subscribe((response) => {
        if(response.status === 200){
          console.log("Rating has been submitted successfully: ", this.recipeRating);
        }
      });
    }
    if(this.reciepeComment != ""){
      this.recipesService.add_recipe_comment(this.user_id, this.recipe.id, this.reciepeComment).subscribe((response) => {
        if(response.status === 200){
          console.log("Comment has been submitted successfully: ", this.reciepeComment);
        }
      });
    }
    this.recipesService
 

  }
  
 
}
