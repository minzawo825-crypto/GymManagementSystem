// import { Component } from '@angular/core';
// import { CommonModule } from '@angular/common';
// import { RouterOutlet } from '@angular/router';
// import { Router } from '@angular/router';

// @Component({
//   selector: 'app-sidebar',
//   standalone: true,
//   imports: [CommonModule,RouterOutlet],
//   templateUrl: './sidebar.component.html',
//   styleUrls: ['./sidebar.component.css']
// })
// export class SidebarComponent {
//   // Default အနေဖြင့် dashboard အား active ဖြစ်စေရန် ထားရှိခြင်း
//   activeMenu: string = 'dashboard';
//  constructor(private router: Router) {}
//   // Menu တစ်ခုချင်းစီ ကလစ်နှိပ်လျှင် active ပြောင်းရန် function
//   setActiveMenu(menuName: string): void {
//     this.activeMenu = menuName;
  
//   if(menuName === 'dashboard'){
//     this.router.navigate(['/Dashboard/home']);
// }
// }
// }

import { Component,signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet,Router, RouterLink, RouterLinkActive } from '@angular/router';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink, RouterLinkActive], // <-- ဒီနေရာမှာ ထည့်ပေးပါ
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.css']
})
export class SidebarComponent {
  isManageMembersOpen = signal<boolean>(false); 

  toggleManageMembers(event: Event) {
    event.preventDefault();
    // 3. 'prev' will automatically be recognized as a boolean now!
    this.isManageMembersOpen.update(prev => !prev); 
  }
  //   
  isGymEquipmentOpen = signal<boolean>(false);
  
  // 💡 Submenu ပေါ် mouse ရောက်နေလားဆိုတာကို မှတ်မယ့် Signal
  isHoveringSubmenu = signal<boolean>(false);

  constructor(private router: Router) {}
  




  toggleGymEquipment(event: Event) {
    event.preventDefault();
    this.isGymEquipmentOpen.update(prev => !prev);
  }

  // 💡 လက်ရှိ Gym Equipment ရဲ့ Submenu screen ထဲ ရောက်နေလား (Active ဖြစ်နေလား) စစ်ပေးမယ့် Helper function
  isSubmenuActive(): boolean {
    return this.router.url.includes('/dashboard/equipment/') || 
           this.router.url === '/dashboard/equipment';
  }
  }
