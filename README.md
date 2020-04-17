# DarkWing

DarkWing is your pen test sidekick!

## Overview

TODO

## Installation (Using Docker)

TODO

## Building Docker Images

TODO

## Installation (for local development)

**Note this requires Docker on Linux. It does not work on Docker for MacOS. (Not sure
about Docker for Windows.)**

The desired development environment looks like this:

```
+-----------+    +--------------+        +-----------------------+
|  browser  |--->| nginx 80/443 |---+--->|  JSON-RPC server 8080 |
+-----------+    +--------------+   |    +-----------------------+
                                    |
                                    |    +-----------------------+
                                    +--->|    dart client 8081   |
                                         +-----------------------+
```

It is similar to the production environment with the addition of an extra server that
provides dart client-side code. This server listens on 8081 and it automatically
rebuilds the client-side code whenever it changes, allowing for faster dev and debug
cycles.

### One-time Setup

With Python (≥3.7), install [Poetry](https://python-poetry.org/docs/) and use it to
install Python dependencies and set up a virtual environment.

```
darkwing $ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3.7
darkwing $ poetry install
```

Generate a self-signed certificate:

```
darkwing $ cd docker/dev
darkwing/docker/dev $ poetry run python gencert.py
```

Install the [Dart SDK](https://dart.dev/get-dart) (currently tested on 2.7.2) and use it
to install the Dart dependencies:

```
darkwing $ cd client
darkwing/client $ pub get
darkwing/client $ pub global activate webdev
```

### Starting Dev Environment

To run the dev environment, first start the docker containers:

```
darkwing $ cd docker/dev
darkwing/docker/dev $ docker-compose up
```

This command starts the nginx container inside docker. Next, you should run the two
other components directly on your host. In a new terminal, start the websocket server.

```
darkwing $ poetry run python -m darkwing --reload
```

The `--reload` flag means the server will restart automatically when the source code is
changed. You might also want to use `--log-level debug` for more verbose logging.

In another new terminal, start the client:

```
darkwing $ cd client
darkwing/client $ webdev serve web:8081 --auto=refresh
```

The client always runs in reload mode, so any change to the source code will trigger
a rebuild. If you use Chrome, then the application will automatically reload so you can
see changes without hitting the reload button.

Finally, open the browser and connect to [https://localhost](https://localhost).

