import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TeamMasterComponent } from './team-master.component';

describe('TeamMasterComponent', () => {
  let component: TeamMasterComponent;
  let fixture: ComponentFixture<TeamMasterComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TeamMasterComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TeamMasterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
