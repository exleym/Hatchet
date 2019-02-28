import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { map } from 'rxjs/operators';
import { Observable } from 'rxjs';


import {Team} from '../models/team';
import {Game} from '../models/game';

@Injectable({
  providedIn: 'root'
})
export class TeamService {
  teamsUrl = 'http://localhost:5000/api/v1/teams';

  constructor(private _http: HttpClient) { }

  getTeams(): Observable<Team[]> {
    return this._http.get<Team[]>(this.teamsUrl)
      .pipe(map(result => {
        return result.map(item => {
          return new Team(item);
        });
      }));
  }

  getTeam(id: number): Observable<Team> {
    return this._http.get<Team>(this.teamsUrl + '/' + id)
      .pipe(map(result => {
        return new Team(result);
      }));
  }

  getTeamGames(teamId: number): Observable<Game[]> {
    return this._http.get<any>(this.teamsUrl + '/' + teamId + '/games')
      .pipe(map(result => {
        return result.map(item => {
          return new Game(item);
        });
      }));
  }

}
