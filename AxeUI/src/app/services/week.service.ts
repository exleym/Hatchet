import { Injectable } from '@angular/core';
import { Week } from '../models/week';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { EnvironmentService } from './environment.service';

@Injectable({
  providedIn: 'root'
})
export class WeekService {

  baseUrl: string;
  context: '/weeks';

  constructor(
    private _http: HttpClient,
    private es: EnvironmentService
  ) {
    this.setBaseUrl('weeks');
  }

  getWeeks(season: number): Observable<Week[]> {
    const url = this.newUrl();
    const params = new HttpParams().set('season', season.toString());
    return this._http.get<Week[]>(url, { params })
      .pipe(map(result => {
        return result.map(item => {
          return new Week(item);
        });
      }));
  }

  getSeasons(): Observable<number[]> {
    return this._http.get<number[]>(this.newUrl('/seasons'));
  }

  private setBaseUrl(context: string) {
    if (!this.baseUrl) {
      if (this.es.config) {
        this.baseUrl = `${this.es.config.hatchetUrl}${context}`;
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
