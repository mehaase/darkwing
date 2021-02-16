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

import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ScansService } from 'src/app/scans.service';

@Component({
    selector: 'scan-detail',
    templateUrl: './detail.component.html',
    styleUrls: ['./detail.component.scss']
})
export class ScanDetailComponent implements OnInit {
    public scan?: Record<string, any>;

    constructor(private route: ActivatedRoute, private scansService: ScansService) { }

    ngOnInit(): void {
        this.load();
    }

    private async load() {
        let id: string | null = this.route.snapshot.paramMap.get('id');
        if (id) {
            this.scan = await this.scansService.getScan(id);
        }
    }
}
