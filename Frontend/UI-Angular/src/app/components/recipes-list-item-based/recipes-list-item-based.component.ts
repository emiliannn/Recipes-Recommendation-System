import { Component } from '@angular/core';
import { NavigationExtras, Router } from '@angular/router';
import { RecipesService } from '../../services/recipes.service';

@Component({
  selector: 'app-recipes-list-item-based',
  templateUrl: './recipes-list-item-based.component.html',
  styleUrl: './recipes-list-item-based.component.css'
})
export class RecipesListItemBasedComponent {
  constructor(public router: Router, private recipesService: RecipesService) { }
  ngOnInit(): void {
    this.fetchRecipes();
  }
  recipesList: any;
  algorithm : string = "collaborative_item_based";
  user_id:  string = "6678f64d68c8b09fe477b57d";


  fetchRecipes(){
    this.recipesService.fetch_user_recommendations(this.user_id, this.algorithm, 15).subscribe((data) => {
      this.recipesList = data;
    });
  }
}
