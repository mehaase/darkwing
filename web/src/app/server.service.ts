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
import { LogService } from './log.service';

type JsonRpcCommand = Record<string, any>;
type JsonRpcArgs = Record<string, any> | Array<string | number> | undefined;
type JsonRpcResult = Record<string, any>;

@Injectable({
  providedIn: 'root'
})
export class ServerService {
  private ws?: WebSocket;
  private nextCommandId: number = 0;
  private pendingRequests: any = {};

  constructor(private log: LogService) { }

  /**
   * Connect to the WebSocket server.
   *
   * @param url WebSocket URL
   */
  public async connect(url: string): Promise<void> {
    this.log.info('Connecting to ' + url);

    return new Promise((resolve, reject) => {
      this.ws = new WebSocket(url);
      this.ws.onopen = (_: Event) => {
        this.ws!.onerror = this.handleWebSocketError;
        this.log.info('Connected.')
        resolve();
      };
      this.ws.onerror = function (event: Event) {
        reject(event);
      };
    });
  }

  /**
   * Invoke a JSON-RPC method on the server.
   *
   * @param method The name of a JSON RPC method to invoke.
   * @param params
   */
  public async invoke(method: string, params?: JsonRpcArgs) {
    if (this.ws === undefined) {
      throw new Error("WebSocket is not connected.");
    }

    let invocation: JsonRpcCommand = {
      'id': this.nextCommandId++,
      'method': method,
      'jsonrpc': '2.0',
    }

    if (params != undefined) {
      invocation['params'] = params;
    }

    let request = JSON.stringify(invocation);
    let encoder = new TextEncoder();
    this.ws.send(encoder.encode(request));

    return new Promise<JsonRpcResult>((resolve, reject) => {
      this.pendingRequests[invocation['id']] = (result: JsonRpcResult) => {
        resolve(result);
      };
    });
  }

  private handleWebSocketError(event: Event) {
    this.log.info('error on websocket: ' + event);
  }
}
