import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { map } from 'rxjs/operators';
import {Observable} from 'rxjs';

import { Stadium } from '../models/stadium';
import {EnvironmentService} from './environment.service';

@Injectable({
  providedIn: 'root'
})
export class StadiumService {

  stadiums: Stadium[];
  baseUrl: string;

  constructor(
    private _http: HttpClient,
    private es: EnvironmentService
  ) {
    this.setBaseUrl('stadiums');
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
    return this._http.get<Stadium>(`${this.baseUrl}/${stadiumId}`)
      .pipe(map(result => {
        return new Stadium(result);
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
