import { Component, OnInit, Input, Output } from '@angular/core';
import { Game } from '../../models/game';
import { Team } from '../../models/team';
import { GameService } from '../../services/game.service';
import {Stadium} from '../../models/stadium';
import {StadiumService} from '../../services/stadium.service';

@Component({
  selector: 'app-schedule',
  templateUrl: './schedule.component.html',
  styleUrls: ['./schedule.component.scss']
})
export class ScheduleComponent implements OnInit {

  @Input() games: Game[];
  @Input() team: Team;
  activeGame: Game;
  activeStadium: Stadium;

  constructor(private gameService: GameService,
              private stadiumService: StadiumService) { }

  addGame(game: Game): void {
    this.gameService.createGame(game)
      .subscribe(res => this.games.push(res));
  }

  ngOnInit() {
    this.setActive(this.games[0]);
  }

  setActive(game: Game): void {
    console.log(`setting activeGame=${game}`);
    this.activeGame = game;
    this.setActiveStadium(game.stadiumId);
  }

  showGameForm(): void {
    console.log('you clicked the thing!');
  }

  setActiveStadium(stadiumId: number): void {
    this.stadiumService.getStadium(stadiumId)
      .subscribe(stadium => {
        this.activeStadium = stadium;
      });
  }

}
