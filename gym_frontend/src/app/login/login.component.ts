import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { CommonModule } from '@angular/common'; 

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  loginForm!: FormGroup;
  errorMessage = '';

  constructor(
    private authService: AuthService,
    private router: Router,
    private formBuilder: FormBuilder
  ) {}

  ngOnInit(): void {
    localStorage.clear();
    sessionStorage.clear();

    this.loginForm = this.formBuilder.group({
      username: ['', [Validators.required]],
      
      password: ['', [Validators.required]] 
    });
  }
    
  onSubmit(): void {
    this.errorMessage = ''; 

    if (this.loginForm.invalid) {
      this.loginForm.markAllAsTouched();
      return;
    }

    this.authService.login(this.loginForm.value).subscribe({
      next: (response) => {
        console.log('Login Response:', response); 

        // 💡 resp.success_response Structure 
        if ((response.status_code === 200 || response.data) && response.data?.access_token) {

          
          localStorage.setItem('token', response.data.access_token);
          if (response.data.user?.username) {
            localStorage.setItem('username', response.data.user.username);
          }

          // Dashboard
          this.router.navigate(['Dashboard']);
        } else {
          this.errorMessage = response.message || 'Login failed. Invalid response from server.';
        }
      },

      error: (err) => {
        console.error('Login Error:', err);
        // Backend မှ error response Message 
        this.errorMessage =
          err.error?.message ||
          'Login Failed. Please check your credentials and try again.';
      }
    });
  }
}