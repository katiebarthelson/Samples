import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable() 
export class LSRSService {
    constructor(private http: HttpClient) {}

    getMainMenu() {
        const url = 'http://127.0.0.1:5000/mainmenu';
        return this.http.get(url);
    }

    getCityPopulation() {
        const url = 'http://127.0.0.1:5000/population';
        return this.http.get(url);
    }

    updateCityPopulation(cityName, state, population) {
        const url = 'http://127.0.0.1:5000/population';
        const body = {
            city_name: cityName,
            state: state,
            population: population
        }
        return this.http.post(url, body);
    }

    getHolidays() {
        const url = 'http://127.0.0.1:5000/holiday';
        return this.http.get(url);
    }

    addHoliday(name, date) {
        const body = {
            date: date,
            holiday_names: name
        };
        const url = 'http://127.0.0.1:5000/holiday';
        return this.http.post(url, body);
    }

    getReportOne() {
        const url = 'http://127.0.0.1:5000/report1';
        return this.http.get(url);
    }

    getReportTwo() {
        const url = 'http://127.0.0.1:5000/report2';
        return this.http.get(url);
    }

    getReportThree(state) {
        const url = `http://127.0.0.1:5000/report3/${state}`;
        return this.http.get(url);
    }

    getReportFour() {
        const url = 'http://127.0.0.1:5000/report4';
        return this.http.get(url);
    }

    getReportFiveYears() {
        const url = 'http://127.0.0.1:5000/report5/year';
        return this.http.get(url);
    }

    getReportFive(year, month) {
        const url = `http://127.0.0.1:5000/report5/${year}/${month}`;
        return this.http.get(url);
    }

    getReportSix() {
        const url = 'http://127.0.0.1:5000/report6';
        return this.http.get(url);
    }

    getReportSeven() {
        const url = 'http://127.0.0.1:5000/report7';
        return this.http.get(url);
    }

    getReportEight() {
        const url = 'http://127.0.0.1:5000/report8';
        return this.http.get(url);
    }

    getReportNine() {
        const url = 'http://127.0.0.1:5000/report9';
        return this.http.get(url);
    }

    
}