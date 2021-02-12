import { Injectable } from '@angular/core';
import { SortDirection } from '@angular/material/sort';
import { LogService } from './log.service';
import { ServerService } from './server.service';

@Injectable({
  providedIn: 'root'
})
export class ScansService {
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
  public async listScans(pageIndex: number, pageSize: number, sortColumn: string,
    sortDirection: SortDirection): Promise<Record<string, any>> {
    let result = await this.serverService.invoke('list_scans', [pageIndex, pageSize,
      sortColumn, sortDirection == "asc"]);
    return result;
  }
}
