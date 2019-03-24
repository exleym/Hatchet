export class GameParticipant {
  id: number;
  gameId: number;
  locationTypeId: number;
  teamId: number;
  teamName: string;
  score: number;

  constructor(data) {
    this.id = data.id;
    this.gameId = data.gameId;
    this.locationTypeId = data.locationTypeId;
    this.teamId = data.teamId;
    this.teamName = data.teamName;
    this.score = data.score;
  }

  location(): string {
    const locMap = {
      1: 'vs', 2: '@'
    };
    return locMap[this.locationTypeId];
  }
}
