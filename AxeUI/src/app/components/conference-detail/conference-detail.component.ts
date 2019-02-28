import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { TitleService } from '../../services/title.service';
import { Conference } from '../../models/conference';
import { ConferenceService } from '../../services/conference.service';
import { Team } from '../../models/team';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-conference-detail',
  templateUrl: './conference-detail.component.html',
  styleUrls: ['./conference-detail.component.scss']
})
export class ConferenceDetailComponent implements OnInit {

  private conferenceId: number;
  conference$: Observable<Conference>;
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
      .pipe(conference => this.conference$ = conference);
  }

  getConferenceMembers(): void {
    this._conferenceService.getConferenceMembers(this.conferenceId)
      .subscribe(members => this.members = members);
  }

  setConferenceId(): void {
    this.conferenceId = +this.route.snapshot.paramMap.get('id');
  }

}
