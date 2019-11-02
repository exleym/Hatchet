import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BetCreatorComponent } from './bet-creator.component';

describe('BetCreatorComponent', () => {
  let component: BetCreatorComponent;
  let fixture: ComponentFixture<BetCreatorComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ BetCreatorComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BetCreatorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
