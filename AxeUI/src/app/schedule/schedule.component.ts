import { Component, OnInit, Input } from '@angular/core';
import {Game} from '../game';
import {Team} from '../teams/team';

@Component({
  selector: 'app-schedule',
  templateUrl: './schedule.component.html',
  styleUrls: ['./schedule.component.scss']
})
export class ScheduleComponent implements OnInit {

  @Input() games: Game[];
  @Input() team: Team;

  constructor() { }

  ngOnInit() {
    console.log(this.games);
    console.log(this.team);
  }

}
