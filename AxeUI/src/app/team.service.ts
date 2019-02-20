import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { map } from 'rxjs/operators';
import {Observable} from 'rxjs';

import {Team} from './teams/team';
import {Game} from './game';

@Injectable({
  providedIn: 'root'
})
export class TeamService {
  teamsUrl = 'http://localhost:5000/api/v1/teams';

  constructor(private _http: HttpClient) { }

  getTeams(): Observable<Team[]> {
    return this._http.get<Team[]>(this.teamsUrl)
      .pipe(map(result => result));
  }

  getTeam(id: number): Observable<Team> {
    return this._http.get<Team>(this.teamsUrl + '/' + id)
      .pipe(result => result);
  }

  getTeamGames(teamId: number): Observable<Game[]> {
    return this._http.get<Game[]>(this.teamsUrl + '/' + teamId + '/games')
      .pipe(map(result => result));
  }

}