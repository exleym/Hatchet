import { Component, OnInit } from '@angular/core';

import { Team } from './team';
import { TeamService } from '../team.service';
import { TitleService } from '../title.service';

@Component({
  selector: 'app-teams',
  templateUrl: './teams.component.html',
  styleUrls: ['./teams.component.scss']
})
export class TeamsComponent implements OnInit {
  teams: Team[];

  constructor(public titleService: TitleService,
              private _teamService: TeamService) { }

  ngOnInit() {
    this.titleService.setTitle('Teams Manager');
    this._teamService.getTeams()
      .subscribe(teams => this.teams = teams);
  }

}
