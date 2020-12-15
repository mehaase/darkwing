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

import 'package:angular/angular.dart';
import 'package:angular_components/angular_components.dart';
import 'package:angular_components/material_button/material_button.dart';
import 'package:angular_router/angular_router.dart';
import 'package:logging/logging.dart';

import 'package:darkwing/service/server.dart';

final log = Logger('HostDetailView');

@Component(
    selector: 'host-detail',
    templateUrl: 'detail.html',
    styleUrls: const [
      'package:angular_components/css/mdc_web/card/mdc-card.scss.css',
      'detail.css',
    ],
    directives: const [
      coreDirectives,
      MaterialButtonComponent,
      MaterialIconComponent,
    ])
class HostDetailView implements OnActivate {
  Map host;

  ServerService _server;

  /// Constructor.
  HostDetailView(this._server);

  /// Called when entering this route.
  @override
  onActivate(_, RouterState current) {
    this._loadHost(current.parameters['id']);
  }

  /// Load host from the server.
  _loadHost(String hostId) async {
    var result =
        await this._server.sendRequest('get_host', {'host_id': hostId});
    this.host = Map.from(result);
  }
}
