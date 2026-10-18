// src/app/services/member.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, forkJoin, map } from 'rxjs';



@Injectable({
  providedIn: 'root'
})
export class EquipmentService {
  private apiUrl = 'http://localhost:8000/api/equipments_entry_form';

  constructor(private http: HttpClient) {}

 

 addEquipment(data: any): Observable<any> {
  return this.http.post<any>(`${this.apiUrl}/entry/create_new_equipment`, data);
}

  getEquipments(filters: any = {}): Observable<any[]> {
    return this.http.post<any[]>(`${this.apiUrl}/entry/get_equipment_list`, filters);
  }

  removeEquipment(syskey: any): Observable<any> {
  const cleanKey = typeof syskey === 'object' && syskey !== null 
    ? (syskey.syskey || syskey.id) 
    : syskey;

  return this.http.post('/api/equipment/entry/remove', { syskey: String(cleanKey) });
}
}