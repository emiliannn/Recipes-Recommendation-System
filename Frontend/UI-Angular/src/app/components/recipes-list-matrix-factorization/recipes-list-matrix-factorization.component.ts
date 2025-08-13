import { Component } from '@angular/core';
import { NavigationExtras, Router } from '@angular/router';
import { RecipesService } from '../../services/recipes.service';
import { Location } from '@angular/common'; // Import the Location class from '@angular/common'


@Component({
  selector: 'app-recipes-list-matrix-factorization',
  templateUrl: './recipes-list-matrix-factorization.component.html',
  styleUrl: './recipes-list-matrix-factorization.component.css'
})
export class RecipesListMatrixFactorizationComponent {

  constructor(public router: Router, private recipesService: RecipesService, private location: Location ) { }
  ngOnInit(): void {
    this.fetchRecipes();
  }
  recipesList: any;
  algorithm : string = "collaborative_matrix_factorization";
  user_id:  string = "6678f64d68c8b09fe477b57d";


  fetchRecipes(){
    this.recipesService.fetch_user_recommendations(this.user_id, this.algorithm, 15).subscribe((data) => {
      this.recipesList = data;
    });
  }
}
