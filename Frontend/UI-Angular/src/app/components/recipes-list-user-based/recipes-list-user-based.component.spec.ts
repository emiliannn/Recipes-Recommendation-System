import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RecipesListUserBasedComponent } from './recipes-list-user-based.component';

describe('RecipesListUserBasedComponent', () => {
  let component: RecipesListUserBasedComponent;
  let fixture: ComponentFixture<RecipesListUserBasedComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [RecipesListUserBasedComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(RecipesListUserBasedComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
