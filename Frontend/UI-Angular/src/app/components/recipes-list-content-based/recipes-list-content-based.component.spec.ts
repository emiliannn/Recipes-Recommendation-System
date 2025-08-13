import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RecipesListContentBasedComponent } from './recipes-list-content-based.component';

describe('RecipesListContentBasedComponent', () => {
  let component: RecipesListContentBasedComponent;
  let fixture: ComponentFixture<RecipesListContentBasedComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [RecipesListContentBasedComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(RecipesListContentBasedComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
