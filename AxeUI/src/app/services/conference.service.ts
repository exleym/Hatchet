import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { map } from 'rxjs/operators';
import {Observable} from 'rxjs';

import { Conference } from '../models/conference';
import {Team} from '../models/team';

@Injectable({
  providedIn: 'root'
})
export class ConferenceService {
  conferencesUrl = 'http://localhost:5000/api/v1/conferences';

  constructor(private _http: HttpClient) { }

  getConferences(): Observable<Conference[]> {
    return this._http.get<Conference[]>(this.conferencesUrl)
      .pipe(map(result => result));
  }

  getConference(id: number): Observable<Conference> {
    return this._http.get<Conference>(this.conferencesUrl + '/' + id)
      .pipe(result => result);
  }

  getConferenceMembers(id: number): Observable<Team[]> {
    return this._http.get<Team[]>(this._conferenceMembersUrl(id));
  }

  _conferenceMembersUrl(id: number): string {
    return this.conferencesUrl + '/' + id + '/members';
  }

}
