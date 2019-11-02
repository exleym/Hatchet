import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { DashboardComponent } from './ui/components/dashboard/dashboard.component';
import { ConferencesComponent } from './components/conferences/conference-master/conferences.component';
import { DivisionsComponent } from './components/divisions/divisions.component';
import { ConferenceDetailComponent } from './components/conferences/conference-detail/conference-detail.component';
import { TeamMasterComponent } from './components/teams/team-master/team-master.component';
import { TeamDetailComponent } from './components/teams/team-detail/team-detail.component';
import { StadiumMasterComponent } from './components/stadiums/stadium-master/stadium-master.component';
import { StadiumDetailComponent } from './components/stadiums/stadium-detail/stadium-detail.component';
import { RankingsMasterComponent } from './components/rankings/rankings-master/rankings-master.component';
import {GamblingMasterComponent} from './components/gambling/gambling-master/gambling-master.component';

const routes: Routes = [
  { path: 'dashboard', component: DashboardComponent },
  { path: 'conferences', component: ConferencesComponent },
  { path: 'conferences/:id', component: ConferenceDetailComponent },
  { path: 'divisions', component: DivisionsComponent },
  { path: 'teams', component: TeamMasterComponent },
  { path: 'teams/:id', component: TeamDetailComponent},
  { path: 'stadiums', component: StadiumMasterComponent},
  { path: 'stadiums/:id', component: StadiumDetailComponent },
  { path: 'rankings', component: RankingsMasterComponent },
  { path: 'gambling', component: GamblingMasterComponent },
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
