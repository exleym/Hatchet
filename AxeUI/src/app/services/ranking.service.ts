import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { Ranking } from '../models/ranking';
import { EnvironmentService } from './environment.service';

@Injectable({
  providedIn: 'root'
})
export class RankingService {

  baseUrl: string;

  constructor(
    private _http: HttpClient,
    private es: EnvironmentService
  ) {
    this.setBaseUrl('polls');
  }

  getRankings(weekId: number, pollId: number): Observable<Ranking[]> {
    const url = `${this.baseUrl}/${pollId}/rankings/week/${weekId}`;
    return this._http.get<Ranking[]>(url)
      .pipe(map(result => {
        return result.map(item => {
          return new Ranking(item);
        });
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
