import {Component, Input, OnInit} from '@angular/core';
import {Team} from '../../../models/team';

@Component({
  selector: 'app-conference-members',
  templateUrl: './conference-members.component.html',
  styleUrls: ['./conference-members.component.scss']
})
export class ConferenceMembersComponent implements OnInit {

  @Input()
  teams: Team[];

  constructor() { }

  ngOnInit() {
  }

}
