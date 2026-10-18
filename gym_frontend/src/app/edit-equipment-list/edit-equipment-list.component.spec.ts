import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EditEquipmentListComponent } from './edit-equipment-list.component';

describe('EditEquipmentListComponent', () => {
  let component: EditEquipmentListComponent;
  let fixture: ComponentFixture<EditEquipmentListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EditEquipmentListComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(EditEquipmentListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
