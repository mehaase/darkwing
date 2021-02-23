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
import { Component, ViewChild } from '@angular/core';
import { ScanService } from '../scan.service';
import { ScanTableComponent } from '../table/table.component';

/**
 * Display scan data and allow the user to submit scan data.
 */
@Component({
    selector: 'scan-index',
    templateUrl: './index.component.html',
    styleUrls: ['./index.component.scss']
})
export class ScanIndexComponent {
    @ViewChild(ScanTableComponent) table!: ScanTableComponent;

    /**
     * Constructor
     *
     * @param service
     */
    constructor(private service: ScanService) { }

    /**
     * Upload scans to the server.
     *
     * @param files A list of scans to upload
     */
    public async uploadFiles(files: FileList) {
        await this.service.uploadScans(files);
        this.table.refresh();
    }
}
