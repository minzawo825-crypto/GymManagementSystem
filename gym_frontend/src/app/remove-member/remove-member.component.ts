// src/app/remove-member/remove-member.component.ts
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MemberService } from '../services/member.service';

@Component({
  selector: 'app-remove-member',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './remove-member.component.html',
  styleUrls: ['./remove-member.component.css']
})
export class RemoveMemberComponent implements OnInit {
   members: any[] = [];
    pagination: any = {};
    isLoading = true;
    successMessage: string | null = null;
    errorMessage: string | null = null;
  
    constructor(private memberService: MemberService) {}
  
    ngOnInit(): void {
      this.fetchMembers();
    }
  
    fetchMembers(): void {
      this.memberService.getMembers().subscribe({
        next: (response: any) => {
          // ✅ Safely extract items and pagination from response wrapper
          this.members = response?.data?.items || [];
          this.pagination = response?.data?.pagination || {};
          this.isLoading = false;
        },
        error: (err) => {
          console.error('Error fetching members:', err);
          this.isLoading = false;
        }
      });
    }
  
  // Remove Action Handler
 remove(syskey: any): void {
    if (!syskey) return;

    if (confirm('Are you sure you want to remove this member?')) {
      this.memberService.removeMember(String(syskey)).subscribe({
        next: (res: any) => {
          if (res && res.success) {
            // Set UI success message
            this.successMessage = res.message || 'Member deleted successfully!';
            this.errorMessage = null;

            // Instantly remove item from table list
            this.members = this.members.filter(m => String(m.syskey) !== String(syskey));

            // Automatically hide message after 3 seconds
            setTimeout(() => {
              this.successMessage = null;
            }, 3000);
          } else {
            this.errorMessage = res.message || 'Failed to remove member.';
          }
        },
        error: (err) => {
          this.errorMessage = 'An error occurred while removing the member.';
          console.error(err);
        }
      });
    }
  }
}