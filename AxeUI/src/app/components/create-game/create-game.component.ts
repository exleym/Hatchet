import { Component } from '@angular/core';
import { FormBuilder } from '@angular/forms';

@Component({
  selector: 'app-create-game',
  templateUrl: './create-game.component.html',
  styleUrls: ['./create-game.component.scss']
})
export class CreateGameComponent {
  submitted = false;
  gameForm = this.fb.group({
    espnId: [''],
    kickoffTime: [''],
    stadiumId: [''],
  });

  constructor(private fb: FormBuilder) { }

  onSubmit(): void {
    this.submitted = true;
    console.log('form submitted successfully!');
    console.log(this.gameForm.value);
  }

}
