import {Component, Input, OnInit} from '@angular/core';
import {Team} from '../../../models/team';
import {TeamService} from '../../../services/team.service';

@Component({
  selector: 'app-team-meta',
  templateUrl: './team-meta.component.html',
  styleUrls: ['./team-meta.component.scss']
})
export class TeamMetaComponent implements OnInit {

  editor = false;

  @Input()
  team: Team;

  constructor(
    teamService: TeamService
  ) { }

  ngOnInit() {
  }

  toggleEditor() {
    this.editor = this.editor === false;
  }
}
