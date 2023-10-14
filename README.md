# Check Systemd Timer

![ShellShock Workflow](https://github.com/cthullu/systemd_timer_check/actions/workflows/shellcheck.yml/badge.svg?branch=main)

A simple bash script which uses systemd capabilities to check if a given systemd
timer is active and has been executed in a given timeframe.

This script was created as varios other scripts to check system services I found
require additional software such as Python3.

The script expects a timer to provided via the `-u` parameter. If no timeframe
(`-t`) is specified, the script will check if the timer is activaed. If a
timeframe was provided, the script will also check if the service runs within
the given number of minutes (+- from now).

## Script Options

~~~SHELL
-h    Print this help message.
-t    Timeframe in minutes within the unit should run.
-u    Name of the systemd timer unit to be checked.
-v    Print the script version.
~~~

## License

MIT

## Author Information

| Date        | Version | Author      |
|-------------|---------|-------------|
| 2023-10-14  | 0.1.0   | Daniel Kuß  |
