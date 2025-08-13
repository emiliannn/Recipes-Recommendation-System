import { Component, Input, Output, EventEmitter, OnInit, AfterViewInit, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialog } from '@angular/material/dialog';
import { NavigationExtras, Router } from '@angular/router';
import { RecipeDetailsComponent } from '../recipe-details/recipe-details.component';
import {ChangeDetectionStrategy} from '@angular/core';
import {MatButtonModule} from '@angular/material/button';
import {MatCardModule} from '@angular/material/card';
import { trigger, state, style, animate, transition } from '@angular/animations';
import {MatIconModule} from '@angular/material/icon';
import {MatBadgeModule} from '@angular/material/badge';
import { RecipesService } from '../../services/recipes.service';
import { ReviewRecipeComponent } from '../review-recipe/review-recipe.component';

@Component({
  selector: 'app-recipe',
  templateUrl: './recipe.component.html',
  styleUrl: './recipe.component.css'

})
export class RecipeComponent implements OnInit {

 user_id:  string = "6678f64d68c8b09fe477b57d";
 @Input() recipe: any | undefined;
 isFrozen = false;

 constructor(private dialog: MatDialog, private router: Router, private recipesService: RecipesService) {}

 ngOnInit(): void {
 }

 childClick(event: Event) {
  event.stopPropagation(); 
  console.log('Child clicked');
}
 
openRecipeDetailsPopup() {
  this.dialog.open(RecipeDetailsComponent, {
    width: '45em',
    height: '35em',
    data: { recipe: this.recipe },
  });
}

openReviewRecipePopup() {
  this.dialog.open(ReviewRecipeComponent, {
    width: '45em',
    height: '35em',
    data: { recipe: this.recipe },
  });
}

  add_disliked_recipe() {
      this.isFrozen = true;
      this.recipesService.add_disliked_recipe(this.user_id, this.recipe.id).subscribe((data) => {
        console.log(data.message);
    });
  }
  
  provideContentBasedRecommendations(recipe: any): void {
   
    const encodedData = encodeURIComponent(JSON.stringify(recipe));
    const navigationExtras: NavigationExtras = {
      queryParams: { recipe: encodedData },
      replaceUrl: true
    };
    this.router.navigate(['/recipesListContentBased'], navigationExtras);
    this.recipesService.increment_user_recipe_views(this.user_id, recipe.id)
    
  }
}