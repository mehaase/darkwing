import {
  Component,
  ElementRef,
  EventEmitter,
  HostBinding,
  HostListener,
  Output,
  ViewChild,
} from '@angular/core';
import { faFileUpload } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-upload-zone',
  templateUrl: './upload-zone.component.html',
  styleUrls: ['./upload-zone.component.scss']
})
export class UploadZoneComponent {
  @HostBinding('class.file-over') fileOver: boolean = false;
  @Output() filesDropped = new EventEmitter();
  @ViewChild('filePicker') filePicker?: ElementRef;

  faFileUpload = faFileUpload;

  constructor() {
    console.log('constructor');
  }

  public uploadFiles(files: FileList) {
    console.log("Uploading files");
    console.log(files);
  }

  public filesPicked(event: Event) {
    console.log(event);
    if (this.filePicker) {
      this.uploadFiles(this.filePicker.nativeElement.files);
      //TODO clear existing files;
    } else {
      console.warn('FilePicker not initialized.');
    }
  }

  public selectFiles() {
    if (this.filePicker) {
      this.filePicker.nativeElement.click();
    } else {
      console.warn('FilePicker not initialized.');
    }
  }

  @HostListener('dragover', ['$event']) onDragOver(event: DragEvent) {
    event.preventDefault();
    event.stopPropagation();
    this.fileOver = true;
  }

  @HostListener('dragleave', ['$event']) onDragLeave(event: DragEvent) {
    event.preventDefault();
    event.stopPropagation();
    this.fileOver = false;
  }

  @HostListener('drop', ['$event']) onDrop(event: DragEvent) {
    event.preventDefault();
    event.stopPropagation();
    this.fileOver = false;
    const files = event.dataTransfer?.files;
    if (files?.length ?? 0 > 0) {
      this.filesDropped.emit(files);
    }
  }
}
