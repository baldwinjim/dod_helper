import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Speakers } from './speakers';

describe('Speakers', () => {
  let component: Speakers;
  let fixture: ComponentFixture<Speakers>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Speakers]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Speakers);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
