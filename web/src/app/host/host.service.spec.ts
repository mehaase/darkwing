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

import { TestBed } from '@angular/core/testing';

import { HostService } from './host.service';

describe('HostService', () => {
    let service: HostService;

    beforeEach(() => {
        TestBed.configureTestingModule({});
        service = TestBed.inject(HostService);
    });

    it('should be created', () => {
        expect(service).toBeTruthy();
    });
});
