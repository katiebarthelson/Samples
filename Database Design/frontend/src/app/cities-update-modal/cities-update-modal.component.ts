import { Component, Inject, OnInit } from '@angular/core';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';
import {LSRSService} from '../service/lsrs.service';

@Component({
  selector: 'app-cities-update-modal',
  templateUrl: './cities-update-modal.component.html',
  styleUrls: ['./cities-update-modal.component.css']
})
export class CitiesUpdateModalComponent implements OnInit {

  newPopulation;
  showErrorMessage = false;

  constructor(
    public dialogRef: MatDialogRef<CitiesUpdateModalComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    private lsrsService: LSRSService) {}

  onNoClick(): void {
    this.dialogRef.close();
  }
  ngOnInit() {
  }

  updatePopulation() {
    let populationNum = parseInt(this.newPopulation);
    if(isNaN(populationNum)) {
      this.showErrorMessage = true;
    } else {
      this.showErrorMessage = false;
      this.lsrsService.updateCityPopulation(this.data.city_name, this.data.state, populationNum).subscribe(data => {
        this.dialogRef.close();
      })
    }
  }

}
