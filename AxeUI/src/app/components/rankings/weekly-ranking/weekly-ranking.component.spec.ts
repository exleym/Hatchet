import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { WeeklyRankingComponent } from './weekly-ranking.component';

describe('WeeklyRankingComponent', () => {
  let component: WeeklyRankingComponent;
  let fixture: ComponentFixture<WeeklyRankingComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ WeeklyRankingComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(WeeklyRankingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
