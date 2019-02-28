import { OnInit } from '@angular/core';
import { GameParticipant } from './game-participant';

export class Game implements OnInit {
  id: number;
  espnId: number;
  kickoffTime: Date;
  stadiumId: number;
  public participants: GameParticipant[];

  ngOnInit() {}

  constructor(data) {
    console.log(`creating game ${data}`);
    this.id = data.id;
    this.espnId = data.espnId;
    this.kickoffTime = new Date(data.kickoffTime);
    this.stadiumId = data.stadiumId;
    this.participants = [];
    this.createParticipants(data.participants);
  }

  createParticipants(participants): void {
    console.log(`creating participants ${participants}`);
     participants.forEach(p => {
       console.log('trying to create a participant');
       this.participants.push(new GameParticipant(p));
       console.log('i think we did it');
    });
  }

  participant(teamId: number): GameParticipant {
    return this.participants.find( p => p.teamId === teamId);
  }

  opponent(teamId: number): GameParticipant {
    return this.participants.find(p => p.teamId !== teamId);
  }
}
