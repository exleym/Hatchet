import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class TitleService {
  title = 'Dashboard';

  setTitle(title: string) {
    console.log('setting title!');
    this.title = title;
  }

  getTitle() {
    console.log(this.title);
    return this.title;
  }

  constructor() { }
}
