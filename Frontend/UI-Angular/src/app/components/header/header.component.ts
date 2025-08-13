import { AfterViewInit, Component, OnChanges, OnDestroy, OnInit } from '@angular/core';
import { MatIconModule, MatIconRegistry } from '@angular/material/icon';
import { DomSanitizer } from '@angular/platform-browser';
import { MatDialog } from '@angular/material/dialog';
import { ActivatedRoute, NavigationEnd, Router } from '@angular/router';
import { MatDividerModule } from '@angular/material/divider';
import { MatButtonModule } from '@angular/material/button';
import { Subscription } from 'rxjs';
import { Location } from '@angular/common'; // Import the Location class from '@angular/common'
import { filter } from 'rxjs/operators';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrl: './header.component.css'
})
export class HeaderComponent implements OnInit, OnDestroy{
  constructor( private activatedRoute: ActivatedRoute, private dialog: MatDialog, private location: Location, private iconRegistry: MatIconRegistry, private sanitizer: DomSanitizer, public router: Router) {

  }
  
  title = 'UI-Angular';
  currentRoute: string = '';
  targetRoute: string = '/recipesLists' || ''; 
  isDifferentRoute: boolean = true;
  private routeSubscription!: Subscription;
  response: any;
  showBackButton = true;

  ngOnInit() {
    this.routeSubscription = this.router.events.pipe(
      filter(event => event instanceof NavigationEnd)
    ).subscribe(() => {
      this.checkRoute();
    });
  }

  private checkRoute(): void {
    this.currentRoute = this.router.url;
    this.showBackButton = true ? this.currentRoute !== this.targetRoute : false;
  }
  
  ngOnDestroy(): void {
    if (this.routeSubscription) {
      this.routeSubscription.unsubscribe();
    }
  }

  navigateBack(): void {
    this.router.navigate(['/recipesLists']);
  }

}

