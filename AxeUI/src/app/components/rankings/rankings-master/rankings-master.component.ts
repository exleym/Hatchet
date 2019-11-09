import { Component, OnInit } from '@angular/core';
import { WeekService } from '../../../services/week.service';
import {TitleService} from '../../../services/title.service';
import { Week } from '../../../models/week';

@Component({
  selector: 'app-rankings-master',
  templateUrl: './rankings-master.component.html',
  styleUrls: ['./rankings-master.component.scss']
})
export class RankingsMasterComponent implements OnInit {
  weeks: Week[];
  activeWeek: Week;
  defaultSeason = 2019;

  constructor(private weekService: WeekService,
              private titleService: TitleService) { }

  ngOnInit() {
    this.titleService.setTitle('Rankings Manager');
    this.getWeeks(this.defaultSeason);
  }

  getWeeks(season: number): void {
    this.weekService.getWeeks(season)
      .subscribe((weeks) => {
        this.weeks = weeks;
        this.activeWeek = weeks[0];
      });
  }

  setActiveWeek(week: Week): void {
    this.activeWeek = week;
  }
}
