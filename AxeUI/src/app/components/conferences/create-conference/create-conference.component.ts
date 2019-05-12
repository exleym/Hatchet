import { Component, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { ConferenceService } from '../../../services/conference.service';
import {ConditionalExpr} from '@angular/compiler';
import {Conference} from '../../../models/conference';

@Component({
  selector: 'app-create-conference',
  templateUrl: './create-conference.component.html',
  styleUrls: ['./create-conference.component.scss']
})
export class CreateConferenceComponent implements OnInit {

  subdivisions = [
    {id: 1, name: 'FBS'},
    {id: 2, name: 'FCS'}
  ];
  submitted = false;
  conferenceForm = this.fb.group({
    subdivision: [''],
    code: [''],
    shortName: [''],
    name: [''],
    inceptionYear: [''],
  });

  constructor(private conferenceService: ConferenceService,
              private fb: FormBuilder) { }

  ngOnInit() {
  }

  addConference(): void {
    this.submitted = true;
    this.conferenceService.createConference(
      new Conference(this.conferenceForm.value)
    ).subscribe((c) => {
      this.emitNewConference(new Conference(c));
    });
    this.conferenceForm.reset();
    this.submitted = false;
  }

  emitNewConference(conference: Conference) {
    console.log(conference);
  }

}
