import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { map } from 'rxjs/operators';
import {Observable} from 'rxjs';

import { Conference } from '../models/conference';
import { Team } from '../models/team';

@Injectable({
  providedIn: 'root'
})
export class ConferenceService {
  conferencesUrl = 'http://localhost:5000/api/v1/conferences';

  constructor(private _http: HttpClient) { }

  getConferences(): Observable<Conference[]> {
    return this._http.get<Conference[]>(this.conferencesUrl)
      .pipe(map(result => {
        return result.map(item => {
          return new Conference(item);
        });
      }));
  }

  getConference(id: number): Observable<Conference> {
    const url = this._conferenceUrl(id);
    return this._http.get<Conference>(url)
      .pipe(map(result => {
        return new Conference(result);
      }));
  }

  getConferenceMembers(id: number): Observable<Team[]> {
    return this._http.get<Team[]>(this._conferenceMembersUrl(id))
      .pipe(map(result => {
        return result.map(item => new Team(item));
      }));
  }

  createConference(conference: Conference): Observable<Conference> {
    const url = this.conferencesUrl;
    return this._http.post<Conference>(url, conference)
      .pipe(map(resp => new Conference(resp)));
  }

  updateConference(conference: Conference): Observable<Conference> {
    const url = this._conferenceUrl(conference.id);
    return this._http.put<Conference>(url, conference)
      .pipe(map(resp => new Conference(resp)));
  }

  deleteConference(conference: Conference): Observable<any> {
    const url = this._conferenceUrl(conference.id);;
    return this._http.delete<any>(url);
  }

  _conferenceUrl(id: number): string {
    return `${this.conferencesUrl}/${id}`
  }

  _conferenceMembersUrl(id: number): string {
    return `${this.conferencesUrl}/${id}/teams`;
  }

}
