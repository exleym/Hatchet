import { Injectable } from '@angular/core';
import { map } from 'rxjs/operators';
import { Observable } from 'rxjs';
import {HttpClient} from '@angular/common/http';

import { Bookmaker } from '../models/bookmaker';
import { EnvironmentService } from './environment.service';

@Injectable({
  providedIn: 'root'
})
export class BookmakerService {

  baseUrl: string;

  constructor(
    private _http: HttpClient,
    private es: EnvironmentService
  ) {
    this.setBaseUrl('bookmakers');
  }

  getBookmakers(): Observable<Bookmaker[]> {
    return this._http.get<Bookmaker[]>(this.baseUrl)
      .pipe(map(result => {
        return result.map(item => {
          return new Bookmaker(item);
        });
      }));
  }

  setBaseUrl(context: string) {
    if (!this.baseUrl) {
      if (this.es.config) {
        this.baseUrl = `${this.es.config.hatchetUrl}/${context}`;
      }
    }
  }
}
