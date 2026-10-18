import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { MemberService, AllDropdowns } from '../services/member.service';

@Component({
  selector: 'app-member-entry',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './member-entry.component.html',
  styleUrls: ['./member-entry.component.css']
})
export class MemberEntryComponent implements OnInit {
  memberForm!: FormGroup;
  dropdowns!: AllDropdowns;
  isLoading = true;
  isEditMode = false;
  syskey: string | null = null;

  constructor(
    private fb: FormBuilder,
    private memberService: MemberService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.initForm();
    this.listenToPriceChanges();

    this.syskey = this.route.snapshot.paramMap.get('syskey');
    this.isEditMode = !!this.syskey;

    // Load dropdowns FIRST, then handle edit mode inside the callback
    this.loadDropdownsAndData();
  }

  private initForm(): void {
    this.memberForm = this.fb.group({
      syskey: [''], // ADDED: Ensures syskey is tracked by Reactive Forms
      t1: ['', Validators.required],
      t2: ['', Validators.required],
      t3: ['', Validators.required],
      t4: ['', Validators.required],
      t5: [new Date().toISOString().substring(0, 10), Validators.required],
      t6: ['', Validators.required], // Plan
      t7: ['', Validators.required],
      t8: ['', Validators.required],
      t9: ['', Validators.required], // Service
      t10: [{ value: 0, disabled: true }, Validators.required] // Total Amount
    });
  }

  private loadDropdownsAndData(): void {
    this.memberService.getDropdowns().subscribe({
      next: (data: AllDropdowns) => {
        this.dropdowns = data;

        if (this.isEditMode && this.syskey) {
          // ADDED: Fetch member detail ONLY AFTER dropdowns are fully loaded
          this.loadMemberDetail(this.syskey);
        } else {
          // Default selections for Create mode
          if (data.genders?.length) this.memberForm.patchValue({ t4: data.genders[0].syskey });
          if (data.plans?.length) this.memberForm.patchValue({ t6: data.plans[0].syskey });
          if (data.services?.length) this.memberForm.patchValue({ t9: data.services[0].syskey });

          this.calculateTotal();
          this.isLoading = false;
        }
      },
      error: (err) => {
        console.error('Failed to load dropdowns', err);
        this.isLoading = false;
      }
    });
  }

  private loadMemberDetail(syskey: string): void {
    this.memberService.getMemberBySyskey(syskey).subscribe({
      next: (res: any) => {
        if (res?.success && res.data) {
          const member = res.data;

          // Safely map display names or IDs back to dropdown syskeys
          const genderSyskey = this.dropdowns?.genders?.find(
            g => g.syskey === member.t4 || g.t1?.toLowerCase() === String(member.t4).toLowerCase()
          )?.syskey || member.t4;

          const planSyskey = this.dropdowns?.plans?.find(
            p => p.syskey === member.t6 || p.t1?.toLowerCase() === String(member.t6).toLowerCase()
          )?.syskey || member.t6;

          const serviceSyskey = this.dropdowns?.services?.find(
            s => s.syskey === member.t9 || s.t1?.toLowerCase() === String(member.t9).toLowerCase()
          )?.syskey || member.t9;

          this.memberForm.patchValue({
            syskey: member.syskey || syskey,
            t1: member.t1,
            t2: member.t2,
            t3: member.t3,
            t4: genderSyskey,
            t5: member.t5 ? member.t5.substring(0, 10) : new Date().toISOString().substring(0, 10),
            t6: planSyskey,
            t7: member.t7,
            t8: member.t8,
            t9: serviceSyskey,
            t10: member.t10
          });

          this.calculateTotal();
        }
        this.isLoading = false;
      },
      error: (err) => {
        console.error('Failed to load member data', err);
        this.isLoading = false;
      }
    });
  }

  private listenToPriceChanges(): void {
    this.memberForm.get('t6')?.valueChanges.subscribe(() => this.calculateTotal());
    this.memberForm.get('t9')?.valueChanges.subscribe(() => this.calculateTotal());
  }

  private calculateTotal(): void {
    if (!this.dropdowns) return;

    const planSyskey = this.memberForm.get('t6')?.value;
    const serviceSyskey = this.memberForm.get('t9')?.value;

    const selectedPlan = this.dropdowns.plans?.find((p) => p.syskey === planSyskey);
    const selectedService = this.dropdowns.services?.find((s) => s.syskey === serviceSyskey);

    const cleanPrice = (val: any): number => {
      if (!val) return 0;
      const numericStr = String(val).replace(/[^0-9.-]+/g, '');
      return parseFloat(numericStr) || 0;
    };

    const planPrice = cleanPrice(selectedPlan?.t2);
    const servicePrice = cleanPrice(selectedService?.t2);

    this.memberForm.patchValue({ t10: planPrice + servicePrice }, { emitEvent: false });
  }

  onSubmit(): void {
    if (this.memberForm.invalid) {
      this.memberForm.markAllAsTouched();
      return;
    }

    const formPayload = this.memberForm.getRawValue();

    // ADDED: Guarantee syskey presence for edit requests
    if (this.isEditMode && this.syskey) {
      formPayload.syskey = this.syskey;
    }

    // Convert t10 to string to align with database/pydantic expectation
    if (formPayload.t10 !== null && formPayload.t10 !== undefined) {
      formPayload.t10 = String(formPayload.t10);
    }

    if (this.isEditMode) {
      this.memberService.updateMember(formPayload).subscribe({
        next: (response: any) => {
          alert(response?.message || 'Member updated successfully!');
          this.router.navigate(['/Dashboard/members/list']);
        },
        error: (err) => {
          console.error('Error updating member:', err);
          alert('Failed to update member.');
        }
      });
    } else {
      this.memberService.addMember(formPayload).subscribe({
        next: (response: any) => {
          alert(response?.message || 'Member added successfully!');
          this.memberForm.reset({
            t5: new Date().toISOString().substring(0, 10),
            t4: this.dropdowns?.genders[0]?.syskey || '',
            t6: this.dropdowns?.plans[0]?.syskey || '',
            t9: this.dropdowns?.services[0]?.syskey || '',
          });
          this.calculateTotal();
        },
        error: (err) => {
          console.error('Error creating member:', err);
          alert('Failed to create member.');
        }
      });
    }
  }
}