import { Component, OnInit } from '@angular/core';
import {LSRSService} from '../service/lsrs.service';

@Component({
  selector: 'app-reports',
  templateUrl: './reports.component.html',
  styleUrls: ['./reports.component.css']
})
export class ReportsComponent implements OnInit {

  report1data;
  report1headers;

  report2data;
  report2headers;

  report3data;
  report3headers;

  report4data;
  report4headers;

  report5data;
  report5headers;

  report6data;
  report6headers;

  report7data;
  report7headers;

  report8data;
  report8headers;

  report9data;
  report9headers;

  states = [
    {
        "name": "Alabama",
        "abbreviation": "AL"
    },
    {
        "name": "Alaska",
        "abbreviation": "AK"
    },
    {
        "name": "American Samoa",
        "abbreviation": "AS"
    },
    {
        "name": "Arizona",
        "abbreviation": "AZ"
    },
    {
        "name": "Arkansas",
        "abbreviation": "AR"
    },
    {
        "name": "California",
        "abbreviation": "CA"
    },
    {
        "name": "Colorado",
        "abbreviation": "CO"
    },
    {
        "name": "Connecticut",
        "abbreviation": "CT"
    },
    {
        "name": "Delaware",
        "abbreviation": "DE"
    },
    {
        "name": "District Of Columbia",
        "abbreviation": "DC"
    },
    {
        "name": "Federated States Of Micronesia",
        "abbreviation": "FM"
    },
    {
        "name": "Florida",
        "abbreviation": "FL"
    },
    {
        "name": "Georgia",
        "abbreviation": "GA"
    },
    {
        "name": "Guam",
        "abbreviation": "GU"
    },
    {
        "name": "Hawaii",
        "abbreviation": "HI"
    },
    {
        "name": "Idaho",
        "abbreviation": "ID"
    },
    {
        "name": "Illinois",
        "abbreviation": "IL"
    },
    {
        "name": "Indiana",
        "abbreviation": "IN"
    },
    {
        "name": "Iowa",
        "abbreviation": "IA"
    },
    {
        "name": "Kansas",
        "abbreviation": "KS"
    },
    {
        "name": "Kentucky",
        "abbreviation": "KY"
    },
    {
        "name": "Louisiana",
        "abbreviation": "LA"
    },
    {
        "name": "Maine",
        "abbreviation": "ME"
    },
    {
        "name": "Marshall Islands",
        "abbreviation": "MH"
    },
    {
        "name": "Maryland",
        "abbreviation": "MD"
    },
    {
        "name": "Massachusetts",
        "abbreviation": "MA"
    },
    {
        "name": "Michigan",
        "abbreviation": "MI"
    },
    {
        "name": "Minnesota",
        "abbreviation": "MN"
    },
    {
        "name": "Mississippi",
        "abbreviation": "MS"
    },
    {
        "name": "Missouri",
        "abbreviation": "MO"
    },
    {
        "name": "Montana",
        "abbreviation": "MT"
    },
    {
        "name": "Nebraska",
        "abbreviation": "NE"
    },
    {
        "name": "Nevada",
        "abbreviation": "NV"
    },
    {
        "name": "New Hampshire",
        "abbreviation": "NH"
    },
    {
        "name": "New Jersey",
        "abbreviation": "NJ"
    },
    {
        "name": "New Mexico",
        "abbreviation": "NM"
    },
    {
        "name": "New York",
        "abbreviation": "NY"
    },
    {
        "name": "North Carolina",
        "abbreviation": "NC"
    },
    {
        "name": "North Dakota",
        "abbreviation": "ND"
    },
    {
        "name": "Northern Mariana Islands",
        "abbreviation": "MP"
    },
    {
        "name": "Ohio",
        "abbreviation": "OH"
    },
    {
        "name": "Oklahoma",
        "abbreviation": "OK"
    },
    {
        "name": "Oregon",
        "abbreviation": "OR"
    },
    {
        "name": "Palau",
        "abbreviation": "PW"
    },
    {
        "name": "Pennsylvania",
        "abbreviation": "PA"
    },
    {
        "name": "Puerto Rico",
        "abbreviation": "PR"
    },
    {
        "name": "Rhode Island",
        "abbreviation": "RI"
    },
    {
        "name": "South Carolina",
        "abbreviation": "SC"
    },
    {
        "name": "South Dakota",
        "abbreviation": "SD"
    },
    {
        "name": "Tennessee",
        "abbreviation": "TN"
    },
    {
        "name": "Texas",
        "abbreviation": "TX"
    },
    {
        "name": "Utah",
        "abbreviation": "UT"
    },
    {
        "name": "Vermont",
        "abbreviation": "VT"
    },
    {
        "name": "Virgin Islands",
        "abbreviation": "VI"
    },
    {
        "name": "Virginia",
        "abbreviation": "VA"
    },
    {
        "name": "Washington",
        "abbreviation": "WA"
    },
    {
        "name": "West Virginia",
        "abbreviation": "WV"
    },
    {
        "name": "Wisconsin",
        "abbreviation": "WI"
    },
    {
        "name": "Wyoming",
        "abbreviation": "WY"
    }
];

showReportThreeData;

reportFiveMonths = [
  {
    "name": "January",
    "value": "01"
  },
  {
    "name": "February",
    "value": "02"
  },
  {
    "name": "March",
    "value": "03"
  },
  {
    "name": "April",
    "value": "04"
  },
  {
    "name": "May",
    "value": "05"
  },
  {
    "name": "June",
    "value": "06"
  },
  {
    "name": "July",
    "value": "07"
  },
  {
    "name": "August",
    "value": "08"
  },
  {
    "name": "September",
    "value": "09"
  },
  {
    "name": "October",
    "value": "10"
  },
  {
    "name": "November",
    "value": "11"
  },
  {
    "name": "December",
    "value": "12"
  }

];
reportFiveYearsObject;
reportFiveYears;
selectedYear;
selectedMonth;
showReportFiveData;

reportEightKeys = [];


