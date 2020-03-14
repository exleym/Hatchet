import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders, HttpParams} from '@angular/common/http';
import { map } from 'rxjs/operators';
import { Observable } from 'rxjs';


import {Game} from '../models/game';
import {Line} from '../models/line';
import {EnvironmentService} from './environment.service';


@Injectable({
  providedIn: 'root'
})
export class GameService {

  baseUrl: string;

  constructor(
    private _http: HttpClient,
    private es: EnvironmentService
  ) {
    this.setBaseUrl('games');
  }

  getGames(): Observable<Game[]> {
    const url = this.baseUrl;
    return this._http.get<Game[]>(url)
      .pipe(map(result => {
        return result.map(item => {
          return new Game(item);
        });
      }));
  }

  getGame(gameId: number): Observable<Game> {
    const url = `${this.baseUrl}/${gameId}`;
    return this._http.get<Game>(url)
      .pipe(map(result => {
        return new Game(result);
      }));
  }

  createGame(game: Game): Observable<Game> {
    const url = this.baseUrl;
    return this._http.post(url, game)
      .pipe(map(result => {
        return new Game(result);
      }));
  }

  getGameLines(gameId: number, teamId?: number): Observable<Line[]> {
    const url = `${this.es.config.hatchetUrl}/lines`;
    let params = new HttpParams().set('game_id', gameId.toString());
    if (teamId != null) { params = params.set('team_id', teamId.toString()); }
    return this._http.get<Line[]>(url, { params })
      .pipe(map(result => {
        return result.map(x => new Line(x));
      }));
  }

  private setBaseUrl(context: string) {
    if (!this.baseUrl) {
      if (this.es.config) {
        this.baseUrl = `${this.es.config.hatchetUrl}/${context}`;
      }
    }
  }
}
