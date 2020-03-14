import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';

export interface Config {
  env: string;
  hatchetUrl: string;
}

@Injectable({
  providedIn: 'root'
})
export class EnvironmentService {

  config: Config;

  constructor(
    private http: HttpClient
  ) { }

  initConfigService() {
    // this.http.get<Config>('/conf/config.json').toPromise().then(x => this.config = x);
    this.config = {env: 'local', hatchetUrl: 'http://localhost:8000/api/v1'};
  }

}
