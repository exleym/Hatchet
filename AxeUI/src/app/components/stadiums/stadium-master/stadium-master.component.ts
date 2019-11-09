import { Component, OnInit } from '@angular/core';

import { Stadium } from '../../../models/stadium';
import { StadiumService } from '../../../services/stadium.service';
import { TitleService } from '../../../services/title.service';

@Component({
  selector: 'app-stadium-master',
  templateUrl: './stadium-master.component.html',
  styleUrls: ['./stadium-master.component.scss']
})
export class StadiumMasterComponent implements OnInit {
  stadiums: Stadium[];

  constructor(public titleService: TitleService,
              private _stadiumService: StadiumService) { }

  ngOnInit() {
    this.titleService.setTitle('Stadiums Management Console');
    this._stadiumService.getStadiums()
      .subscribe((res: Stadium[]) => this.stadiums = res);
  }

}
