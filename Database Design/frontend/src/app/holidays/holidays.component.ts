import { Component, OnInit } from '@angular/core';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';
import {HolidaysAddModalComponent} from '../holidays-add-modal/holidays-add-modal.component';
import {LSRSService} from '../service/lsrs.service';

@Component({
  selector: 'app-holidays',
  templateUrl: './holidays.component.html',
  styleUrls: ['./holidays.component.css']
})
export class HolidaysComponent implements OnInit {

  inputData;

  constructor(public dialog: MatDialog, private lsrsService: LSRSService) { }

  ngOnInit() {
    this.lsrsService.getHolidays().subscribe(data => {
      this.inputData = data;
    });
  }

  openDialog() {
    const dialogRef = this.dialog.open(HolidaysAddModalComponent, {
      width: '500px'
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
      this.refreshData();
    });
  }

  refreshData() {
    this.lsrsService.getHolidays().subscribe(data => {
      this.inputData = data;
    });
  }

}
