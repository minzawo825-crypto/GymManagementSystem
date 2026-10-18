// import { Routes } from '@angular/router';
// import { LoginComponent } from './login/login.component';
// import { SidebarComponent } from './sidebar/sidebar.component';


// export const routes: Routes = [
//     {path: 'login', component: LoginComponent},
//     {path: 'sidebar', component: SidebarComponent},
//     {path: 'd', component: SidebarComponent},
//      {path: '', redirectTo: 'sidebar', pathMatch: 'full'},
    
// ];
import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { SidebarComponent } from './Dashboard/sidebar.component';
import { DashboardhomeComponent } from './Dashboard_home/dashboardhome.component'; // အသစ်ဆောက်ခဲ့တဲ့ component
import { MemberEntryComponent } from './member-entry/member-entry.component';
import { MemberEntryListComponent } from './member-entry-list/member-entry-list.component';
import { RemoveMemberComponent } from './remove-member/remove-member.component';
import { EditMemberListComponent } from './edit-member-list/edit-member-list.component';
import { EquipmentEntryComponent } from './equipment-entry/equipment-entry.component';
import { EditEquipmentListComponent } from './edit-equipment-list/edit-equipment-list.component';

export const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
 
  
  {
    path: 'Dashboard', component: SidebarComponent, // ဒါက ပင်မ Layout ဖြစ်ပြီး ဘယ်ဘက်မှာ Sidebar ရှိနေမယ်
   children: [
      { 
        path: '',  redirectTo: 'Dashboard_home', pathMatch: 'full' 
      },
      { 
        path: 'Dashboard_home', component: DashboardhomeComponent 
      } ,// /dashboard/home 
       
        { path: 'members/entry', component: MemberEntryComponent },
        { path: 'members/entry/:syskey', component: MemberEntryComponent },
        { path: 'members/list', component: MemberEntryListComponent },
        { path: 'members/remove', component: RemoveMemberComponent },
        { path: 'members/update', component: EditMemberListComponent },
        { path: 'members/update/:syskey', component: EditMemberListComponent },
         { path: 'equipment/add', component: EquipmentEntryComponent },
         { path: 'equipment/list', component:  EditEquipmentListComponent },
      //  URL: /Dashboard/members/ent
    ]
  },
 
  { 
    path: '', redirectTo: 'Dashboard', pathMatch: 'full' 
  } ,
 
];

