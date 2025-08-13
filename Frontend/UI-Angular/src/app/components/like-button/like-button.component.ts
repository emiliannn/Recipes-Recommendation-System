import { Component, Input, OnInit } from '@angular/core';
import { trigger, state, style, animate, transition } from '@angular/animations';
import { RecipesService } from '../../services/recipes.service';

@Component({
  selector: 'app-like-button',
  templateUrl: './like-button.component.html',
  styleUrl: './like-button.component.css',
  animations: [
    trigger('heart', [
        state('unliked', style({
            color: '#aeb5ae',
            // opacity: '0.5',
            transform: 'scale(1)'
        })),
        state('liked', style({
            color: '#e74c3c',
            opacity: '1',
            transform: 'scale(1.1)'
        })),
        transition('unliked <=> liked', animate('100ms ease-out'))
    ])
  ]
})
export class LikeButtonComponent implements OnInit {
  user_id:  string = "6678f64d68c8b09fe477b57d";

  @Input() recipe: any | undefined;
  public likeState: string = 'unliked';
  public iconName: string = "favorite_border";

  constructor(private recipesService: RecipesService) { }


  ngOnInit(): void {
    this.checkIfUserLikedRecipe();
  }


  checkIfUserLikedRecipe(){
    this.recipesService.checkIfUserLikedRecipe(this.user_id, this.recipe.id).subscribe((data) => {
      if(data.userLiked) {
        this.likeState = 'liked';
        this.iconName = "favorite";
      } else {
        this.likeState = 'unliked';
        this.iconName = "favorite_border";
      }
    });
  }


  toggleLikeState(){
    if(this.likeState == 'unliked'){
      this.likeState = 'liked';
      this.iconName = "favorite";
      this.recipesService.save_user_recipe(this.user_id, this.recipe.id).subscribe((data) => {
        console.log('Data has been unsaved. ', data);});
    } else {
      this.likeState = 'unliked';
      this.iconName = "favorite_border";
      this.recipesService.unsave_user_recipe(this.user_id, this.recipe.id).subscribe((data) => {  
        console.log('Data has been saved. ', data);
    });
  }

  }

}