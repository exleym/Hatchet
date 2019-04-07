import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { map } from 'rxjs/operators';
import { Observable } from 'rxjs';


import {Team} from '../models/team';
import {Game} from '../models/game';

@Injectable({
  providedIn: 'root'
})
export class GameService {
  gamesUrl = 'http://localhost:5000/api/v1/teams';

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
}
