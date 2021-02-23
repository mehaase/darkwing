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
import { BehaviorSubject, Observable, of } from 'rxjs';
import { ScanListItem, ScanService } from '../scan.service';
import { PageRequest } from '../../page';

/**
 * Data source for the Table view. This class should
 * encapsulate all logic for fetching and manipulating the displayed data
 * (including sorting, pagination, and filtering).
 */
export class ScanDataSource extends DataSource<ScanListItem> {
    private scansSubject = new BehaviorSubject<ScanListItem[]>([]);
    private loadingSubject = new BehaviorSubject<boolean>(false);

    public loading$ = this.loadingSubject.asObservable();
    public totalCount = 0;

    /**
     * Constructor
     * @param scansService
     */
    constructor(private scansService: ScanService) {
        super();
    }

    connect(_: CollectionViewer): Observable<ScanListItem[]> {
        return this.scansSubject.asObservable();
    }

    disconnect(_: CollectionViewer): void {
        this.scansSubject.complete();
        this.loadingSubject.complete();
    }

    public async loadScans(page: PageRequest) {
        this.loadingSubject.next(true);
        try {
            let result = await this.scansService.listScans(page);
            this.totalCount = result.totalCount;
            this.scansSubject.next(result.items);
        }
        finally {
            this.loadingSubject.next(false);
        }
    }
}
