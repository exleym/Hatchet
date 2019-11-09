import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { StadiumMasterComponent } from './stadium-master.component';

describe('StadiumMasterComponent', () => {
  let component: StadiumMasterComponent;
  let fixture: ComponentFixture<StadiumMasterComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ StadiumMasterComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(StadiumMasterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
