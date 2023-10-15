# Check Systemd

![Service Workflow](https://github.com/cthullu/systemd_timer_check/actions/workflows/systemd_service.yml/badge.svg?branch=main) ![Timer Workflow](https://github.com/cthullu/systemd_timer_check/actions/workflows/systemd_timer.yml/badge.svg?branch=main)

A toolsuite to check systemd services and timer written in bash.

This scripts were created as varios other scripts to check system services I
found require additional software such as Python3.

The repository currently holds 2 check sripts:

* check_systemd_service.sh
* check_systemd_timer.sh

## check_systemd_service.sh

Script to check if a specified service

* exists
* is-active
* is-enabled

### Options

~~~SHELL
-h    Print this help message.
-u    Name of the systemd service unit to be checked.
-v    Print the script version.
~~~

### Service Check Retun Codes

* RC0 if the specified service runs and is enabled
* RC0 if help is printed
* RC0 if version is printed
* RC1 if the specified service runs but is not enables
* RC2 if the specified service was not found
* RC2 if the specified service does not run
* RC3 if no service was defined
* RC3 if an invalid option was defined

## check_systemd_timer.sh

A simple bash script which uses systemd capabilities to check if a given systemd
timer is active and has been executed in a given timeframe.

The script expects a timer to provided via the `-u` parameter. If no timeframe
(`-t`) is specified, the script will check if the timer is activaed. If a
timeframe was provided, the script will also check if the service runs within
the given number of minutes (+- from now).

Script to check if a specified service

* exists
* is-enabled
* runs within defined timeframe

## Script Options

~~~SHELL
-h    Print this help message.
-t    Timeframe in minutes within the unit should run.
-u    Name of the systemd timer unit to be checked.
-v    Print the script version.
~~~

### Timer Check Retun Codes

* RC0 if help is printed
* RC0 if version is printed
* RC0 if the specified timer is active and did run within the defined timeframe
* RC1 if the specified timer did not run within defined timeframe
* RC2 if the specified timer was not found
* RC2 if the specified timer was not found
* RC3 if an invalid timeframe was defined
* RC3 if no timer was specified
* RC3 if an invalid option was defined

## License

MIT

## Author Information

| Date        | Version | Author      |
|-------------|---------|-------------|
| 2023-10-14  | 0.1.0   | Daniel Kuß  |
| 2023-10-15  | 1.0.0   | Daniel Kuß  |
