import { Component, OnInit, Input } from '@angular/core';
import {Game} from '../../models/game';
import {Team} from '../../models/team';
import {GameParticipant} from '../../models/game-participant';

@Component({
  selector: 'app-schedule-item',
  templateUrl: './schedule-item.component.html',
  styleUrls: ['./schedule-item.component.scss']
})
export class ScheduleItemComponent implements OnInit {

  @Input() game: Game;
  @Input() referenceTeam: Team;
  referenceParticipant: GameParticipant;
  opponent: GameParticipant;

  constructor() { }

  ngOnInit() {
    this.setParticipants();
  }

  setParticipants(): void {
    this.referenceParticipant = this.game.participants
      .find(x => x.teamId === this.referenceTeam.id);
    this.opponent = this.game.participants
      .find(x => x.teamId !== this.referenceTeam.id);
  }

}
