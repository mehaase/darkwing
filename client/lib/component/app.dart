// Darkwing: Let's get IP-rangerous!
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

import 'dart:html';

import 'package:angular/angular.dart';
import 'package:angular_components/angular_components.dart';
import 'package:angular_router/angular_router.dart';
import 'package:logging/logging.dart';

import 'package:darkwing/component/routes.dart';
import 'package:darkwing/service/server.dart';

Map<String, Level> LOG_LEVELS = const {
  'all': Level.ALL,
  'finest': Level.FINEST,
  'finer': Level.FINER,
  'fine': Level.FINE,
  'config': Level.CONFIG,
  'info': Level.INFO,
  'warning': Level.WARNING,
  'severe': Level.SEVERE,
  'shout': Level.SHOUT,
  'off': Level.OFF,
};

@Component(selector: 'app', templateUrl: 'app.html', styleUrls: const [
  'package:angular_components/app_layout/layout.scss.css',
  'app.css'
], directives: const [
  coreDirectives,
  MaterialButtonComponent,
  MaterialIconComponent,
  MaterialListComponent,
  MaterialListItemComponent,
  MaterialPersistentDrawerDirective,
  routerDirectives
], providers: const [
  // AuthenticationService,
  routerProviders,
  //ClassProvider(RouterHook, useClass: RouterAuthenticationHook),
  materialProviders,
  ServerService
], exports: [
  Routes
])
class AppComponent {
  /// Authentication service.
  // AuthenticationService auth;

  /// JSON-RPC service.
  ServerService server;

  /// Constructor.
  AppComponent(
    this.server,
  ) {
    var logLevel = window.localStorage['log-level'];
    Logger.root.level = LOG_LEVELS[logLevel] ?? Level.SEVERE;

    Logger.root.onRecord.listen((LogRecord r) {
      var msg = '[${r.level.name}] ${r.loggerName}: ${r.message}';
      if (r.object != null) {
        msg += ' (Object: ${r.object.toString()})';
      }
      window.console.log(msg);
    });

    this.server.stayConnected();
  }
}
