# Check Systemd

[![Check Service Script](https://github.com/Cthullu/check_systemd/actions/workflows/systemd_service.yml/badge.svg?branch=main)](https://github.com/Cthullu/check_systemd/actions/workflows/systemd_service.yml)
[![Check Timer Script](https://github.com/Cthullu/check_systemd/actions/workflows/systemd_timer.yml/badge.svg?branch=main)](https://github.com/Cthullu/check_systemd/actions/workflows/systemd_timer.yml)
[![Perform Python Linter run](https://github.com/Cthullu/check_systemd/actions/workflows/python_lint.yml/badge.svg?branch=main)](https://github.com/Cthullu/check_systemd/actions/workflows/python_lint.yml)

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

[1]: bash/README.md
[2]: python/README.md
