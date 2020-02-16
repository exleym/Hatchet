import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';

import { TitleService } from '../../../services/title.service';
import { Team } from '../../../models/team';
import { TeamService } from '../../../services/team.service';
import { Game } from '../../../models/game';
import { Record } from '../../../models/record';
import {Observable, Subject} from 'rxjs';
import {WeekService} from '../../../services/week.service';
import {FormBuilder} from '@angular/forms';

@Component({
  selector: 'app-team-detail',
  templateUrl: './team-detail.component.html',
  styleUrls: ['./team-detail.component.scss']
})
export class TeamDetailComponent implements OnInit {

  private teamId: number;
  currentSeason: number;
  team: Team;
  games$: Observable<Game[]>;
  record$: Observable<Record>;
  activeGame: Game;
  editTeam = false;
  availableSeasons: number[];
  verbose: boolean;
  submitted = false;
  teamSubject: Subject<Team>;

  constructor(
    private route: ActivatedRoute,
    public titleService: TitleService,
    private teamService: TeamService,
    private _weekService: WeekService,
    private location: Location,
  ) { }

  ngOnInit() {
    this.verbose = true;
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
    this.teamService.getTeam(this.teamId)
      .subscribe(team => this.team = team);
  }

  setTeamId(): void {
    this.teamId = +this.route.snapshot.paramMap.get('id');
  }

  setGames(season?: number): void {
    this.teamService.getTeamGames(this.teamId, season)
      .pipe(game => this.games$ = game);
  }

  setRecord(season?: number): void {
    this.teamService.getTeamRecord(this.teamId, season)
      .pipe(record => this.record$ = record);
  }

  setPageTitle(): void {
    this.titleService.setTitle('Team Details');
  }

  toggleEditor(): void {
    this.editTeam = this.editTeam === false;
  }

  onTeamEditSubmit(team: Team): void {
    this.toggleEditor();
    this.teamService.updateTeam(team)
      .subscribe(t => this.team = t);
    this.submitted = true;
  }

  goBack(): void {
    this.location.back();
  }

  setActiveGame(game: Game): void {
    this.activeGame = game;
  }
}
