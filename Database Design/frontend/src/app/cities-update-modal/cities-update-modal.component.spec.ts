import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CitiesUpdateModalComponent } from './cities-update-modal.component';

describe('CitiesUpdateModalComponent', () => {
  let component: CitiesUpdateModalComponent;
  let fixture: ComponentFixture<CitiesUpdateModalComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CitiesUpdateModalComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CitiesUpdateModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
