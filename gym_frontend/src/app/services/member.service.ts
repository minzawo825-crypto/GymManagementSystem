// src/app/services/member.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, forkJoin, map } from 'rxjs';

export interface DropdownOption {
  syskey: string;
  t1: string;  // Database label
  t2?: string; // Service amount/price
}

export interface AllDropdowns {
  genders: DropdownOption[];
  plans: DropdownOption[];
  services: DropdownOption[];
}


export interface MemberUpdateRequest extends Partial<any> {
  syskey: string;
}

@Injectable({
  providedIn: 'root'
})
export class MemberService {
  private apiUrl = 'http://localhost:8000/api/members_entry_form';

  constructor(private http: HttpClient) {}

  // Explicitly attaches type as an HttpParam to format URL as /dropdown?type=gender
  getDropDown(type: 'gender' | 'plan' | 'service'): Observable<DropdownOption[]> {
    const params = new HttpParams().set('type', type);

    return this.http.get<any>(`${this.apiUrl}/dropdown`, { params }).pipe(
      map(res => res?.data?.data_list || [])
    );
  }

  // Combines individual dropdown requests into a single object for the component
  getDropdowns(): Observable<AllDropdowns> {
    return forkJoin({
      genders: this.getDropDown('gender'),
      plans: this.getDropDown('plan'),
      services: this.getDropDown('service')
    });
  }

 addMember(data: any): Observable<any> {
  return this.http.post<any>(`${this.apiUrl}/entry/create_new_member`, data);
}

  getMembers(filters: any = {}): Observable<any[]> {
    return this.http.post<any[]>(`${this.apiUrl}/entry/member_list`, filters);
  }

  removeMember(syskey: string): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/entry/remove`, { syskey: String(syskey) });
  }
  getMemberById(syskey: string): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/entry/get_member`, { syskey: String(syskey) });
  }

  // ✅ Fixed: 2 arguments passed (url, body)
getMemberBySyskey(syskey: string): Observable<any> {
  return this.http.post<any>(
    `${this.apiUrl}/entry/get_member`,
    { syskey: syskey }
  );
}

  // Update existing member details
  updateMember(payload: any): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/entry/update_member`, payload);
  }
}