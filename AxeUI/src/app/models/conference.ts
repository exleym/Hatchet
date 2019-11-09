export class Conference {
  id: number;
  code: string;
  name: string;
  shortName: string;
  inceptionYear: number;

  constructor(data: any) {
    this.id = data.id;
    this.code = data.code;
    this.name = data.name;
    this.shortName = data.shortName;
    this.inceptionYear = data.inceptionYear;
  }
}
