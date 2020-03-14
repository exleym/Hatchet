import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {Team} from '../../../models/team';
import {TeamService} from '../../../services/team.service';
import {FormBuilder} from '@angular/forms';

@Component({
  selector: 'app-team-editor',
  templateUrl: './team-editor.component.html',
  styleUrls: ['./team-editor.component.scss']
})
export class TeamEditorComponent implements OnInit {

  submitted = false;

  @Input()
  team: Team;

  @Output()
  teamSubject = new EventEmitter();

  teamEditor = this.fb.group({
    id: [''],
    shortName: [''],
    name: [''],
    mascot: [''],
    logo: ['']
  });

  constructor(
    private teamService: TeamService,
    private fb: FormBuilder,
  ) { }

  ngOnInit() {
    this.setFormValue();
  }

  setFormValue(): void {
    console.log(this.team);
    const teamValues = {
      id: this.team.id,
      shortName: this.team.shortName,
      name: this.team.name,
      mascot: this.team.mascot,
      logo: this.team.logo
    };
    this.teamEditor.setValue(teamValues);
  }

  onSubmit(): void {
    const team = new Team(this.teamEditor.value);
    this.teamSubject.emit(team);
    this.submitted = true;
  }

}
