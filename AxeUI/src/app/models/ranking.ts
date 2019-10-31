import {Team} from './team';

export class Ranking {
  id: number;
  weekId: number;
  pollId: number;
  teamId: number;
  rank: number;
  priorRank: number;
  team: Team;

  constructor(data) {
    this.id = data.id;
    this.weekId = data.weekId;
    this.pollId = data.pollId;
    this.teamId = data.teamId;
    this.rank = data.rank;
    this.priorRank = data.priorRank;
    this.team = new Team(data.team);
  }

  getPriorRank(): any {
    if (this.priorRank === null) {
      return 'N/A';
    }
    return this.priorRank;
  }
}
