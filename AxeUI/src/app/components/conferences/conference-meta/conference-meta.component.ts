import {Component, Input, OnInit} from '@angular/core';
import {Conference} from '../../../models/conference';
import {ConferenceService} from '../../../services/conference.service';
import {FormBuilder} from '@angular/forms';

@Component({
  selector: 'app-conference-meta',
  templateUrl: './conference-meta.component.html',
  styleUrls: ['./conference-meta.component.scss']
})
export class ConferenceMetaComponent implements OnInit {

  editor = false;
  submitted = false;

  @Input()
  conference: Conference;

  confEditor = this.fb.group({
    id: [''],
    code: [''],
    shortName: [''],
    name: [''],
    inceptionYear: [''],
  });

  constructor(
    private _conferenceService: ConferenceService,
    private fb: FormBuilder
  ) { }

  ngOnInit() {
  }

  toggleEditor() {
    this.confEditor.setValue(this.conference);
    this.editor = this.editor === false;
    this.submitted = false;
  }

  deleteConference(): void {
    this._conferenceService.deleteConference(this.conference).subscribe(
      () => { console.log('Deletion successful!'); }
    );
  }

  onSubmit(): void {
    this.submitted = true;
    this._conferenceService.updateConference(this.confEditor.value)
      .subscribe(conf => this.conference = conf);
    this.toggleEditor();
  }

}
