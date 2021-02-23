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

import { Injectable } from '@angular/core';
import { PageRequest, PageResult } from '../page';
import { ServerService } from '../server.service';

export class Host {
    private constructor(
        public hostId: string,
        public started: Date,
        public completed: Date,
        public state: string,
        public stateReason: string,
        public addresses: Array<string>,
        public hostnames: Array<string>,
        public coverImage: string,
        public ports: Array<HostPort>,
    ) {
    }

    public static fromJson(json: Record<string, any>) {
        let ports: Array<HostPort> = new Array();
        for (let portJson of json['ports']) {
            ports.push(HostPort.fromJson(portJson));
        }
        return new Host(
            json['host_id'],
            json['started'],
            json['completed'],
            json['state'],
            json['state_reason'],
            json['addresses'],
            json['hostnames'],
            json['cover_image'],
            ports,
        );
    }
}

export class HostListItem {
    private constructor(
        public hostId: string,
        public started: Date,
        public completed: Date,
        public state: string,
        public stateReason: string,
        public addresses: Array<string>,
        public hostnames: Array<string>,
        public coverImage: string,
    ) {
    }

    public static fromJson(json: Record<string, any>) {
        return new HostListItem(
            json['host_id'],
            json['started'],
            json['completed'],
            json['state'],
            json['state_reason'],
            json['addresses'],
            json['hostnames'],
            json['coverImage'],
        );
    }
}

export class HostPort {
    private constructor(
        public number: number,
        public transport: string,
        public state: string,
        public stateReason: string,
        public service: string,
    ) {

    }

    public static fromJson(json: Record<string, any>) {
        return new HostPort(
            json['number'],
            json['transport'],
            json['state'],
            json['state_reason'],
            json['service'],
        );
    }
}

export class HostPortService {
    private constructor(
        private name: string,
        private product: string,
        private version: string,
        private method: string,
        private confidence: string,
        private cpes: string,
    ) {

    }

    public static fromJson(json: Record<string, any>) {
        return new HostPortService(
            json['name'],
            json['product'],
            json['version'],
            json['method'],
            json['confidence'],
            json['cpes'],
        );
    }
}

@Injectable({
    providedIn: 'root'
})
export class HostService {

    constructor(private serverService: ServerService) {

    }

    public async getHost(hostId: string): Promise<Host> {
        let json = await this.serverService.invoke('get_host', [hostId]);
        return Host.fromJson(json);
    }

    public async listHosts(page: PageRequest): Promise<PageResult<HostListItem>> {
        let json = await this.serverService.invoke('list_hosts', [page.toJson()]);
        let items = new Array<HostListItem>();
        for (let item of json['items']) {
            items.push(HostListItem.fromJson(item));
        }
        return new PageResult(json['total_count'], items);
    }
}
