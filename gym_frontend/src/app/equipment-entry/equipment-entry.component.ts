import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { EquipmentService } from '../services/equipment.service';

@Component({
  selector: 'app-equipment-entry',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './equipment-entry.component.html',
  styleUrl: './equipment-entry.component.css'
})
export class EquipmentEntryComponent implements OnInit {
  equipmentForm!: FormGroup;
  isSubmitting = false;

  constructor(
    private fb: FormBuilder,
    private equipmentService: EquipmentService
  ) {}

  ngOnInit(): void {
    this.initForm();
  }

  private initForm(): void {
    // Aligned strictly to the t1-t8 Equipment schema
    this.equipmentForm = this.fb.group({
      t1: ['', Validators.required], // Equipment Name
      t2: ['', Validators.required], // Description
      t3: [new Date().toISOString().substring(0, 10), Validators.required], // Purchase Date
      t4: ['', Validators.required], // Quantity
      t5: ['', Validators.required], // Vendor Name
      t6: ['', Validators.required], // Vendor Address
      t7: ['', Validators.required], // Contact Number
      t8: [0, [Validators.required, Validators.min(0)]], // Cost per item
      n1: [1]                        // Status (1 = active)
    });
  }

  onSubmit(): void {
    // Check form validity and block duplicate requests
    if (this.equipmentForm.invalid || this.isSubmitting) {
      this.equipmentForm.markAllAsTouched();
      console.warn('Form validation failed:', this.equipmentForm.value);
      return;
    }

    this.isSubmitting = true;
    const formPayload = this.equipmentForm.getRawValue();

    // Ensure cost (t8) is sent as a number
    if (formPayload.t8) {
      formPayload.t8 = Number(formPayload.t8);
    }

    this.equipmentService.addEquipment(formPayload).subscribe({
      next: (response: any) => {
        alert(response?.message || 'Equipment added successfully!');
        this.equipmentForm.reset({
          t3: new Date().toISOString().substring(0, 10),
          n1: 1
        });
        this.isSubmitting = false;
      },
      error: (err) => {
        console.error('Error creating equipment:', err);
        alert(err?.error?.message || 'Failed to create equipment. Please check backend logs.');
        this.isSubmitting = false;
      }
    });
  }
}