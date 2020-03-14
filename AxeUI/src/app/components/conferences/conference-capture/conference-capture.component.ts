import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {Conference} from '../../../models/conference';
import {FormBuilder} from '@angular/forms';

@Component({
  selector: 'app-conference-capture',
  templateUrl: './conference-capture.component.html',
  styleUrls: ['./conference-capture.component.scss']
})
export class ConferenceCaptureComponent implements OnInit {

  @Input() conference: Conference;
  @Output() success: EventEmitter<Conference>;
  submitted = false;

  confEditor = this.fb.group({
    id: [''],
    code: [''],
    shortName: [''],
    name: [''],
    inceptionYear: [''],
  });

  constructor(
    private fb: FormBuilder,
  ) { }

  ngOnInit() {
  }

  onSubmit() {
    this.submitted = true;
  }

}
