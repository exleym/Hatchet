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
    this.id = data.id;
    this.espnId = data.espnId;
    this.kickoffTime = new Date(data.kickoffTime);
    this.stadiumId = data.stadiumId;
    this.participants = [];
    this.createParticipants(data.participants);
  }

  createParticipants(participants): void {
     participants.forEach(p => {
       this.participants.push(new GameParticipant(p));
    });
  }

  participant(teamId: number): GameParticipant {
    return this.participants.find( p => p.teamId === teamId);
  }

  opponent(teamId: number): GameParticipant {
    return this.participants.find(p => p.teamId !== teamId);
  }
}
