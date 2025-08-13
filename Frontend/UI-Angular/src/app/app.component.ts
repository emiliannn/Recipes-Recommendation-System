import { AfterViewInit, Component, OnDestroy, OnInit } from '@angular/core';
import { MatIconModule, MatIconRegistry } from '@angular/material/icon';
import { DomSanitizer } from '@angular/platform-browser';
import { MatDialog } from '@angular/material/dialog';
import { NavigationEnd, Router } from '@angular/router';
import {MatDividerModule} from '@angular/material/divider';
import {MatButtonModule} from '@angular/material/button';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',

})
export class AppComponent implements OnInit, OnDestroy , AfterViewInit{
  showComponents: boolean = true;
  routerSubscription: Subscription | undefined;
  
  
  constructor(private dialog: MatDialog, private iconRegistry: MatIconRegistry, private sanitizer: DomSanitizer, public router: Router) {


  }

  ngOnInit() {
    this.routerSubscription = this.router.events.subscribe(event => {
      if (event instanceof NavigationEnd) {
        this.showComponents = !event.url.includes('/recipesListContentBased');
      }
    });
  }

  ngOnDestroy() {
    if (this.routerSubscription) {
      this.routerSubscription.unsubscribe();
    }
  }
  
  ngAfterViewInit(): void {
  }
  

  // openAddItemPopup(item: string){
  //   this.dialog.open(AddItemComponent, {
  //     width: '45em',
  //     height: '35em',
  //     data: item
  // })}

//   fetchUser(id: string) {
//     this.ct.getUser(id)
//      .subscribe(
//        data => {
//            if (data !== undefined) 
//              this.user = data;
//       }
//      )
//  } 
 


}
