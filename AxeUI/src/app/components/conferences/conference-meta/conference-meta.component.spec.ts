import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ConferenceMetaComponent } from './conference-meta.component';

describe('ConferenceMetaComponent', () => {
  let component: ConferenceMetaComponent;
  let fixture: ComponentFixture<ConferenceMetaComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ConferenceMetaComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ConferenceMetaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
