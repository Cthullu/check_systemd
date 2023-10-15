#!/usr/bin/env bash

 set -o pipefail

#
# This is a lightweight bash script to be used with Nagios/Icinga using only
# bash functionality to keep dependencies at a minimum.
#

#
# Author: Daniel Kuß
# License: MIT
# Source: https://github.com/Cthullu/systemd_timer_check
#

VERSION="0.1.1"

#
# History:
# * 2023-10-14: Version 0.1.0
#

#
# Function to print tool usage
#

usage() {
    echo
    echo "Usage: ${0} [-h|v] [-t <int>] -u <string>.timer" 1>&2
    echo
}

#
# Function to print help message
#

help() {
    # Display the help message
    echo "Systemd Timer check script."
    echo
    echo "This script can be used to get the current state of a systemd timer."
    echo "If only the timer name is provided, the script will check if the"
    echo "timer is active."
    echo "If in addition a time-window is provided, the script will check if"
    echo "the timer had run within given window."

    usage

    echo "Options:"
    echo "-h    Print this help message."
    echo "-t    Timeframe in minutes within the unit should run."
    echo "-u    Name of the systemd timer unit to be checked."
    echo "-v    Print the script version."
    echo
}

#
# Little helpers
#

timer_exists() {
    local TIMER="${1}"

    if systemctl list-timers "${TIMER}" | grep "${TIMER}"; then
        return 0
    else
        return 1
    fi

}

timer_active() {
    local TIMER="${1}"

  if systemctl is-active "${TIMER}"; then
    return 0
  else
    return 1
  fi

}

#
# Main program body
#


#
# Get the command line opts
#

while getopts ":ht:u:v" option; do
    case ${option} in
        h)  # Print the help message
            help
            exit 0
            ;;

        t)  # Save the provided timeframe
            TIMEFRAME=${OPTARG}
            re_isanum='^[0-9]+$'

            if ! [[ ${TIMEFRAME} =~ ${re_isanum} ]]; then

                echo "Error: Timeframe must be a positive integer."
                usage
                exit 3

            fi

            ;;

        u)  # Save the provided timer name
            SYSTEMD_TIMER="${OPTARG}"

            if ! [[ ${SYSTEMD_TIMER} == *.timer ]]; then

                echo "Error: Specified unit must be a timer."
                usage
                exit 3

            fi

            ;;

        v)  # Print the version
            echo "${VERSION}"
            exit 0
            ;;

        :)
            echo "Error: -${OPTARG} requires an argument."
            usage
            exit 3
            ;;

        \?) # Catch invalid options
            echo "Error: Invalid option."
            usage
            exit 3
            ;;

        *)  # We should never get here, so simply exit
            return 3
            ;;
    esac
done

#
# Check if the systemd timer unit was defined
#

if [[ -z ${SYSTEMD_TIMER} ]]; then

    echo "Error: A unit name must be specified."
    usage
    exit 3

fi

#
# Check if provided systemd timer exists
#

if ! timer_exists "${SYSTEMD_TIMER}" &> /dev/null; then

    echo "Critical: Timer ${SYSTEMD_TIMER} not found at system."
    exit 2

fi

#
# Check if systemd timer is active
#

if ! timer_active "${SYSTEMD_TIMER}" &> /dev/null; then

    echo "Critical: Timer is not active."
    exit 2

fi

#
# If a timestamp was specified, we need to compare it with the provided
# timeframe value
#

if [[ -n ${TIMEFRAME} ]]; then

    LAST_EXECUTION=$(systemctl show "${SYSTEMD_TIMER}" --property LastTriggerUSec --value)
    LAST_EXECUTION_SEC=$(date --date "${LAST_EXECUTION}" +'%s')

    NEXT_EXECUTION=$(systemctl show "${SYSTEMD_TIMER}" --property NextElapseUSecRealtime --value)
    NEXT_EXECUTION_SEC=$(date --date "${NEXT_EXECUTION}" +'%s')

    MAX_LAST_EXECUTION_SEC=$(date --date "${TIMEFRAME} minutes ago" +'%s')
    MAX_NEXT_EXECUTION_SEC=$(date --date "${TIMEFRAME} minutes" +'%s')

    #
    # Compare our timestamps
    #

    if [[ ${LAST_EXECUTION_SEC} -lt ${MAX_LAST_EXECUTION_SEC} ]] && [[ ${NEXT_EXECUTION_SEC} -gt ${MAX_NEXT_EXECUTION_SEC} ]]; then

        echo "Warning: ${SYSTEMD_TIMER} will not run in specified timeframe "
        exit 1

    fi

fi

#
# If we end here, everything is fine
#

echo "Checked ${SYSTEMD_TIMER} -- OK"
exit 0
