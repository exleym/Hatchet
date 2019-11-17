import {Team} from './team';

export class Rating {
  id: number;
  gameId: number;
  networkId: number;
  rating: number;
  viewers: number;

  constructor(data) {
    this.id = data.id;
    this.gameId = data.gameId;
    this.networkId = data.networkId;
    this.rating = data.rating;
    this.viewers = data.viewers;
  }
}
