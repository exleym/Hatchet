import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { FormBuilder, ReactiveFormsModule } from '@angular/forms';
import { NgxSmartModalModule } from 'ngx-smart-modal';
import { UiModule } from './ui/ui.module';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { DashboardComponent } from './ui/components/dashboard/dashboard.component';
import { ConferencesComponent } from './components/conferences/conference-master/conferences.component';
import { DivisionsComponent } from './components/divisions/divisions.component';
import { CardComponent } from './ui/components/card/card.component';
import { GamesComponent } from './components/games/games.component';

import { ConferenceService } from './services/conference.service';
import { TitleService } from './services/title.service';
import { NavbarComponent } from './components/generic/navbar/navbar.component';
import { SidebarComponent } from './components/generic/sidebar/sidebar.component';
import { MasterSearchComponent } from './components/generic/master-search/master-search.component';
import { TeamMasterComponent } from './components/teams/team-master/team-master.component';
import { ConferenceDetailComponent } from './components/conferences/conference-detail/conference-detail.component';
import { TeamDetailComponent } from './components/teams/team-detail/team-detail.component';
import { ScheduleComponent } from './components/schedule/schedule.component';
import { ScheduleItemComponent } from './components/schedule-item/schedule-item.component';
import { CreateGameComponent } from './components/create-game/create-game.component';
import { CreateConferenceComponent } from './components/conferences/create-conference/create-conference.component';
import { StadiumMasterComponent } from './components/stadiums/stadium-master/stadium-master.component';
import { StadiumDetailComponent } from './components/stadiums/stadium-detail/stadium-detail.component';
import { RankingsMasterComponent } from './components/rankings/rankings-master/rankings-master.component';
import { WeeklyRankingComponent } from './components/rankings/weekly-ranking/weekly-ranking.component';
import { GamblingMasterComponent } from './components/gambling/gambling-master/gambling-master.component';
import { LiveBetsComponent } from './components/gambling/live-bets/live-bets.component';
import { BetsHistoryComponent } from './components/gambling/bets-history/bets-history.component';
import { BetCreatorComponent } from './components/gambling/bet-creator/bet-creator.component';

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    SidebarComponent,
    MasterSearchComponent,
    DashboardComponent,
    ConferencesComponent,
    DivisionsComponent,
    GamesComponent,
    CardComponent,
    TeamMasterComponent,
    ConferenceDetailComponent,
    TeamDetailComponent,
    ScheduleComponent,
    ScheduleItemComponent,
    CreateGameComponent,
    CreateConferenceComponent,
    StadiumMasterComponent,
    StadiumDetailComponent,
    RankingsMasterComponent,
    WeeklyRankingComponent,
    GamblingMasterComponent,
    LiveBetsComponent,
    BetsHistoryComponent,
    BetCreatorComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    ReactiveFormsModule,
    NgxSmartModalModule.forRoot(),
    UiModule,
  ],
  providers: [FormBuilder],
  bootstrap: [AppComponent]
})
export class AppModule { }
