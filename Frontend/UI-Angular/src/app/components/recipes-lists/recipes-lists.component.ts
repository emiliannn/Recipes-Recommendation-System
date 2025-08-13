import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { Location } from '@angular/common'; 

@Component({
  selector: 'app-recipes-lists',
  templateUrl: './recipes-lists.component.html',
  styleUrl: './recipes-lists.component.css'
})
export class RecipesListsComponent {
  constructor(public router: Router , private location: Location) {
}

}