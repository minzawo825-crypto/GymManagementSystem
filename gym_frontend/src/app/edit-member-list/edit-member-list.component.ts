import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { MemberService } from '../services/member.service';


@Component({
  selector: 'app-edit-member-list',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './edit-member-list.component.html',
  styleUrl: './edit-member-list.component.css'
})
export class EditMemberListComponent implements OnInit {
  members: any[] = [];
  isLoading: boolean = false;
  pagination: any = {};

  constructor(
    private memberService: MemberService, 
    private router: Router
  ) {}

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
  

 onEdit(member: any): void {
  // Check if member exists and extract syskey (or fallbacks if named differently)
  const id = member?.syskey || member?.id || member?._id;

  if (!id) {
    console.error('Failed to navigate: syskey is undefined in member object', member);
    return;
  }

  // Segment 0: '/Dashboard/members/entry', Segment 1: id
  this.router.navigate(['/Dashboard/members/entry', id]);
}
}