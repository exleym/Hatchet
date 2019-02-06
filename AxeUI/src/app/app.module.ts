import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';


import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NavbarComponent } from './navbar/navbar.component';
import { SidebarComponent } from './sidebar/sidebar.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { ConferencesComponent } from './conferences/conferences.component';
import { DivisionsComponent } from './divisions/divisions.component';
import { CardComponent } from './card/card.component';

import { ConferenceService } from './conference.service';
import { TitleService } from './title.service';
import { TeamsComponent } from './teams/teams.component';
import { ConferenceDetailComponent } from './conference-detail/conference-detail.component';
import { TeamDetailComponent } from './team-detail/team-detail.component';

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    SidebarComponent,
    DashboardComponent,
    ConferencesComponent,
    DivisionsComponent,
    CardComponent,
    TeamsComponent,
    ConferenceDetailComponent,
    TeamDetailComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
