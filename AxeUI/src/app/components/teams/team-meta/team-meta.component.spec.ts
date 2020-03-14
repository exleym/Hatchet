import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TeamMetaComponent } from './team-meta.component';

describe('TeamMetaComponent', () => {
  let component: TeamMetaComponent;
  let fixture: ComponentFixture<TeamMetaComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TeamMetaComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TeamMetaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
