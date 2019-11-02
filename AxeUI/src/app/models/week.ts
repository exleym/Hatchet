export class Week {
  id: number;
  number: number;
  season: number;
  startDate: Date;
  endDate: Date;

  constructor(data) {
    this.id = data.id;
    this.number = data.number;
    this.startDate = new Date(data.startDate);
    this.endDate = new Date(data.endDate);
  }
}
