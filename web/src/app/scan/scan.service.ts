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
import { LogService } from '../log.service';
import { PageRequest, PageResult } from '../page';
import { ServerService } from '../server.service';

export class ScanListItem {
    private constructor(
        private scanId: string,
        private scanner: string,
        private commandLine: string,
        private started: Date,
        private hostCount: number,
    ) {

    }

    public static fromJson(json: Record<string, any>) {
        return new ScanListItem(
            json['scan_id'],
            json['scanner'],
            json['command_line'],
            json['started'],
            json['host_count'],
        )
    }
};

@Injectable({
    providedIn: 'root'
})
export class ScanService {
    /**
     * Constructor
     * @param logService
     * @param serverService
     */
    constructor(private log: LogService, private serverService: ServerService) {
    }

    /**
     * Upload scan files to the server.
     * @param files
     */
    public async uploadScans(files: FileList) {
        this.log.info(`Uploading ${files.length} files.`);
        for (let i = 0; i < files.length; i++) {
            let file = files[i];
            this.log.info(`Uploading: ${file.name}`);
            let fileData = await file.arrayBuffer();
            //TODO does this handle large files?
            let fileData64 = btoa(String.fromCharCode(...new Uint8Array(fileData)));
            this.serverService.invoke('upload_scan', { 'base64_data': fileData64 });
        }
    }

    public async getScan(id: string): Promise<Record<string, any>> {
        return await this.serverService.invoke('get_scan', [id]);
    }

    /**
     * Fetch a page of scan data.
     */
    public async listScans(page: PageRequest): Promise<PageResult<ScanListItem>> {
        let json = await this.serverService.invoke('list_scans', [page.toJson()]);
        let items = new Array<ScanListItem>();
        for (let item of json['items']) {
            items.push(ScanListItem.fromJson(item));
        }
        return new PageResult(json['total_count'], items);
    }
}
