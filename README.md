Shinken to Alerta
=================

Forward Shinken events to Alerta for a consolidated view and improved visualisation.

Transform this ...

![nagios](/docs/images/shinken-hosts-groups-overview.png?raw=true)

Into this ...

![alerta](/docs/images/shinken-alerta.png?raw=true)

Installation
------------

To install Shinken follow the official online documentation.

Then use the `shinken` CLI to install the published module:

    $ shinken install alerta

Configuration
-------------

Add `alerta` to the list of broker modules to use
in `/etc/shinken/brokers/broker-master.cfg`:

```
define broker {
    broker_name     broker-master
    address         localhost
    port            7772
    spare           0

    ## Optional
    manage_arbiters     1   ; Take data from Arbiter. There should be only one
                            ; broker for the arbiter.
    manage_sub_realms   1   ; Does it take jobs from schedulers of sub-Realms?
    timeout             3   ; Ping timeout
    data_timeout        120 ; Data send timeout
    max_check_attempts  3   ; If ping fails N or more, then the node is dead
    check_interval      60  ; Ping node every N seconds

    ## Modules
    # Default: None
    # Interesting modules that can be used:
    # - simple-log              = just all logs into one file
    # - livestatus              = livestatus listener
    # - tondodb-mysql           = NDO DB support (deprecated)
    # - npcdmod                 = Use the PNP addon
    # - graphite                = Use a Graphite time series DB for perfdata
    # - webui                   = Shinken Web interface
    # - glpidb                  = Save data in GLPI MySQL database
    # Comma separated list of modules
    modules	webui2,alerta

    # Enable https or not
    use_ssl	          0
    # enable certificate/hostname check, will avoid man in the middle attacks
    hard_ssl_name_check   0

    ## Advanced
    realm   All
}
```

Modify the defaults by updating `/etc/shinken/modules/alerta.cfg`:

```
define module {
    module_name     alerta
    module_type     http
    endpoint        http://localhost:8080
    environment     Production
    debug           0
}
```

Testing
-------

TBC

Troubleshooting
---------------

TBC

References
----------

* [Server Monitoring with Shinken on Ubuntu 16.04](https://www.howtoforge.com/tutorial/server-monitoring-with-shinken-on-ubuntu-16-04/)
* [Shinken Broker modules](https://shinken.readthedocs.io/en/1.4.2/89_packages/the_broker_modules.html#the-broker-modules)

License
-------

Copyright (c) 2018 Nick Satterly. Available under the MIT License.
