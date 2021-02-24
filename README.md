# Darkwing: Let's get IP-rangerous!

## Overview

Darkwing is your pen test sidekick.

## Installation

*todo: generate docker images and describe installation here*

## Dev Environment

### Dev Dependencies

To set up a development environment, you need the following dependencies:

    * [Docker & Docker Compose](https://docs.docker.com/desktop/)
    * [Node & NPM](https://nodejs.org/en/download/)
    * [Angular & Angular CLI ](https://angular.io/guide/setup-local)
    * [Python 3.9](https://www.python.org/downloads/)
    * [Python Poetry](https://python-poetry.org)

### Dev Setup

The desired development environment looks like this:

```
+-----------+    +-------------------+
|  browser  |--->| ng serve tcp/4200 |
+-----------+    +-------------------+
                           |
                           V
                 +-------------------+
                 | darkwing tcp/8080 |
                 +-------------------+
                           |
                           V
             +----------------------------+
             | mongodb (Docker) tcp/27017 |
             +----------------------------+
```

The Angular CLI runs the dev server on localhost:4200, which connects to the Darkwing
server on localhost:8080. The Darkwing server connects to MongoDB running inside of a
Docker container. To get this running, you should have 4 terminals open:

1. Run the Angular client in the first terminal.
2. Run the Darkwing server in the second terminal.
3. Run MongoDB inside a Docker container in the third terminal.
4. Use the 4th terminal for ad hoc work.

<table border="2">
    <tr>
        <td width="50%">
            <code>
            $ cd darkwing_root/web<br>
            $ ng serve<br>
            </code>
        </td>
        <td width="50%">
            <code>
            $ cd darkwing_root<br>
            $ poetry shell<br>
            $ source .darkwing.env # see below<br>
            $ python -m darkwing --log-level debug --reload<br>
            </code>
        </td>
    </tr>
    <tr>
        <td width="50%">
            <code>
            $ cd darkwing_root/docker/dev<br>
            $ docker-compose up<br>
            </code>
        </td>
        <td width="50%">
            <code>
            $ # this terminal is for ad hoc work<br>
            </code>
        </td>
    </tr>
</table>

The server's `--reload` flag will tell it restart automatically when the source code is
changed. And `--log-level debug` adds more detailed log output.

The client always runs in reload mode, so any change to the source code will trigger
a rebuild.

Finally, open the browser and connect to [http://localhost:4200](http://localhost:4200).

## Environment Variables

The application maintains most of its configuration in the database, but for aspects of
configuration that cannot be stored in the database (e.g. database connection
information), those are passed through the environment. Environment variables are a
convenient way to configure the application when it is running inside a container.

The following environment variables are used.

<dl>
     <dt>DARKWING_MONGO_HOST</dt>
     <dd>The hostname for the MongoDB server.</dd>
</dl>

To pass environment variables in at runtime, you have a few options.

1. Put the environment variables in a file, e.g. `.darkwing.env`, and `source` it prior
   to running the server.
2. Set the environment on the command line, i.e.
   `env DARKWING_MONGO_HOST=localhost python -m darkwing...`
3. For production deployments, add variables to the `docker-compose.yml`.

## Building Docker Images

*todo: put instructions for building and publishing Docker images*
