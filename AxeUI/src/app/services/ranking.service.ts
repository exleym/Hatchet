import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { Ranking } from '../models/ranking';

@Injectable({
  providedIn: 'root'
})
export class RankingService {

  baseUrl = 'http://localhost:5000/api/v1/polls';

  constructor(private _http: HttpClient) { }

  getRankings(weekId: number, pollId: number): Observable<Ranking[]> {
    const url = `${this.baseUrl}/${pollId}/rankings/week/${weekId}`
    return this._http.get<Ranking[]>(url)
      .pipe(map(result => {
        return result.map(item => {
          return new Ranking(item);
        });
      }));
  }

}
