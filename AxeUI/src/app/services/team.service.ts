import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders, HttpParams} from '@angular/common/http';
import { map } from 'rxjs/operators';
import {Observable} from 'rxjs';

import {Team} from '../models/team';
import {Game} from '../models/game';
import {Record} from '../models/record';
import {EnvironmentService} from './environment.service';


@Injectable({
  providedIn: 'root'
})
export class TeamService {

  baseUrl: string;
  context = '/teams';

  constructor(
    private es: EnvironmentService,
    private _http: HttpClient
  ) {
    this.setBaseUrl('teams');
  }

  getTeams(): Observable<Team[]> {
    return this._http.get<Team[]>(this.baseUrl)
      .pipe(map(result => {
        return result.map(item => {
          return new Team(item);
        });
      }));
  }

  getTeam(teamId: number): Observable<Team> {
    const url = `${this.baseUrl}/${teamId}`;
    return this._http.get<Team>(url)
      .pipe(map(result => {
        return new Team(result);
      }));
  }

  updateTeam(team: Team): Observable<Team> {
    const url = `${this.baseUrl}/${team.id}`;
    console.log(url);
    return this._http.put<Team>(url, team)
      .pipe(map(result => {
        return new Team(result);
      }));
  }

  getTeamGames(teamId: number, season?: number): Observable<Game[]> {
    let params = new HttpParams();
    if (season != null) {
     params = params.set('season', season.toString());
    }
    const url = `${this.baseUrl}/${teamId}/games`;
    return this._http.get<any>(url, { params })
      .pipe(map(result => {
        return result.map(item => {
          return new Game(item);
        });
      }));
  }

  getTeamRecord(teamId: number, season?: number): Observable<Record> {
    let params = new HttpParams();
    if (season != null) {
      params = params.set('season', season.toString());
    }
    const url = `${this.baseUrl}/${teamId}/record`;
    return this._http.get<any>(url, {params})
      .pipe(map(result => {
        return new Record(result);
      }));
  }

  setBaseUrl(context: string) {
    if (!this.baseUrl) {
      if (this.es.config) {
        this.baseUrl = `${this.es.config.hatchetUrl}/${context}`;
      }
    }
  }

  private newUrl(context?: string) {
    if (!this.baseUrl) {
      this.setBaseUrl(this.context);
    }
    if (!context) {
      return this.baseUrl;
    }
    return `${this.baseUrl}${context}`;
  }
}
