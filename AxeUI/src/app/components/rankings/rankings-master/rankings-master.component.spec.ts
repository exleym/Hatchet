import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RankingsMasterComponent } from './rankings-master.component';

describe('RankingsMasterComponent', () => {
  let component: RankingsMasterComponent;
  let fixture: ComponentFixture<RankingsMasterComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RankingsMasterComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RankingsMasterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
