export class Team {
  id: number;
  code: string;
  name: string;
  shortName: string;
  mascot: string;
  conferenceId: number;
  divisionId: number;
  stadiumId: number;
  teamLogo = 'football.png';

  constructor(data) {
    this.id = data.id;
    if (this.id === 13) {
      this.teamLogo = 'clemson.png';
    }
    if (this.id === 14) {
      this.teamLogo = 'boston-college.png';
    }
    this.code = data.code;
    this.name = data.name;
    this.shortName = data.shortName;
    this.mascot = data.mascot;
    this.divisionId = data.divisionId;
    this.stadiumId = data.stadiumId;
    this.conferenceId = data.conferenceId;
  }

  displayName(): string {
    if (this.shortName.length < 17) {
      return this.shortName;
    }
    return this.code;
  }
}
