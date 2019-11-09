import { Injectable } from '@angular/core';
import { Week } from '../models/week';
import {HttpClient, HttpParams} from '@angular/common/http';
import {Observable} from 'rxjs';
import {map} from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class WeekService {

  baseUrl = 'http://localhost:5000/api/v1/weeks';

  constructor(private _http: HttpClient) { }

  getWeeks(season: number): Observable<Week[]> {
    const params = new HttpParams().set('season', season.toString());
    return this._http.get<Week[]>(this.baseUrl, { params })
      .pipe(map(result => {
        return result.map(item => {
          return new Week(item);
        });
      }));
  }
}
