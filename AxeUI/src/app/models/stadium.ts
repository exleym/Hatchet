export class Stadium {
  id: number;
  code: string;
  name: string;
  city: string;
  state: string;
  latitude: string;
  longitude: string;
  built: number;
  capacity: number;
  surfaceId: number;

  constructor(data) {
    console.log('Team.constructor()');
    console.log(data);
    this.id = data.id;
    this.name = data.name;
    this.city = data.city;
    this.state = data.state;
    this.latitude = data.latitude;
    this.longitude = data.longitude;
    this.built = data.built;
    this.capacity = data.capacity;
    this.surfaceId = data.surfaceId;
  }
}
