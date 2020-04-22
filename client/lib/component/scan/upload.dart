// Darkwing: Your pen test sidekick!
// Copyright (C) 2020 Mark E. Haase <mehaase@gmail.com>
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

import 'dart:convert';
import 'dart:html';
import 'dart:typed_data';

import 'package:angular/angular.dart';
import 'package:angular_components/angular_components.dart';
import 'package:logging/logging.dart';

import 'package:darkwing/service/server.dart';

final log = Logger('ScanUploadView');

@Component(
    selector: 'scan-upload',
    templateUrl: 'upload.html',
    styleUrls: const [
      'upload.css'
    ],
    directives: const [
      coreDirectives,
      MaterialButtonComponent,
      MaterialProgressComponent,
    ])
class ScanUploadView {
  bool dragOver = false;
  num uploadProgress;
  bool uploadProgressIndeterminate = false;

  ServerService _server;

  /// Constructor.
  ScanUploadView(this._server);

  /// Handle when an item is dragged over the target.
  handleDragOver(MouseEvent e) {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'copy';
    this.dragOver = true;
  }

  /// Handle when an item is dragged back outside the target.
  handleDragLeave(MouseEvent e) {
    this.dragOver = false;
  }

  /// Handle when an item is dropped on the target.
  handleDrop(MouseEvent e) {
    e.preventDefault();
    this.dragOver = false;
    this._readFile(e.dataTransfer.files[0]);
  }

  /// Handle the file dialog.
  uploadScan(FileUploadInputElement input) {
    this._readFile(input.files[0]);
  }

  /// A helper which reads a File object and then calls _uploadFile.
  _readFile(File f) {
    var reader = FileReader();
    reader.onProgress.listen((event) {
      log.info('Upload event ${event.loaded}/${event.total}');
      this.uploadProgress = event.loaded * 100 / event.total;
    });
    reader.onLoadEnd.listen((event) {
      log.info('Upload complete.');
      this.uploadProgress = 100;
      this.uploadProgressIndeterminate = true;
      this._uploadFile(reader.result);
    });
    reader.readAsArrayBuffer(f);
  }

  /// Uploads the file to the server.
  _uploadFile(Uint8List data) async {
    var encodedData = base64Encode(data);
    try {
      var result = await this
          ._server
          .sendRequest('upload_scan', {'base64_data': encodedData});
      window.console.log(result);
    } finally {
      this.uploadProgress = null;
      this.uploadProgressIndeterminate = false;
    }
  }
}
