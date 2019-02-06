import { Component, OnInit } from '@angular/core';
import { ConferenceService } from '../conference.service';
import { Conference } from './conference';
import { TitleService } from '../title.service';

@Component({
  selector: 'app-conferences',
  templateUrl: './conferences.component.html',
  styleUrls: ['./conferences.component.scss']
})
export class ConferencesComponent implements OnInit {
  conferences: Conference[];

  constructor(private _conference: ConferenceService,
              public titleService: TitleService) { }

  ngOnInit() {
    this.titleService.setTitle('Conference Manager');
    this._conference.getConferences()
      .subscribe(conferences => this.conferences = conferences);
  }
}
