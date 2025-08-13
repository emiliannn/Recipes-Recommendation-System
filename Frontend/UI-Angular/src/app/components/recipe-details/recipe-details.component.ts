import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { Router } from '@angular/router';

@Component({
  selector: 'app-recipe-details',
  templateUrl: './recipe-details.component.html',
  styleUrl: './recipe-details.component.css'
})
export class RecipeDetailsComponent {
  recipe: any | undefined;
  user_id:  string = "6678f64d68c8b09fe477b57d";

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any,
    private dialogRef: MatDialogRef<RecipeDetailsComponent>,
    private router: Router
  ) {
    this.recipe = data.recipe;
  }

  close(): void {
    this.dialogRef.close();
  }
}
