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

import { SortDirection } from '@angular/material/sort';

/**
 * Represents a requested page from a result set.
 */
export class PageRequest {
    /**
     * Constructor
     * @param pageNumber The 1-based page index to request.
     * @param itemsPerPage The max number of items per page.
     * @param sortColumn The column name to sort by.
     * @param sortDirection The sort direction.
     */
    constructor(
        private pageNumber: number,
        private itemsPerPage: number,
        private sortColumn: string,
        private sortDirection: SortDirection) {

    }

    /**
     * Return an object that can be sent to the server.
     */
    public toJson(): Record<string, any> {
        return {
            'page_number': this.pageNumber,
            'items_per_page': this.itemsPerPage,
            'sort_column': this.sortColumn,
            'sort_ascending': this.sortDirection == 'asc',
        };
    }
}

export class Jsonable {
    public static fromJson(): Record<string, any> {
        throw new Error('Subclasses of Jsonable must override toJson().');
    }
}

/**
 * Represents a page of results.
 *
 * I wanted to put a static method fromJson() on this class and have it call T's
 * fromJson() method but couldn't figure out how to make it work.
 */
export class PageResult<T extends Jsonable> {
    /**
     * Private constructor -- use static method instead.
     * @param totalCount
     * @param items
     */
    public constructor(public totalCount: number, public items: Array<T>) {
    }
}
