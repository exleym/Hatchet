export class Network {
  id: number;
  code: string;
  name: string;
  website: string;

  constructor(data) {
    this.id = data.id;
    this.code = data.code;
    this.name = data.name;
    this.website = data.website;
  }
}
