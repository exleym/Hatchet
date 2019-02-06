import { Component, OnInit } from '@angular/core';
import { MenuItem } from './menuItem';

const MENU_ITEMS: MenuItem[] = [
  {id: 2, iconName: 'dashboard', displayName: 'Dashboard', linkURL: '/dashboard'},
  {id: 3, iconName: 'stars', displayName: 'Conference', linkURL: '/conferences'},
  {id: 4, iconName: 'people', displayName: 'Teams', linkURL: '/teams'},
  {id: 5, iconName: 'person', displayName: 'Players', linkURL: '/players'},
  {id: 6, iconName: 'games', displayName: 'Games', linkURL: '/games'},
  {id: 7, iconName: 'show_chart', displayName: 'Statistics', linkURL: '/statistics'},
];

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss']
})
export class SidebarComponent implements OnInit {
  menuItems = MENU_ITEMS;

  constructor() { }

  ngOnInit() {
  }

}
