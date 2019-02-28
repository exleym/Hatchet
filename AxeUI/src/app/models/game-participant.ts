export class GameParticipant {
  id: number;
  gameId: number;
  locationTypeId: number;
  teamId: number;
  teamName: string;
  score: number;

  constructor(data) {
    console.log(`creating participant: ${data}`);
    this.id = data.id;
    this.gameId = data.gameId;
    this.locationTypeId = data.locationTypeId;
    this.teamId = data.teamId;
    this.teamName = data.teamName;
    this.score = data.score;
  }
}
