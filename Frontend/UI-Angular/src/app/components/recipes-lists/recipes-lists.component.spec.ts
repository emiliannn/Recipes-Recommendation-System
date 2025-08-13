import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RecipesListsComponent } from './recipes-lists.component';

describe('RecipesListsComponent', () => {
  let component: RecipesListsComponent;
  let fixture: ComponentFixture<RecipesListsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [RecipesListsComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(RecipesListsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
