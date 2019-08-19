import { Team } from './team';


export class GameParticipant {
  id: number;
  gameId: number;
  locationTypeId: number;
  teamId: number;
  team: Team;
  score: number;

  constructor(data) {
    this.id = data.id;
    this.gameId = data.gameId;
    this.locationTypeId = data.locationTypeId;
    this.teamId = data.teamId;
    if (data.team == null) {
      this.team = null;
    } else {
      this.team = new Team(data.team);
    }
    this.score = data.score;
  }

  location(): string {
    const locMap = {
      1: 'vs', 2: '@'
    };
    return locMap[this.locationTypeId];
  }
}
