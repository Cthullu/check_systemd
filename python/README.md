# check_systemd.py

Python version of the check systemd tools.

It consists of one main programm and two subcommands to either check a systemd
service or timer.

The python version also comes with a debug switch to test and check services and
timers manually:

~~~bash
usage: check_systemd [-h] [-d] [-v] {service,timer} ...

Checksystemd service and timer units.

options:
  -h, --help       show this help message and exit
  -d, --debug      turn on debug logging
  -v, --version    show program's version number and exit

subcommands:
  valid subcommands

  {service,timer}  additional help
    service        systemd service related checks
    timer          systemd timer related checks
~~~

## Subcommand "service"

The `service` subcommand is the equivalent of the `check_systemd_service.sh`
script.

~~~bash
usage: check_systemd service [-h] -s <service>

options:
  -h, --help            show this help message and exit
  -s <service>, --service <service>
                        the name of the systemd service to check
~~~

It provides the following return codes:

* `0`: if the specified service runs and is enabled
* `1`: if the specified service runs but is not enables
* `2`: if the specified service was not found
* `2`: if the specified service does not run

## Subcommand "timer"

The `timer`? subcommand is the equivalent of the `check_systemd_timer.sh`
script.

~~~bash
usage: check_systemd timer [-h] -t <timer> [-w <window>]

options:
  -h, --help            show this help message and exit
  -t <timer>, --timer <timer>
                        the name of the systemd timer to check
  -w <window>, --window <window>
                        the time window in minutes in which the timer should have run
~~~

It provides the following return codes:

* `0`: if the specified timer is active (and ran within defined timeframe)
* `1`: if the specified timer is not active
* `1`: if the specified timer did not run within defined timeframe
* `2`: if the specified timer was not found
