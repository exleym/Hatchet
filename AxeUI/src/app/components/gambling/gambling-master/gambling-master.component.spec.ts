import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { GamblingMasterComponent } from './gambling-master.component';

describe('GamblingMasterComponent', () => {
  let component: GamblingMasterComponent;
  let fixture: ComponentFixture<GamblingMasterComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ GamblingMasterComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(GamblingMasterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
