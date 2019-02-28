export class Team {
  id: number;
  name: string;
  shortName: string;
  mascot: string;
  conference: string;
  division: string;
  stadium: string;

  constructor(data) {
    this.id = data.id;
    this.name = data.name;
    this.shortName = data.shortName;
    this.mascot = data.mascot;
    this.conference = data.conference;
    this.division = data.division;
    this.stadium = data.stadium;
  }
}
