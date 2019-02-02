import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { DashboardComponent } from './dashboard/dashboard.component';
import { ConferencesComponent } from './conferences/conferences.component';
import { DivisionsComponent } from './divisions/divisions.component';

const routes: Routes = [
  { path: 'dashboard', component: DashboardComponent },
  { path: 'conferences', component: ConferencesComponent },
  { path: 'divisions', component: DivisionsComponent },
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
