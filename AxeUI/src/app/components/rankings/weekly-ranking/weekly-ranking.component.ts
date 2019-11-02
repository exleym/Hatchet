import {Component, Input, OnChanges, OnInit, SimpleChanges} from '@angular/core';
import {Week} from '../../../models/week';
import { Ranking } from '../../../models/ranking';
import { RankingService } from '../../../services/ranking.service';

@Component({
  selector: 'app-weekly-ranking',
  templateUrl: './weekly-ranking.component.html',
  styleUrls: ['./weekly-ranking.component.scss']
})
export class WeeklyRankingComponent implements OnInit, OnChanges {

  @Input() week: Week;
  rankings: Ranking[];

  constructor(private rankingService: RankingService) { }

  ngOnInit() {
  }

  ngOnChanges(changes: SimpleChanges): void {
    this.updateRankings(changes.week.currentValue);
  }

  updateRankings(week: Week) {
    this.rankingService.getRankings(week.id, 1)
      .subscribe((rankings) => {
        this.rankings = rankings;
      });
  }

}
