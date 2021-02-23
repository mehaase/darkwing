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

import { BehaviorSubject } from 'rxjs';
import { AfterViewInit, Component, ViewChild } from '@angular/core';
import { MatPaginator } from '@angular/material/paginator';
import { PageRequest } from '../../page';
import { HostListItem, HostService } from '../host.service';

@Component({
    selector: 'host-index',
    templateUrl: './index.component.html',
    styleUrls: ['./index.component.scss']
})
export class HostIndexComponent implements AfterViewInit {
    public hostCount!: number;
    public hosts!: Array<HostListItem>;

    private loadingSubject = new BehaviorSubject<boolean>(false);
    public loading$ = this.loadingSubject.asObservable();

    @ViewChild(MatPaginator) paginator!: MatPaginator;

    constructor(private hostService: HostService) { }

    ngAfterViewInit() {
        this.paginator.page
            .subscribe((_: any) => { this.refreshData() });
        setTimeout(() => this.refreshData());
    }

    private async refreshData() {
        this.loadingSubject.next(true);
        let page = new PageRequest(
            this.paginator.pageIndex,
            this.paginator.pageSize,
            'todo', //TODO
            'asc'
        );
        try {
            let result = await this.hostService.listHosts(page);
            this.hostCount = result.totalCount;
            this.hosts = result.items;
        } finally {
            this.loadingSubject.next(false);
        }
    }
}
