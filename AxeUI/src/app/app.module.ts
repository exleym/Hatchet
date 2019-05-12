import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { FormBuilder, ReactiveFormsModule } from '@angular/forms';
import { NgxSmartModalModule } from 'ngx-smart-modal';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NavbarComponent } from './ui/components/navbar/navbar.component';
import { SidebarComponent } from './ui/components/sidebar/sidebar.component';
import { DashboardComponent } from './ui/components/dashboard/dashboard.component';
import { ConferencesComponent } from './components/conferences/conference-master/conferences.component';
import { DivisionsComponent } from './components/divisions/divisions.component';
import { CardComponent } from './ui/components/card/card.component';
import { GamesComponent } from './components/games/games.component';

import { ConferenceService } from './services/conference.service';
import { TitleService } from './services/title.service';
import { TeamsComponent } from './components/teams/teams.component';
import { ConferenceDetailComponent } from './components/conferences/conference-detail/conference-detail.component';
import { TeamDetailComponent } from './components/team-detail/team-detail.component';
import { ScheduleComponent } from './components/schedule/schedule.component';
import { ScheduleItemComponent } from './components/schedule-item/schedule-item.component';
import { CreateGameComponent } from './components/create-game/create-game.component';
import { CreateConferenceComponent } from './components/conferences/create-conference/create-conference.component';

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    SidebarComponent,
    DashboardComponent,
    ConferencesComponent,
    DivisionsComponent,
    GamesComponent,
    CardComponent,
    TeamsComponent,
    ConferenceDetailComponent,
    TeamDetailComponent,
    ScheduleComponent,
    ScheduleItemComponent,
    CreateGameComponent,
    CreateConferenceComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    ReactiveFormsModule,
    NgxSmartModalModule.forRoot(),
  ],
  providers: [FormBuilder],
  bootstrap: [AppComponent]
})
export class AppModule { }
