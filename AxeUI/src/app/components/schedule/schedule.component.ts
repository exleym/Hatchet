import { Component, OnInit, Input, Output } from '@angular/core';
import { Game } from '../../models/game';
import { Line } from '../../models/line';
import { Team } from '../../models/team';
import { GameService } from '../../services/game.service';
import {Stadium} from '../../models/stadium';
import {StadiumService} from '../../services/stadium.service';
import {BookmakerService} from '../../services/bookmaker.service';
import {Bookmaker} from '../../models/bookmaker';

@Component({
  selector: 'app-schedule',
  templateUrl: './schedule.component.html',
  styleUrls: ['./schedule.component.scss']
})
export class ScheduleComponent implements OnInit {

  @Input() games: Game[];
  @Input() team: Team;
  activeGame: Game;
  activeLines: Line[];
  activeStadium: Stadium;
  bookmakers: Map<number, Bookmaker>;

  constructor(private gameService: GameService,
              private stadiumService: StadiumService,
              private bookmakerService: BookmakerService) { }

  addGame(game: Game): void {
    this.gameService.createGame(game)
      .subscribe(res => this.games.push(res));
  }

  ngOnInit() {
    this.bookmakers = new Map<number, Bookmaker>();
    this.setActive(this.games[0]);
    this.setBookmakers();
  }

  setActive(game: Game): void {
    console.log(`setting activeGame=${game}`);
    this.activeGame = game;
    this.setActiveStadium(game.stadiumId);
    this.setActiveLines(game.id, this.team.id);
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

  setActiveLines(gameId: number, teamId?: number) {
    this.gameService.getGameLines(gameId, teamId)
      .subscribe(lines => {
        this.activeLines = lines;
      });
  }

  setBookmakers(): void {
    this.bookmakerService.getBookmakers()
      .subscribe(bookmakers => {
        bookmakers.map(item => {
          const bookie: Bookmaker = new Bookmaker(item);
          this.bookmakers.set(bookie.id, bookie);
        });
      });
  }

  getBookmakerName(bookmakerId: number): string {
    const bookie: Bookmaker = this.bookmakers.get(bookmakerId);
    return bookie.name;
  }

}
