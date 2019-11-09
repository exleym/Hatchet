import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders, HttpParams} from '@angular/common/http';
import { map } from 'rxjs/operators';
import { Observable } from 'rxjs';


import {Team} from '../models/team';
import {Game} from '../models/game';
import {Line} from '../models/line';


@Injectable({
  providedIn: 'root'
})
export class GameService {
  gamesUrl = 'http://localhost:5000/api/v1/teams';
  linesUrl = 'http://localhost:5000/api/v1/lines';

  constructor(private _http: HttpClient) { }

  getGames(): Observable<Game[]> {
    return this._http.get<Game[]>(this.gamesUrl)
      .pipe(map(result => {
        return result.map(item => {
          return new Game(item);
        });
      }));
  }

  getGame(gameId: number): Observable<Game> {
    return this._http.get<Game>(`${this.gamesUrl}/${gameId}`)
      .pipe(map(result => {
        return new Game(result);
      }));
  }

  createGame(game: Game): Observable<Game> {
    return this._http.post(this.gamesUrl, game)
      .pipe(map(result => {
        return new Game(result);
      }));
  }

  getGameLines(gameId: number, teamId?: number): Observable<Line[]> {
    let params = new HttpParams().set('game_id', gameId.toString());
    if (teamId != null) { params = params.set('team_id', teamId.toString()); }
    return this._http.get<Line[]>(`${this.linesUrl}`, { params })
      .pipe(map(result => {
        return result.map(x => new Line(x));
      }));
  }
}
