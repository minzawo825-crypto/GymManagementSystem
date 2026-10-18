// src/app/members/member-list.component.ts
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MemberService } from '../services/member.service';

@Component({
  selector: 'app-member-list',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './member-entry-list.component.html',
  styleUrls: ['./member-entry-list.component.css']
})
export class MemberEntryListComponent implements OnInit {
  members: any[] = [];
  pagination: any = {};
  isLoading = true;

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
}