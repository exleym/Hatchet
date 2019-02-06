import { Component, OnInit } from '@angular/core';
import { Card } from '../card/card';
import { TitleService } from '../title.service';

const CARDS: Card[] = [
  {id: 1,  width: 6, title: 'Test Card Number 1', subtitle: 'Lorem Ipsum'},
  {id: 2,  width: 6, title: 'Test Card Number 2', subtitle: 'Lorem Ipsum'},
  {id: 3,  width: 6, title: 'Test Card Number 3', subtitle: 'Lorem Ipsum'},
  {id: 4,  width: 6, title: 'Test Card Number 4', subtitle: 'Lorem Ipsum'},
  {id: 5,  width: 6, title: 'Test Card Number 5', subtitle: 'Lorem Ipsum'},
  {id: 6,  width: 6, title: 'Test Card Number 6', subtitle: 'Lorem Ipsum'},
  {id: 7,  width: 6, title: 'Test Card Number 7', subtitle: 'Lorem Ipsum'},
  {id: 8,  width: 6, title: 'Test Card Number 8', subtitle: 'Lorem Ipsum'},
];

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {
  cards = CARDS;

  constructor(public titleService: TitleService) {}

  ngOnInit() {
    this.titleService.setTitle('Dashboard');
  }

}
