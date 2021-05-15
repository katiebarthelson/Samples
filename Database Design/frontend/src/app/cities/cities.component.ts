import { Component, OnInit } from '@angular/core';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';
import {CitiesUpdateModalComponent} from '../cities-update-modal/cities-update-modal.component';
import {LSRSService} from '../service/lsrs.service';

@Component({
  selector: 'app-cities',
  templateUrl: './cities.component.html',
  styleUrls: ['./cities.component.css']
})
export class CitiesComponent implements OnInit {

  inputData;

  constructor(public dialog: MatDialog, private lsrsService: LSRSService) { }

  ngOnInit() {
    this.lsrsService.getCityPopulation().subscribe(data => {
      this.inputData = data;
    });
  }

  openDialog(data:any) {
    const dialogRef = this.dialog.open(CitiesUpdateModalComponent, {
      width: '500px',
      data: data
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
      this.refreshData();
    });
  }

  refreshData() {
    this.lsrsService.getCityPopulation().subscribe(data => {
      this.inputData = data;
    });
  }

}
