import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { map } from 'rxjs/operators';
import {Observable} from 'rxjs';

import { Conference } from '../models/conference';
import { Team } from '../models/team';
import { EnvironmentService } from './environment.service';

@Injectable({
  providedIn: 'root'
})
export class ConferenceService {

  baseUrl: string;

  constructor(
    private _http: HttpClient,
    private es: EnvironmentService
  ) {
    this.setBaseUrl('conferences');
  }

  getConferences(): Observable<Conference[]> {
    return this._http.get<Conference[]>(this.baseUrl)
      .pipe(map(result => {
        return result.map(item => {
          return new Conference(item);
        });
      }));
  }

  getConference(id: number): Observable<Conference> {
    const url = `${this.baseUrl}/${id}`;
    return this._http.get<Conference>(url)
      .pipe(map(result => {
        return new Conference(result);
      }));
  }

  getConferenceMembers(id: number): Observable<Team[]> {
    const url = `${this.baseUrl}/${id}/teams`;
    return this._http.get<Team[]>(url)
      .pipe(map(result => {
        return result.map(item => new Team(item));
      }));
  }

  createConference(conference: Conference): Observable<Conference> {
    return this._http.post<Conference>(this.baseUrl, conference)
      .pipe(map(resp => new Conference(resp)));
  }

  updateConference(conference: Conference): Observable<Conference> {
    const url = `${this.baseUrl}/${conference.id}`;
    return this._http.put<Conference>(url, conference)
      .pipe(map(resp => new Conference(resp)));
  }

  deleteConference(conference: Conference): Observable<any> {
    const url = `${this.baseUrl}/${conference.id}`;
    return this._http.delete<any>(url);
  }

  setBaseUrl(context: string) {
    if (!this.baseUrl) {
      if (this.es.config) {
        this.baseUrl = `${this.es.config.hatchetUrl}/${context}`;
      }
    }
  }
}
