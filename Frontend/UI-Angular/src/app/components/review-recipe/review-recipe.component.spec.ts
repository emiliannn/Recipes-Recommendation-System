import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ReviewRecipeComponent } from './review-recipe.component';

describe('ReviewRecipeComponent', () => {
  let component: ReviewRecipeComponent;
  let fixture: ComponentFixture<ReviewRecipeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ReviewRecipeComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ReviewRecipeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
