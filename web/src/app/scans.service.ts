import { Injectable } from '@angular/core';
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
  constructor(
    private log: LogService,
    private serverService: ServerService) {

  }

  /**
   * Upload scan files to the server.
   *
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
}
