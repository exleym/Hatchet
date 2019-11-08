export class Line {
  id: number;
  gameId: number;
  teamId: number;
  bookmakerId: number;
  spread: number;
  overUnder: number;
  vigorish: number;

  constructor(data) {
    this.id = data.id;
    this.gameId = data.gameId;
    this.teamId = data.teamId;
    this.bookmakerId = data.bookmakerId;
    this.spread = data.spread;
    this.overUnder = data.overUnder;
    this.vigorish = data.vigorish;
  }
}
