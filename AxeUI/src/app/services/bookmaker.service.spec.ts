import { TestBed } from '@angular/core/testing';

import { BookmakerService } from './bookmaker.service';

describe('BookmakerService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: BookmakerService = TestBed.get(BookmakerService);
    expect(service).toBeTruthy();
  });
});
