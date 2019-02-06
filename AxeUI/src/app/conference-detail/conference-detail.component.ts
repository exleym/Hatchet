import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { TitleService } from '../title.service';
import { Conference } from '../conferences/conference';
import { ConferenceService } from '../conference.service';
import { Team } from '../teams/team';

@Component({
  selector: 'app-conference-detail',
  templateUrl: './conference-detail.component.html',
  styleUrls: ['./conference-detail.component.scss']
})
export class ConferenceDetailComponent implements OnInit {

  private conferenceId: number;
  conference: Conference;
  members: Team[];

  constructor(private route: ActivatedRoute,
              public titleService: TitleService,
              private _conferenceService: ConferenceService) { }

  ngOnInit() {
    this.setConferenceId();
    this.getConferenceMembers();
    this.getConference();
    this.titleService.setTitle('Conference Details');
  }

  getConference(): void {
    this._conferenceService.getConference(this.conferenceId)
      .subscribe(conference => this.conference = conference);
  }

  getConferenceMembers(): void {
    this._conferenceService.getConferenceMembers(this.conferenceId)
      .subscribe(members => this.members = members);
  }

  setConferenceId(): void {
    this.conferenceId = +this.route.snapshot.paramMap.get('id');
  }

}
