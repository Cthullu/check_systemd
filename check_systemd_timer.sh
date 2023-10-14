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

VERSION="0.1.0"

#
# Function to print tool usage
#

Usage()
{
    echo
    echo "Usage: ${0} [-h|v] [-t <int>] -u <string>.timer" 1>&2
    echo
}

#
# Function to print help message
#

Help()
{
    # Display the help message
    echo "Systemd Timer check script."
    echo
    echo "This script can be used to get the current state of a systemd timer."
    echo "If only the timer name is provided, the script will check if the"
    echo "timer is active."
    echo "If in addition a time-window is provided, the script will check if"
    echo "the timer had run within given window."

    Usage

    echo "Options:"
    echo "-h    Print this help message."
    echo "-t    Timeframe in minutes since the unit should have last run."
    echo "-u    Name of the systemd timer unit to be checked."
    echo "-v    Print the script version."
    echo
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
            Help
            exit 0
            ;;
        t)
            TIMEFRAME=${OPTARG}
            re_isanum='^[0-9]+$'
            if ! [[ ${TIMEFRAME} =~ ${re_isanum} ]]; then
                echo "Error: Timeframe must be a positive integer."
                Usage
                exit 1
            fi
            ;;
        u)
            SYSTEMD_TIMER="${OPTARG}"
            if ! [[ ${SYSTEMD_TIMER} == *.timer ]]; then
                echo "Error: Specified unit must be a timer."
                Usage
                exit 1
            fi
            ;;
        v)  # Print the version
            echo "Version: ${VERSION}"
            exit 0
            ;;
        :)
            echo "Error: -${OPTARG} requires an argument."
            Usage
            exit 1
            ;;
        \?) # Catch invalid options
            echo "Error: Invalid option."
            Usage
            exit 1
            ;;
    esac
done

#
# Check if the systemd timer unit was defined
#

if [[ -z ${SYSTEMD_TIMER} ]]; then
    echo "Error: A unit name must be specified."
    Usage
    exit 1
fi

#
# Check if provided systemd timer exists
#

systemctl list-timers ${SYSTEMD_TIMER} | grep ${SYSTEMD_TIMER} &> /dev/null

if [[ $? -ne 0 ]]; then
    echo "Error: Timer ${SYSTEMD_TIMER} not found at system."
    exit 2
fi

exit 0
