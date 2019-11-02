import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { map } from 'rxjs/operators';
import {Observable} from 'rxjs';

import { Stadium } from '../models/stadium';

@Injectable({
  providedIn: 'root'
})
export class StadiumService {

  baseUrl = 'http://localhost:5000/api/v1/stadiums';
  stadiums: Stadium[];

  constructor(private _http: HttpClient) {
    this.getStadiums()
      .subscribe((stadiums) => {
        this.stadiums = stadiums;
      });
  }

  getStadiums(): Observable<Stadium[]> {
    return this._http.get<Stadium[]>(this.baseUrl)
      .pipe(map(result => {
        return result.map(item => {
          return new Stadium(item);
        });
      }));
  }

  getStadium(stadiumId): Observable<Stadium> {
    const url = `${this.baseUrl}/${stadiumId}`;
    return this._http.get<Stadium>(url)
      .pipe(map(result => {
        return new Stadium(result);
      }));
  }
}
