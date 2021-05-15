import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {

  constructor(private router: Router) { }

  ngOnInit() {
  }

  goToReports() {
    this.router.navigate(['/reports']);
  }

  goToHome() {
    this.router.navigate(['/']);
  }

  goToHolidays() {
    this.router.navigate(['/holidays']);
  }

  goToCities() {
    this.router.navigate(['/cities']);
  }

}
