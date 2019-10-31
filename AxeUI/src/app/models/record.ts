export class Record {
  season: number;
  wins: number;
  losses: number;
  confWins: number;
  confLosses: number;

  constructor(data) {
    this.season = data.season;
    this.wins = data.wins;
    this.losses = data.losses;
    this.confWins = data.confWins;
    this.confLosses = data.confLosses;
  }
}
