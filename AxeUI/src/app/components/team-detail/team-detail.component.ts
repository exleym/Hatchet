import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';

import { TitleService } from '../../services/title.service';
import { Team } from '../../models/team';
import { TeamService } from '../../services/team.service';
import { Game } from '../../models/game';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-team-detail',
  templateUrl: './team-detail.component.html',
  styleUrls: ['./team-detail.component.scss']
})
export class TeamDetailComponent implements OnInit {

  private teamId: number;
  team$: Observable<Team>;
  games$: Observable<Game[]>;

  constructor(private route: ActivatedRoute,
              public titleService: TitleService,
              private _teamService: TeamService,
              private location: Location) { }

  ngOnInit() {
    this.setTeamId();
    this.getTeam();
    // this.setPageTitle();
    this.setGames();
    console.log(this.games$);
  }

  getTeam(): void {
    this._teamService.getTeam(this.teamId)
      .pipe(team => this.team$ = team);
  }

  setTeamId(): void {
    this.teamId = +this.route.snapshot.paramMap.get('id');
  }

  setGames(): void {
    this._teamService.getTeamGames(this.teamId)
      .pipe(game => this.games$ = game);
  }

  goBack(): void {
    this.location.back();
  }

}
