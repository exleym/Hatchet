import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MasterSearchComponent } from './components/master-search/master-search.component';
import { NavbarComponent } from './components/navbar/navbar.component';
import { SidebarComponent } from './components/sidebar/sidebar.component';
import {RouterModule} from '@angular/router';

@NgModule({
  declarations: [
    MasterSearchComponent,
    NavbarComponent,
    SidebarComponent
  ],
  imports: [
    CommonModule,
    RouterModule
  ],
  exports: [
    NavbarComponent,
    SidebarComponent,
    RouterModule
  ]
})
export class UiModule { }
