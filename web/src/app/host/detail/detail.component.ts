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
import { AfterViewInit, Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Host, HostService } from '../host.service';

@Component({
    selector: 'host-detail',
    templateUrl: './detail.component.html',
    styleUrls: ['./detail.component.scss']
})
export class HostDetailComponent implements AfterViewInit {
    public host?: Host;

    private loadingSubject = new BehaviorSubject<boolean>(false);
    public loading$ = this.loadingSubject.asObservable();

    constructor(private hostService: HostService, private route: ActivatedRoute) { }

    ngAfterViewInit() {
        setTimeout(() => this.refreshData());
    }

    private async refreshData() {
        let hostId: string | null = this.route.snapshot.paramMap.get('id');
        this.loadingSubject.next(true);
        try {
            if (hostId != null) {
                this.host = await this.hostService.getHost(hostId);
            }
        } finally {
            this.loadingSubject.next(false);
        }
    }
}
