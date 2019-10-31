import { Component, OnInit, Input, Output } from '@angular/core';
import { Game } from '../../models/game';
import { Team } from '../../models/team';
import { GameService } from '../../services/game.service';

@Component({
  selector: 'app-schedule',
  templateUrl: './schedule.component.html',
  styleUrls: ['./schedule.component.scss']
})
export class ScheduleComponent implements OnInit {

  @Input() games: Game[];
  @Input() team: Team;
  activeGame: Game;

  constructor(private gameService: GameService) { }

  addGame(game: Game): void {
    this.gameService.createGame(game)
      .subscribe(res => this.games.push(res));
  }

  ngOnInit() {
    this.activeGame = this.games[1];
  }

  setActive(game: Game): void {
    console.log(`setting activeGame=${game}`);
    this.activeGame = game;
  }

  showGameForm(): void {
    console.log('you clicked the thing!');
  }

}
