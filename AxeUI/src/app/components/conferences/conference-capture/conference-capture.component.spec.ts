import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ConferenceCaptureComponent } from './conference-capture.component';

describe('ConferenceCaptureComponent', () => {
  let component: ConferenceCaptureComponent;
  let fixture: ComponentFixture<ConferenceCaptureComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ConferenceCaptureComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ConferenceCaptureComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
