import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MemberEntryListComponent } from './member-entry-list.component';

describe('MemberEntryListComponent', () => {
  let component: MemberEntryListComponent;
  let fixture: ComponentFixture<MemberEntryListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MemberEntryListComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(MemberEntryListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
