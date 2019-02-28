import { Component, OnInit } from '@angular/core';
import { ConferenceService } from '../../services/conference.service';
import { Conference } from '../../models/conference';
import { TitleService } from '../../services/title.service';

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
