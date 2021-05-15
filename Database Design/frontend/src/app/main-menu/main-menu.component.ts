import { Component, OnInit } from '@angular/core';
import { LSRSService } from '../service/lsrs.service';

@Component({
  selector: 'app-main-menu',
  templateUrl: './main-menu.component.html',
  styleUrls: ['./main-menu.component.css']
})
export class MainMenuComponent implements OnInit {

  data = {
    counts: []
  };
  dataHeaders = ['Advertising Campaigns', 'Food Store', 'Product', 'Childcare Store', 'Store'];
  inputData;

  constructor(private lsrsService: LSRSService) { }

  ngOnInit() {
    this.lsrsService.getMainMenu().subscribe(data => {
      this.inputData = data;
      this.data = {
        counts: [
          {
            name: "Advertising Campaigns",
            count: this.inputData[0].campaign_count
          },
          {
            name: "Food Store",
            count: this.inputData[1].food_store_count
          }, 
          {
            name: "Product",
            count: this.inputData[2].product_count
          }, 
          {
            name: "Childcare Store",
            count: this.inputData[3].childcare_store_count
          },
          {
            name: "Store",
            count: this.inputData[4].store_count
          }
        ]
      }
    });
  }

}
