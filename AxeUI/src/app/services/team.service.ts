import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders, HttpParams} from '@angular/common/http';
import { map } from 'rxjs/operators';
import {Observable} from 'rxjs';

import {Team} from '../models/team';
import {Game} from '../models/game';
import {Record} from '../models/record';


@Injectable({
  providedIn: 'root'
})
export class TeamService {
  teamsUrl = 'http://localhost:5000/api/v1/teams';
  teams: Team[];

  constructor(private _http: HttpClient) {
    this.getTeams()
      .subscribe((teams) => {
        this.teams = teams;
      });
  }

  getTeams(): Observable<Team[]> {
    return this._http.get<Team[]>(this.teamsUrl)
      .pipe(map(result => {
        return result.map(item => {
          return new Team(item);
        });
      }));
  }

  getTeam(id: number): Observable<Team> {
    const url = `${this.teamsUrl}/${id}`;
    return this._http.get<Team>(url)
      .pipe(map(result => {
        return new Team(result);
      }));
  }

  getTeamGames(teamId: number, season?: number): Observable<Game[]> {
    let params = new HttpParams();
    if (season != null) {
     params = params.set('season', season.toString());
    }
    const url = `${this.teamsUrl}/${teamId}/games`;
    return this._http.get<any>(url, { params })
      .pipe(map(result => {
        return result.map(item => {
          return new Game(item);
        });
      }));
  }

  getTeamRecord(teamId: number): Observable<Record> {
    const url = `${this.teamsUrl}/${teamId}/record`;
    return this._http.get<any>(url)
      .pipe(map(result => {
        return new Record(result);
      }));
  }

}
