import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { DashboardComponent } from './dashboard/dashboard.component';
import { ConferencesComponent } from './conferences/conferences.component';
import { DivisionsComponent } from './divisions/divisions.component';
import { ConferenceDetailComponent } from './conference-detail/conference-detail.component';
import { TeamsComponent } from './teams/teams.component';
import { TeamDetailComponent } from './team-detail/team-detail.component';

const routes: Routes = [
  { path: 'dashboard', component: DashboardComponent },
  { path: 'conferences', component: ConferencesComponent },
  { path: 'conferences/:id', component: ConferenceDetailComponent },
  { path: 'divisions', component: DivisionsComponent },
  { path: 'teams', component: TeamsComponent },
  { path: 'teams/:id', component: TeamDetailComponent},
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
