// Darkwing: Let's get IP-rangerous!
// Copyright (C) 2021 Mark E. Haase <mehaase@gmail.com>
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { LayoutModule } from '@angular/cdk/layout';
import { MainNavComponent } from './main-nav/main-nav.component';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatListModule } from '@angular/material/list';
import { MatMenuModule } from '@angular/material/menu';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatSliderModule } from '@angular/material/slider';
import { MatToolbarModule } from '@angular/material/toolbar';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';

import { DashboardComponent } from './dashboard/dashboard.component';
import { HostsComponent } from './hosts/hosts.component';
import { ScansComponent } from './scans/scans.component';
import { UploadZoneComponent } from './upload-zone/upload-zone.component';

@NgModule({
  declarations: [
    AppComponent,
    DashboardComponent,
    HostsComponent,
    MainNavComponent,
    ScansComponent,
    UploadZoneComponent,
  ],
  imports: [
    AppRoutingModule,
    BrowserAnimationsModule,
    BrowserModule,
    FontAwesomeModule,
    LayoutModule,
    MatButtonModule,
    MatCardModule,
    MatGridListModule,
    MatListModule,
    MatMenuModule,
    MatSidenavModule,
    MatSliderModule,
    MatToolbarModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
