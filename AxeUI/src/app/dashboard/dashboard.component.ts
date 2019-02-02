import { Component, OnInit } from '@angular/core';
import { Card } from '../card/card';

const CARDS: Card[] = [
  {id: 1,  width: 6, title: 'Test Card Number 1', subtitle: 'Lorem Ipsum'},
  {id: 2,  width: 6, title: 'Test Card Number 2', subtitle: 'Lorem Ipsum'},
  {id: 3,  width: 6, title: 'Test Card Number 3', subtitle: 'Lorem Ipsum'},
];

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {
  cards = CARDS;

  constructor() { }

  ngOnInit() {
  }

}
