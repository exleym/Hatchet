import { OnInit } from '@angular/core';
import { GameParticipant } from './game-participant';
import { Rating } from './rating';
import {Team} from './team';
import { TeamService } from '../services/team.service';

export class Game implements OnInit {
  id: number;
  espnId: number;
  kickoffTime: Date;
  stadiumId: number;
  rating: Rating;
  public participants: GameParticipant[];

  ngOnInit() {}

  constructor(data) {
    this.id = data.id;
    this.espnId = data.espnId;
    this.kickoffTime = new Date(data.kickoffTime);
    this.stadiumId = data.stadiumId;
    this.participants = [];
    this.createParticipants(data.participants);
    this.createRating(data.rating);
  }

  createParticipants(participants): void {
     participants.forEach(p => {
       this.participants.push(new GameParticipant(p));
    });
  }

  createRating(rating): void {
    if (rating !== null) {
      this.rating = new Rating(rating);
    }
  }

  participant(teamId: number): GameParticipant {
    return this.participants.find( p => p.teamId === teamId);
  }

  opponent(teamId: number): GameParticipant {
    return this.participants.find(p => p.teamId !== teamId);
  }
}
