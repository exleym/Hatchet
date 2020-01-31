import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ConferenceMembersComponent } from './conference-members.component';

describe('ConferenceMembersComponent', () => {
  let component: ConferenceMembersComponent;
  let fixture: ComponentFixture<ConferenceMembersComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ConferenceMembersComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ConferenceMembersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
