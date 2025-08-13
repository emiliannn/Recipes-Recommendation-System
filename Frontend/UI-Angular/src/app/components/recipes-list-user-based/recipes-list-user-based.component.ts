import { Component } from '@angular/core';
import { NavigationExtras, Router } from '@angular/router';
import { RecipesService } from '../../services/recipes.service';
import { Location } from '@angular/common'; // Import the Location class from '@angular/common'


@Component({
  selector: 'app-recipes-list-user-based',
  templateUrl: './recipes-list-user-based.component.html',
  styleUrl: './recipes-list-user-based.component.css'
})
export class RecipesListUserBasedComponent {
  constructor(public router: Router, private recipesService: RecipesService, private location: Location) { }
  algorithm : string = "collaborative_user_based";
  user_id:  string = "6678f64d68c8b09fe477b57d";
  ngOnInit(): void {
    this.fetchRecipes();
  }
  
  recipesList: any = [];
  isFrozen: boolean = false;


  fetchRecipes(){
    this.recipesService.fetch_user_recommendations(this.user_id, this.algorithm, 15).subscribe((data) => {
      this.recipesList = data;
    });
  }


  updateIsFrozen(isFrozen: boolean) {
    this.isFrozen = isFrozen;
  }

}