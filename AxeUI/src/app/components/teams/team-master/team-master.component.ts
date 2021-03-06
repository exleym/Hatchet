import { Component, OnInit } from '@angular/core';

import { Team } from '../../../models/team';
import { TeamService } from '../../../services/team.service';
import { TitleService } from '../../../services/title.service';
import {map} from 'rxjs/operators';

@Component({
  selector: 'app-teams',
  templateUrl: './team-master.component.html',
  styleUrls: ['./team-master.component.scss']
})
export class TeamMasterComponent implements OnInit {
  teams: Team[];

  constructor(public titleService: TitleService,
              private _teamService: TeamService) { }

  ngOnInit() {
    this.titleService.setTitle('Teams Manager');
    this._teamService.getTeams()
      .subscribe((res: Team[]) => this.teams = res);
  }

}
