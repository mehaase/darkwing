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

import 'package:angular/angular.dart';
import 'package:angular_router/angular_router.dart';

import 'package:darkwing/component/host/detail.template.dart'
    as host_detail_template;
import 'package:darkwing/component/host/list.template.dart'
    as host_list_template;
import 'package:darkwing/component/none.template.dart' as none_template;
import 'package:darkwing/component/scan/detail.template.dart'
    as scan_detail_template;
import 'package:darkwing/component/scan/list.template.dart'
    as scan_list_template;

class RouteAuthorization {
  bool login;

  RouteAuthorization({this.login});
}

class Routes {
  static final hostDetail = RouteDefinition(
      path: 'host/:id',
      component: host_detail_template.HostDetailViewNgFactory,
      additionalData: RouteAuthorization(login: true));
  static final hostList = RouteDefinition(
      path: 'host',
      component: host_list_template.HostListViewNgFactory,
      additionalData: RouteAuthorization(login: true));
  static final none = RouteDefinition(
      path: 'none',
      component: none_template.NoneViewNgFactory,
      additionalData: RouteAuthorization(login: false));
  static final root = RouteDefinition.redirect(path: '', redirectTo: 'host');
  static final scanDetail = RouteDefinition(
      path: 'scan/:id',
      component: scan_detail_template.ScanDetailViewNgFactory,
      additionalData: RouteAuthorization(login: true));
  static final scanList = RouteDefinition(
      path: 'scan',
      component: scan_list_template.ScanListViewNgFactory,
      additionalData: RouteAuthorization(login: true));

  static final all = <RouteDefinition>[
    hostDetail,
    hostList,
    none,
    scanDetail,
    scanList,
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
