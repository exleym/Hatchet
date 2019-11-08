import { Injectable } from '@angular/core';
import { map } from 'rxjs/operators';
import { Observable } from 'rxjs';
import {HttpClient} from '@angular/common/http';

import { Bookmaker } from '../models/bookmaker';

@Injectable({
  providedIn: 'root'
})
export class BookmakerService {
  bookmakersUrl = 'http://localhost:5000/api/v1/bookmakers';

  constructor(private _http: HttpClient) { }

  getBookmakers(): Observable<Bookmaker[]> {
    return this._http.get<Bookmaker[]>(this.bookmakersUrl)
      .pipe(map(result => {
        return result.map(item => {
          return new Bookmaker(item);
        });
      }));
  }
}
