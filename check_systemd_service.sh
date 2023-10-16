#!/usr/bin/env bash

 set -o pipefail

#
# This is a lightweight bash script to be used with Nagios/Icinga using only
# bash functionality to keep dependencies at a minimum.
#

#
# Author: Daniel Kuß
# License: MIT
# Source: https://github.com/Cthullu/check_systemd
#

VERSION="1.0.1"

#
# History:
# * 2023-10-15: Version 0.1.0
# * 2023-10-15: Version 1.0.0
# * 2023-10-15: Version 1.0.1
#

#
# Function to print tool usage
#

usage() {
    echo
    echo "Usage: ${0} [-h|v] -u <string>.service" 1>&2
    echo
}

#
# Function to print help message
#

help() {
    # Display the help message
    echo "Systemd Service check script."
    echo
    echo "This script checks if a provided systemd service is running and"
    echo "enabled."

    usage

    echo "Options:"
    echo "-h    Print this help message."
    echo "-u    Name of the systemd service unit to be checked."
    echo "-v    Print the script version."
    echo
}

#
# Little helpers
#

service_exists() {
  local SERVICE="${1}"

  if [[ -n $(systemctl list-units --all --type service --full --no-legend "${SERVICE}" || true) ]]; then
    return 0
  else
    return 1
  fi

}

service_active() {
  local SERVICE="${1}"

  if systemctl is-active "${SERVICE}"; then
    return 0
  else
    return 1
  fi

}

service_enabled() {
  local SERVICE="${1}"

  if systemctl is-enabled "${SERVICE}"; then
    return 0
  else
    return 1
  fi

}

#
# Main program body
#

while getopts ":hu:v" option; do
    case ${option} in
        h)  # Print the help message
            help
            exit 0
            ;;

        u)  # Save the provided unit
            SYSTEMD_UNIT="${OPTARG}"

            if ! [[ ${SYSTEMD_UNIT} == *.service ]]; then

                echo "Error: Specified unit must be a service."
                usage
                exit 3

            fi

            ;;

        v)  # Print the version
            echo "${VERSION}"
            exit 0
            ;;

        :)  # In case argument is missing
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
# Check if a systemd service unit was defined
#

if [[ -z ${SYSTEMD_UNIT} ]]; then

    echo "Error: A unit name must be specified."
    usage
    exit 3

fi

#
# Check if the specified service exists
#

if ! service_exists "${SYSTEMD_UNIT}" &> /dev/null; then

    echo "Critical: Service ${SYSTEMD_UNIT} not found at system."
    exit 2

fi

#
# Check if service is running
#

if ! service_active "${SYSTEMD_UNIT}" &> /dev/null; then

  echo "Critical: Service ${SYSTEMD_UNIT} is not running."
  exit 2

fi

#
# Check if service is enabled
#

if ! service_enabled "${SYSTEMD_UNIT}"; then

  echo: "Warning: Service ${SYSTEMD_UNIT} is not enabled."
  exit 1

fi

#
# If we end here, everything is fine
#

echo "${SYSTEMD_UNIT} is running an enabled -- OK."
exit 0
