import 'dart:async';
import 'dart:convert';
import 'dart:html';

import 'package:angular/angular.dart';
import 'package:logging/logging.dart';

/// A ServerException is thrown if a server-side error occurs while processing
/// a request.
class ServerException implements Exception {
  int code;
  String message;

  ServerException(Map jsonError) {
    this.code = jsonError['code'];
    this.message = jsonError['message'];
  }
  String toString() {
    return 'ServerException (${code}): ${message}';
  }
}

/// This class handles interaction with the server, abstracting out details like
/// command IDs and pairing responses to requests.
@Injectable()
class ServerService {
  /// Sends true when connected to server and false when disconnected.
  Stream<bool> connected;
  bool isConnected = false;

  int _nextCommandId;
  Map<int, Completer> _pendingRequests;
  Future<WebSocket> _socketFuture;
  StreamController<bool> _connectedController;

  final Logger log = new Logger('ServerService');

  /// Constructor.
  ServerService() {
    this._clearState();
    this._connectedController = new StreamController<bool>.broadcast();
    this.connected = this._connectedController.stream;
  }

  /// Send a request to the server and return a future response.
  Future<dynamic> sendRequest(String method, [Map params]) async {
    var socket = await this._getSocket();
    var completer = new Completer<dynamic>();
    var commandId = this._nextCommandId++;
    var request = {
      'id': commandId,
      'method': method,
      'jsonrpc': '2.0',
    };
    if (params != null) {
      request['params'] = params;
    }
    this._pendingRequests[commandId] = completer;
    var requestData = utf8.encode(jsonEncode(request));
    socket.send(requestData); // There's no async API for Websocket!
    return completer.future;
  }

  /// Tell the server to connect immediately and automatically re-connect
  /// if the connection drops.
  stayConnected() async {
    this.connected.listen((isConnected) async {
      if (!isConnected) {
        log.info('Will try to reconnect in 2 seconds.');
        await new Future.delayed(new Duration(seconds: 2));
        this._socketFuture == null;
        await this._getSocket();
      }
    });

    await this._getSocket();
  }

  /// Clear out all state related to a connection.
  ///
  /// This is useful for resetting after closing a connection as well as for
  /// initialization of this object.
  void _clearState() {
    this._nextCommandId = 0;
    this._pendingRequests = {};
    this._socketFuture = null;
  }

  /// Return a websocket wrapped in a future. If not already connected, this
  /// method will connect to the websocket before completing the future.
  Future<WebSocket> _getSocket() {
    print('get socket');
    if (this._socketFuture == null) {
      var completer = new Completer<WebSocket>();
      var currentUri = Uri.parse(window.location.href);
      var socketUri = new Uri(
        scheme: 'wss',
        userInfo: currentUri.userInfo,
        host: currentUri.host,
        port: currentUri.port,
        path: '/ws/',
      );
      print('new websocket');
      var socket = new WebSocket(socketUri.toString());
      socket.binaryType = 'arraybuffer';
      this._socketFuture = completer.future;

      var connTimeout = new Future.delayed(new Duration(seconds: 5), () {
        if (!this.isConnected) {
          ('conn timeout; closing');
          socket.close();
        }
      });

      socket.onClose.listen((event) {
        print('conn closed');
        log.info('Socket disconnected.');
        this._clearState();
        this._connectedController.add(false);
        this.isConnected = false;
      });

      socket.onError.listen((event) {
        print('conn error');
        var err = 'Server error!';
        log.severe(err, event);
        completer.completeError(err);
        this._socketFuture = null;
      });

      socket.onMessage.listen(this._handleServerMessage);

      socket.onOpen.listen((event) {
        print('conn open');
        log.info('Socket connected.');
        completer.complete(socket);
        this._connectedController.add(true);
        this.isConnected = true;
      });
    }

    return this._socketFuture;
  }

  /// Handles an incoming message from the websocket.
  ///
  /// This either completes a command future with a response, or it sends
  /// a message to a subscription stream.
  void _handleServerMessage(MessageEvent event) {
    var message = jsonDecode(utf8.decode(event.data.asInt8List()));

    if (message.containsKey('id')) {
      this._handleServerResponse(message);
    } else {
      throw new Exception('Unexpected message type: ' + message.toString());
    }
  }

  /// Handle a Response message.
  ///
  /// This returns response data or a subscription stream back to the caller
  /// who sent the request.
  void _handleServerResponse(Map response) {
    var commandId = response['id'];
    var completer = this._pendingRequests.remove(commandId);

    if (response.containsKey('result')) {
      completer.complete(response['result']);
    } else if (response.containsKey('error')) {
      completer.completeError(new ServerException(response['error']));
    } else {
      this.log.severe('Invalid server response: ' + response.toString());
    }
  }
}
