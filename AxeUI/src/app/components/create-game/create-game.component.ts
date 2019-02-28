import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';

@Component({
  selector: 'app-create-game',
  templateUrl: './create-game.component.html',
  styleUrls: ['./create-game.component.scss']
})
export class CreateGameComponent implements OnInit {
  formEspnId = new FormControl('', Validators.required);
  formKickoffTime = new FormControl('', Validators.required);
  formStadiumId = new FormControl('', Validators.required);
  formOpponentId = new FormControl('');

  constructor() { }

  ngOnInit() {
  }

}
