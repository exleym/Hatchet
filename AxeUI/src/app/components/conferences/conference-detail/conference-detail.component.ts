import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { FormBuilder } from '@angular/forms';
import { TitleService } from '../../../services/title.service';
import { Conference } from '../../../models/conference';
import { ConferenceService } from '../../../services/conference.service';
import { Team } from '../../../models/team';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-conference-detail',
  templateUrl: './conference-detail.component.html',
  styleUrls: ['./conference-detail.component.scss']
})
export class ConferenceDetailComponent implements OnInit {

  private conferenceId: number;
  conference: Conference;
  members: Team[];
  editor = false;
  submitted = false;
  confEditor = this.fb.group({
    id: [''],
    code: [''],
    shortName: [''],
    name: [''],
    inceptionYear: [''],
  });

  constructor(private route: ActivatedRoute,
              public titleService: TitleService,
              private _conferenceService: ConferenceService,
              private fb: FormBuilder) { }

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

  toggleEditor(): void {
    this.confEditor.setValue(this.conference);
    this.editor = this.editor === false;
    this.submitted = false;
  }

  onSubmit(): void {
    console.log(this.confEditor.value);
    this._conferenceService.updateConference(this.confEditor.value)
      .subscribe(conf => this.conference = conf);
    this.submitted = true;
    this.toggleEditor();
  }

  deleteConference(): void {
    this._conferenceService.deleteConference(this.conference).subscribe(
      () => { console.log('Deletion successful!'); }
    );
    console.log(`deleting conference: ${this.conference}`);
  }

}
