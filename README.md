# Check Systemd

![Service Workflow](https://github.com/cthullu/systemd_timer_check/actions/workflows/systemd_service.yml/badge.svg?branch=main)
![Timer Workflow](https://github.com/cthullu/systemd_timer_check/actions/workflows/systemd_timer.yml/badge.svg?branch=main)

A toolsuite to check systemd services and timer.

The goal of this scripts are to provide simple check scripts to be used with
nagios or Icinga2 to check the status of a systemd unit which is either a
service or a timer.

Currently, the check scripts exists in two versions:

* 2 bash scripts to check either service or timer
* 1 python script to check both, service and timer

[Bash version README][1]

[Python version README][2]

## License

MIT

## Author

Daniel Kuß

[1]: bash/readme.md
[2]: python/readme.md
