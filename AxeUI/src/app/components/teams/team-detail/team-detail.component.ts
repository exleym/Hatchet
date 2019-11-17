import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';

import { TitleService } from '../../../services/title.service';
import { Team } from '../../../models/team';
import { TeamService } from '../../../services/team.service';
import { Game } from '../../../models/game';
import { Record } from '../../../models/record';
import { Observable } from 'rxjs';
import {WeekService} from '../../../services/week.service';

@Component({
  selector: 'app-team-detail',
  templateUrl: './team-detail.component.html',
  styleUrls: ['./team-detail.component.scss']
})
export class TeamDetailComponent implements OnInit {

  private teamId: number;
  currentSeason: number;
  team$: Observable<Team>;
  games$: Observable<Game[]>;
  record$: Observable<Record>;
  activeGame: Game;
  availableSeasons: number[];

  constructor(private route: ActivatedRoute,
              public titleService: TitleService,
              private _teamService: TeamService,
              private _weekService: WeekService,
              private location: Location) { }

  ngOnInit() {
    this.currentSeason = 2019;
    this.setTeamId();
    this.getTeam();
    this.setPageTitle();
    this.setGames(this.currentSeason);
    this.setRecord();
    this.setAvailableSeasons();
  }

  setAvailableSeasons(): void {
    this._weekService.getSeasons()
      .subscribe(seasons => {
        this.availableSeasons = seasons;
      });
  }

  setSeason(season: number): void {
    this.currentSeason = season;
    this.setGames(this.currentSeason);
    this.setRecord(this.currentSeason);
  }

  getTeam(): void {
    this._teamService.getTeam(this.teamId)
      .pipe(team => this.team$ = team);
  }

  setTeamId(): void {
    this.teamId = +this.route.snapshot.paramMap.get('id');
  }

  setGames(season?: number): void {
    this._teamService.getTeamGames(this.teamId, season)
      .pipe(game => this.games$ = game);
  }

  setRecord(season?: number): void {
    this._teamService.getTeamRecord(this.teamId, season)
      .pipe(record => this.record$ = record);
  }

  setPageTitle(): void {
    this.titleService.setTitle('Team Details');
  }

  goBack(): void {
    this.location.back();
  }

  setActiveGame(game: Game): void {
    this.activeGame = game;
  }

}