  constructor(private lsrsService:LSRSService) { }

  ngOnInit() {
    this.reportOne();
  }

  reportClicked(event) {
    if(event.index === 0) {
      this.reportOne();
    } else if(event.index === 1) {
      this.reportTwo();
    } else if(event.index === 2) {
      
    } else if(event.index === 3) {
      this.reportFour();
    } else if(event.index === 4) {
      this.lsrsService.getReportFiveYears().subscribe(data => {
        this.reportFiveYearsObject = data;
        this.reportFiveYears = [];
        for(let i = 0; i < this.reportFiveYearsObject.length; i++) {
          this.reportFiveYears.push(this.reportFiveYearsObject[i].year);
        }
        this.reportFiveYears.sort();
      })
    } else if(event.index === 5) {
      this.reportSix();
    } else if(event.index === 6) {
      this.reportSeven();
    } else if(event.index === 7) {
      this.reportEight();
    } else if(event.index === 8) {
      this.reportNine();
    } 
  }

  reportOne() {
    this.lsrsService.getReportOne().subscribe(data => {
      this.report1data = data;
    });
  
    this.report1headers = ['category_name', 'product_count', 'min_retail_price', 'avg_retail_price', 'max_retail_price']
  }

  reportTwo() {
    this.lsrsService.getReportTwo().subscribe(data => {
      this.report2data = data;
    });

    this.report2headers = ['pid', 'product_name', 'retail_price', 'total_quantity_sold', 'discounted_quantity_sold', 'not_discounted_quantity_sold', 'actual_revenue', 'predicted_revenue', 'revenue_difference']

  }

  reportThree(state) {
    this.showReportThreeData = true;
    this.lsrsService.getReportThree(state).subscribe(data => {
      this.report3data = data;
    });
  
    this.report3headers = ['store_number', 'street_address', 'city_name', 'yearly_revenue', 'sale_year']
  }

  reportFour() {
    this.lsrsService.getReportFour().subscribe(data => {
      this.report4data = data;
    });
  
    this.report4headers = ['year', 'total_units_sold', 'avg_quantity', 'groundhog_day_sales']
  }

  reportFive() {
    this.showReportFiveData = true;
    this.lsrsService.getReportFive(this.selectedYear,this.selectedMonth).subscribe(data => {
      this.report5data = data;
    });

    this.report5headers = ['category_name', 'state', 'sum']
  
  }

  reportSix() {
    this.lsrsService.getReportSix().subscribe(data => {
      this.report6data = data;
    });
    
    this.report6headers = ['year', 'small', 'medium', 'large', 'extra_large']
  }

  reportSeven() {
    this.lsrsService.getReportSeven().subscribe(data => {
      this.report7data = data;
    });

    this.report7headers = ['month', 'no_childcare', 'limit30', 'limit45', 'limit60'];
  }

  reportEight() {
    this.lsrsService.getReportEight().subscribe(data => {
      this.report8data = data;
      console.log(this.report8data);
      console.log(Object.keys(this.report8data[0]));
      for(let i = 0; i < this.report8data.length; i++) {
        this.reportEightKeys.push(Object.keys(this.report8data[i])[0]);
      }
      console.log(this.reportEightKeys);
    })
  }

  reportNine() {
    this.lsrsService.getReportNine().subscribe(data => {
      this.report9data = data;
    })

    this.report9headers = ['pid', 'product_name', 'sold_during_campaign', 'sold_outside_campaign', 'ad_difference']
  }

}
