export class Team {
  id: number;
  name: string;
  shortName: string;
  mascot: string;
  conferenceId: number;
  divisionId: number;
  stadiumId: number;

  constructor(data) {
    this.id = data.id;
    this.name = data.name;
    this.shortName = data.shortName;
    this.mascot = data.mascot;
    this.divisionId = data.divisionId;
    this.stadiumId = data.stadiumId;
    this.conferenceId = data.conferenceId;
  }
}
