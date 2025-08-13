import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { RecipesListContentBasedComponent } from './components/recipes-list-content-based/recipes-list-content-based.component';
import { AppComponent } from './app.component';
import { RecipesListsComponent } from './components/recipes-lists/recipes-lists.component';

const routes: Routes = [
  { path: 'recipesListContentBased', component: RecipesListContentBasedComponent },
  { path: 'recipesLists', component: RecipesListsComponent },
  { path: '', redirectTo: '/recipesLists', pathMatch: 'full' },

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
