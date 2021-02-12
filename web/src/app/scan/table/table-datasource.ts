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

import { CollectionViewer, DataSource } from '@angular/cdk/collections';
import { SortDirection } from '@angular/material/sort';
import { BehaviorSubject, Observable, of } from 'rxjs';
import { ScansService } from 'src/app/scans.service';

export interface ScanInfo {
    scan_id: string,
    scanner: string;
    command_line: string;
    started: Date;
    host_count: number;
};

/**
 * Data source for the Table view. This class should
 * encapsulate all logic for fetching and manipulating the displayed data
 * (including sorting, pagination, and filtering).
 */
export class ScanDataSource extends DataSource<ScanInfo> {
    private scansSubject = new BehaviorSubject<ScanInfo[]>([]);
    private loadingSubject = new BehaviorSubject<boolean>(false);

    public loading$ = this.loadingSubject.asObservable();
    public totalCount = 0;

    /**
     * Constructor
     * @param scansService
     */
    constructor(private scansService: ScansService) {
        super();
    }

    connect(_: CollectionViewer): Observable<ScanInfo[]> {
        return this.scansSubject.asObservable();
    }

    disconnect(_: CollectionViewer): void {
        this.scansSubject.complete();
        this.loadingSubject.complete();
    }

    public async loadScans(pageIndex: number, pageSize: number, sortColumn: string,
        sortDirection: SortDirection) {
        this.loadingSubject.next(true);
        try {
            let result = await this.scansService.listScans(pageIndex, pageSize,
                sortColumn, sortDirection);
            this.totalCount = result.total;
            this.scansSubject.next(result.scans);
        }
        finally {
            this.loadingSubject.next(false);
        }
    }
}
