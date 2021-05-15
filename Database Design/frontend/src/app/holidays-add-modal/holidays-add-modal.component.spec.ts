import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { HolidaysAddModalComponent } from './holidays-add-modal.component';

describe('HolidaysAddModalComponent', () => {
  let component: HolidaysAddModalComponent;
  let fixture: ComponentFixture<HolidaysAddModalComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ HolidaysAddModalComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(HolidaysAddModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
