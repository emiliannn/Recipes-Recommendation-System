import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { RecipeComponent } from './components/recipe/recipe.component';
import { MatToolbarModule  } from '@angular/material/toolbar';
import { MatMenuModule } from '@angular/material/menu';
import { MatTabsModule } from '@angular/material/tabs';
import {MatSelectModule} from '@angular/material/select';
import { MatRadioModule } from '@angular/material/radio';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { DragScrollComponent  } from 'ngx-drag-scroll';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatFormFieldModule  } from '@angular/material/form-field';
import { MatButtonToggleModule }    from '@angular/material/button-toggle';
import { HttpClientModule } from '@angular/common/http';
import { RecipesListUserBasedComponent } from './components/recipes-list-user-based/recipes-list-user-based.component';
import { RecipesListItemBasedComponent } from './components/recipes-list-item-based/recipes-list-item-based.component';
import { RecipesListMatrixFactorizationComponent } from './components/recipes-list-matrix-factorization/recipes-list-matrix-factorization.component';
import { RecipesListContentBasedComponent } from './components/recipes-list-content-based/recipes-list-content-based.component';
import { HeaderComponent } from './components/header/header.component';
import { RecipesListsComponent } from './components/recipes-lists/recipes-lists.component';
import {MatButtonModule} from '@angular/material/button';
import {MatCardModule} from '@angular/material/card';
import {MatProgressBarModule} from '@angular/material/progress-bar';
import {MatChipsModule} from '@angular/material/chips';
import { LikeButtonComponent } from './components/like-button/like-button.component';
import { RecipeDetailsComponent } from './components/recipe-details/recipe-details.component';
import { MatListModule } from '@angular/material/list';
import { ReviewRecipeComponent } from './components/review-recipe/review-recipe.component';
import{ StarRatingModule } from 'angular-star-rating';
import {MatInputModule} from '@angular/material/input';

@NgModule({
  declarations: [
      AppComponent,
      RecipeComponent,
      RecipesListsComponent,
      RecipesListUserBasedComponent,
      RecipesListItemBasedComponent,
      RecipesListMatrixFactorizationComponent,
      RecipesListContentBasedComponent,
      HeaderComponent,
      LikeButtonComponent,
      RecipeDetailsComponent,
      ReviewRecipeComponent,
      
    ],
  imports: [
    HttpClientModule,
    DragScrollComponent,
    NgbModule,
    BrowserModule,
    MatSelectModule,
    AppRoutingModule,
    MatToolbarModule,
    MatMenuModule,
    MatRadioModule,
    MatProgressSpinnerModule,
    ReactiveFormsModule, FormsModule,
    MatIconModule,
    BrowserAnimationsModule,
    MatTabsModule,
    MatFormFieldModule,
    MatButtonToggleModule,
    MatCardModule,
    MatButtonModule,
    MatProgressBarModule,
    MatChipsModule,
    MatListModule,
    StarRatingModule.forRoot(),
    MatInputModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
