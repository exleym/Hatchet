import {Component, EventEmitter} from '@angular/core';
import { FormBuilder } from '@angular/forms';
import {GameService} from '../../services/game.service';
import {Game} from '../../models/game';

@Component({
  selector: 'app-create-game',
  templateUrl: './create-game.component.html',
  styleUrls: ['./create-game.component.scss']
})
export class CreateGameComponent {

  submitted = false;
  gameSubject = new EventEmitter();

  gameForm = this.fb.group({
    espnId: [''],
    kickoffTime: [''],
    stadiumId: [''],
  });

  constructor(
    private fb: FormBuilder,
    private gameService: GameService
  ) { }

  onSubmit(): void {
    this.submitted = true;
    const game = new Game(this.gameForm.value);
    this.gameService.createGame(game)
      .subscribe(g => this.gameSubject.emit(g));
  }

}
