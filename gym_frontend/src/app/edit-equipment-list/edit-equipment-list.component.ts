import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { EquipmentService } from '../services/equipment.service';


@Component({
  selector: 'app-edit-member-list',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './edit-equipment-list.component.html',
  styleUrl: './edit-equipment-list.component.css'
})
export class EditEquipmentListComponent implements OnInit {
  equipments: any[] = [];
  isLoading: boolean = false;
  pagination: any = {};
  successMessage: string | null = null;
  errorMessage: string | null = null;
  constructor(
    private equipmentService: EquipmentService, 
    private router: Router
  ) {}

  ngOnInit(): void {
      this.fetchEquipments();
    }
  
    fetchEquipments(): void {
      this.equipmentService.getEquipments().subscribe({
        next: (response: any) => {
          // ✅ Safely extract items and pagination from response wrapper
          this.equipments = response?.data?.itemname || [];
          this.pagination = response?.data?.pagination || {};
          this.isLoading = false;
        },
        error: (err) => {
          console.error('Error fetching equipment:', err);
          this.isLoading = false;
        }
      });
    }
  

 onEdit(equipment: any): void {
  // Check if member exists and extract syskey (or fallbacks if named differently)
  const id = equipment?.syskey || equipment?.id || equipment?._id;

  if (!id) {
    console.error('Failed to navigate: syskey is undefined in member object', equipment);
    return;
  }

  // Segment 0: '/Dashboard/members/entry', Segment 1: id
  this.router.navigate(['/Dashboard/equipment/add', id]);
}

remove(itemOrKey: any): void {
  if (!itemOrKey) return;

  // Extract key string if full object was passed from template
  const syskey = typeof itemOrKey === 'object' ? (itemOrKey.syskey || itemOrKey.id) : itemOrKey;

  if (confirm('Are you sure you want to remove this equipment?')) {
    this.equipmentService.removeEquipment(syskey).subscribe({
      next: (res: any) => {
        if (res && res.success) {
          this.successMessage = res.message || 'Equipment deleted successfully!';
          
          // Remove from local array using primitive string check
          this.equipments = this.equipments.filter(
            m => String(m.syskey || m.id) !== String(syskey)
          );
        } else {
          this.errorMessage = res.message || 'Failed to remove equipment.';
        }
      },
      error: (err) => {
        this.errorMessage = 'An error occurred while removing equipment.';
        console.error(err);
      }
    });
  }
}
     
}


