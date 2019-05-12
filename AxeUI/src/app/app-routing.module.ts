import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { DashboardComponent } from './ui/components/dashboard/dashboard.component';
import { ConferencesComponent } from './components/conferences/conference-master/conferences.component';
import { DivisionsComponent } from './components/divisions/divisions.component';
import { ConferenceDetailComponent } from './components/conferences/conference-detail/conference-detail.component';
import { TeamsComponent } from './components/teams/teams.component';
import { TeamDetailComponent } from './components/team-detail/team-detail.component';

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
