import 'package:angular/angular.dart';
import 'package:angular_router/angular_router.dart';

import 'package:darkwing/component/hosts/list.template.dart'
    as host_list_template;
import 'package:darkwing/component/none.template.dart' as none_template;

class RouteAuthorization {
  bool requiresLogin;

  RouteAuthorization(this.requiresLogin);
}

class Routes {
  static final hostList = RouteDefinition(
      path: 'host', // temporarily an alias to terms view
      component: host_list_template.HostListViewNgFactory,
      additionalData: RouteAuthorization(true));
  static final none = RouteDefinition(
      path: 'none',
      component: none_template.NoneViewNgFactory,
      additionalData: RouteAuthorization(false));
  static final root = RouteDefinition.redirect(path: '', redirectTo: 'host');

  static final all = <RouteDefinition>[
    hostList,
    none,
  ];
}

/// This custom router hook enforces authentication.
///
/// Note that because Router depends on RouterHook we can not have the DI inject a
/// router into this instance, or even inject anything that depends on router, such as
/// AuthenticationService. Instead, we inject the AuthenticationService lazily when it
/// is first accessed.
@Injectable()
class RouterAuthenticationHook extends RouterHook {
  // AuthenticationService _auth;
  // // This somewhat confusing hack is a work-around the fact that router hooks cannot
  // // redirect routes, and router hooks also cannot inject a router (either directly or
  // // through AuthenticationService) to perform redirects.
  // AuthenticationService get auth =>
  //     _auth ??= _injector.provideType(AuthenticationService);
  // Injector _injector;

  // RouterAuthenticationHook(this._injector);

  // @override
  // Future<bool> canActivate(
  //     Object componentInstance, RouterState oldState, RouterState newState) {
  //   if (newState.routes.length > 1) {
  //     // Why does the state contain a list of routes? I assume for now that it always
  //     // contains 1 item.
  //     throw Exception('Unexpected router state contains multiple routes');
  //   }
  //   var ra = newState.routes[0].additionalData as RouteAuthorization;
  //   if (ra.requiresLogin) {
  //     var r = this.auth.checkLogin();
  //     return r;
  //   } else {
  //     return Future.value(true);
  //   }
  // }
}
