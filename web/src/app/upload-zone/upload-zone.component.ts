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

/**
 * This component allows the user to select files either by dropping them onto the
 * component or using a file picker dialog.
 */
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

    constructor() { }

    /**
     * Handle the file picker choosing files.
     *
     * @param event The file picker event
     */
    public filesPicked(event: Event) {
        console.log(event);
        if (this.filePicker) {
            this.filesDropped.emit(this.filePicker.nativeElement.files);
            //TODO clear existing files;
        } else {
            console.warn('FilePicker not initialized.');
        }
    }

    /**
     * Handle the file picker's selection of files.
     */
    public selectFiles() {
        if (this.filePicker) {
            this.filePicker.nativeElement.click();
        } else {
            console.warn('FilePicker not initialized.');
        }
    }

    /**
     * Handle a dragover event by updating component appearance.
     *
     * @param event The dragover event
     */
    @HostListener('dragover', ['$event']) onDragOver(event: DragEvent) {
        event.preventDefault();
        event.stopPropagation();
        this.fileOver = true;
    }

    /**
     * Handle a dragleave event by updating component appearance.
     *
     * @param event The dragleave event
     */
    @HostListener('dragleave', ['$event']) onDragLeave(event: DragEvent) {
        event.preventDefault();
        event.stopPropagation();
        this.fileOver = false;
    }

    /**
     * Handle a drop event by emitting the files.
     *
     * @param event The dragleave event
     */
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
