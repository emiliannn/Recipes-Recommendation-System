import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RecipesListItemBasedComponent } from './recipes-list-item-based.component';

describe('RecipesListItemBasedComponent', () => {
  let component: RecipesListItemBasedComponent;
  let fixture: ComponentFixture<RecipesListItemBasedComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [RecipesListItemBasedComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(RecipesListItemBasedComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
