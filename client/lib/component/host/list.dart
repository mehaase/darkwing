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
import 'package:angular_components/angular_components.dart';
import 'package:angular_router/angular_router.dart';
import 'package:logging/logging.dart';

import 'package:darkwing/service/server.dart';

final log = Logger('HostListView');

@Component(selector: 'host-list', templateUrl: 'list.html', styleUrls: const [
  'list.css'
], directives: const [
  coreDirectives,
  // MaterialButtonComponent,
  // MaterialProgressComponent,
])
class HostListView implements OnActivate {
  List<Map> hosts;

  Router _router;
  ServerService _server;

  /// Constructor.
  HostListView(this._router, this._server);

  /// Go to scan detail page.
  gotoHostDetail(String hostId) async {
    await this._router.navigate('/host/${hostId}');
  }

  /// Called when entering this route.
  @override
  onActivate(_, RouterState current) {
    this._loadHosts();
  }

  /// Load hosts from the server.
  _loadHosts() async {
    var result = await this._server.sendRequest('list_hosts');
    this.hosts = List<Map>.from(result['hosts']);
  }
}
