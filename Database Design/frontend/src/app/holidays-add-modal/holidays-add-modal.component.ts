import { formatDate } from '@angular/common';
import { Component, Inject, OnInit } from '@angular/core';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';
import {LSRSService} from '../service/lsrs.service';

@Component({
  selector: 'app-holidays-add-modal',
  templateUrl: './holidays-add-modal.component.html',
  styleUrls: ['./holidays-add-modal.component.css']
})
export class HolidaysAddModalComponent implements OnInit {

  holidayName;
  holidayDate;

  months = {
      "Jan": "01",
      "Feb": "02",
      "Mar": "03",
      "Apr": "04",
      "May": "05",
      "Jun": "06",
      "Jul": "07",
      "Aug": "08",
      "Sep": "09",
      "Oct": "10",
      "Nov": "11",
      "Dec": "12"
    }

  constructor(
    public dialogRef: MatDialogRef<HolidaysAddModalComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    private lsrsService: LSRSService) {}

  onNoClick(): void {
    this.dialogRef.close();
  }

  ngOnInit() {
  }

  addHoliday() {
    let formattedDate = formatDate(this.holidayDate, 'longDate', 'en-US');
    let month = formattedDate.slice(0,3);
    let monthCode = this.months[month];
    let day = formattedDate.slice(-8,-6);
    if(day.charAt(0) === " ") {
      day = "0" + day[1];
    }
    let newDate = formattedDate.slice(-4) + "-" + monthCode + "-" + day
    this.lsrsService.addHoliday(this.holidayName, newDate).subscribe(data => {
      this.dialogRef.close();
    })
  }

}
