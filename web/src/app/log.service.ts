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

/**
 * A very simplistic logging service. To be improved later.
 */
@Injectable({
  providedIn: 'root'
})
export class LogService {
  error(msg: any) {
    this.log('ERROR', msg);
  }

  warn(msg: any) {
    this.log('WARN ', msg);
  }

  info(msg: any) {
    this.log('INFO ', msg);
  }

  debug(msg: any) {
    this.log('DEBUG', msg);
  }

  private log(level: string, msg: string) {
    console.log(this.timestamp() + ' [' + level + '] ' + msg);
  }

  private timestamp(): string {
    let now = new Date();
    return this.pad(now.getHours(), 2) + ':' +
      this.pad(now.getMinutes(), 2) + ':' +
      this.pad(now.getSeconds(), 2) + '.' +
      this.pad(now.getMilliseconds(), 3);
  }

  private pad(num: number, length: number): string {
    let s = num + '';
    while (s.length < length) {
      s = '0' + s;
    }
    return s;
  }
}
