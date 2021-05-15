import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { MainMenuComponent } from './main-menu/main-menu.component';
import { ReportsComponent } from './reports/reports.component';
import { HolidaysComponent } from './holidays/holidays.component';
import { CitiesComponent } from './cities/cities.component';

const routes: Routes = [
  { path: '', component: MainMenuComponent },
  { path: 'reports', component: ReportsComponent},
  { path: 'holidays', component: HolidaysComponent},
  { path: 'cities', component: CitiesComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
