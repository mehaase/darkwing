import 'dart:html';

import 'package:angular/angular.dart';
import 'package:angular_components/angular_components.dart';
import 'package:angular_router/angular_router.dart';
import 'package:logging/logging.dart';

import 'package:darkwing/component/routes.dart';
import 'package:darkwing/service/server.dart';

@Component(selector: 'app', templateUrl: 'app.html', styleUrls: const [
  'package:angular_components/app_layout/layout.scss.css',
  // 'app.scss.css'
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
    if (window.localStorage['debug-log'] == 'true') {
      Logger.root.level = Level.ALL;
    } else {
      Logger.root.level = Level.SEVERE;
    }

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
