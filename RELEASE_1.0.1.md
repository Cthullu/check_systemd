# Release 1.0.1

After reading some more regarding the expected [return codes by Icinga2][1], I
decided to adapt the RC values for my scripts to match.

By default Icinga2 expects the following return codes in respect to the host
state:

| Value | Host State  | Service State |
|-------|-------------|---------------|
| 0     | Up          | OK            |
| 1     | Up          | Warning       |
| 2     | Down        | Critical      |
| 3     | Down        | Unknown       |

## check_systemd_service

Old:

* The script returns RC 0 if the specified service is active and enabled.
* If the service is not enabled or active, RC 1 is returned.
* If the service is not known at the system, RC 2 is returned.

New:

* RC0 if the specified service runs and is enabled
* RC0 if help is printed
* RC0 if version is printed
* RC1 if the specified service runs but is not enables
* RC2 if the specified service was not found
* RC2 if the specified service does not run
* RC3 if no service was defined
* RC3 if an invalid option was defined

## check_systemd_timer

Old:

* The script returns RC 0 if the specified timer is active and runs within the
  specified timeframe.
* If the timer is not active or does not run within the timeframe, RC 1 is
  returned.
* If the timer is not known at the system, RC 2 is returned.

New:

* RC0 if help is printed
* RC0 if version is printed
* RC0 if the specified timer is active and did run within the defined timeframe
* RC1 if the specified timer did not run within defined timeframe
* RC2 if the specified timer was not found
* RC2 if the specified timer was not found
* RC3 if an invalid timeframe was defined
* RC3 if no timer was specified
* RC3 if an invalid option was defined

[1]: https://icinga.com/docs/icinga-2/latest/doc/03-monitoring-basics/#check-result-state-mapping
