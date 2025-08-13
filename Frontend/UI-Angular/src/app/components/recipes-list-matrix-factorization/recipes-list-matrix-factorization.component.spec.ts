import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RecipesListMatrixFactorizationComponent } from './recipes-list-matrix-factorization.component';

describe('RecipesListMatrixFactorizationComponent', () => {
  let component: RecipesListMatrixFactorizationComponent;
  let fixture: ComponentFixture<RecipesListMatrixFactorizationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [RecipesListMatrixFactorizationComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(RecipesListMatrixFactorizationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
