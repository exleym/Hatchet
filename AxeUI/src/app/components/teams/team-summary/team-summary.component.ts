import {Component, Input, OnInit} from '@angular/core';
import { Team } from '../../../models/team';

@Component({
  selector: 'app-team-summary',
  templateUrl: './team-summary.component.html',
  styleUrls: ['./team-summary.component.scss']
})
export class TeamSummaryComponent implements OnInit {

  @Input()
  team: Team;

  constructor() { }

  ngOnInit() {
  }

}
