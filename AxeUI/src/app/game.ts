import { OnInit } from '@angular/core';


export class GameParticipant {
  id: number;
  gameId: number;
  locationTypeId: number;
  teamId: number;
  score: number;
}


export class Game implements OnInit {
  id: number;
  espnId: number;
  kickoffTime: string;
  stadiumId: number;
  participants: GameParticipant[];

  ngOnInit() {}

  participant(teamId: number): GameParticipant {
    return this.participants.find( p => p.teamId === teamId);
  }

  opponent(teamId: number): GameParticipant {
    return this.participants.find(p => p.teamId !== teamId);
  }
}
