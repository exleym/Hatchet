import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { TitleService } from '../title.service';
import { Team } from '../teams/team';
import { TeamService } from '../team.service';

@Component({
  selector: 'app-team-detail',
  templateUrl: './team-detail.component.html',
  styleUrls: ['./team-detail.component.scss']
})
export class TeamDetailComponent implements OnInit {

  private teamId: number;
  team: Team;

  constructor(private route: ActivatedRoute,
              public titleService: TitleService,
              private _teamService: TeamService) { }

  ngOnInit() {
    this.setTeamId();
    this.getTeam();
    this.setPageTitle();
  }

  getTeam(): void {
    this._teamService.getTeam(this.teamId)
      .subscribe(team => this.team = team);
  }

  setTeamId(): void {
    this.teamId = +this.route.snapshot.paramMap.get('id');
  }

  setPageTitle(): void {
    this.titleService.setTitle(this.team.shortName);
  }

}
