#!/bin/bash
#===============================================================================
#
#          FILE:  wikidata-civil-defense.sh
#
#         USAGE:  ./scripts/etc/wikidata-civil-defense.sh
#
#   DESCRIPTION:  Wikidata Civil defende organizations
#
#       OPTIONS:  ---
#
#  REQUIREMENTS:  ---
#          BUGS:  ---
#         NOTES:  ---
#        AUTHOR:  Emerson Rocha <rocha[at]ieee.org>
#       COMPANY:  EticaAI
#       LICENSE:  Public Domain dedication
#                 SPDX-License-Identifier: Unlicense
#       VERSION:  v1.0
#       CREATED:  2022-10-28 21:56 UTC
#      REVISION:  ---
#===============================================================================
set -e

__ROOTDIR="$(pwd)"
ROOTDIR="${ROOTDIR:-$__ROOTDIR}"

__BUILDTEMPDIR="$ROOTDIR/partials/temp"
BUILDTEMPDIR="${BUILDTEMPDIR:-$__BUILDTEMPDIR}"

#### Fancy colors constants - - - - - - - - - - - - - - - - - - - - - - - - - -
# shellcheck disable=SC2034
tty_blue=$(tput setaf 4)
# shellcheck disable=SC2034
tty_green=$(tput setaf 2)
# shellcheck disable=SC2034
tty_red=$(tput setaf 1)
# shellcheck disable=SC2034
tty_normal=$(tput sgr0)

## Example
# printf "\n\t%40s\n" "${tty_blue}${FUNCNAME[0]} STARTED ${tty_normal}"
# printf "\t%40s\n" "${tty_green}${FUNCNAME[0]} FINISHED OKAY ${tty_normal}"
# printf "\t%40s\n" "${tty_blue} INFO: [] ${tty_normal}"
# printf "\t%40s\n" "${tty_red} ERROR: [] ${tty_normal}"
#### Fancy colors constants - - - - - - - - - - - - - - - - - - - - - - - - - -

#######################################
# ...
#
# Globals:
#   ROOTDIR
#   BUILDTEMPDIR
# Arguments:
#
# Returns
#   None
#######################################
wikidata_civil_defense() {
  printf "\n\t%40s\n" "${tty_blue}${FUNCNAME[0]} STARTED ${tty_normal}"
  set -x

  # ./scripts/readme-from-csv.py \
  #   --method=compile-readme \
  #   --natural-language-objective=en \
  #   "${ROOTDIR}/index.template.html" \
  #   >"${ROOTDIR}/spatial-epidemiology-and-health-surveillance.html"

  # # ./scripts/readme-from-csv.py \
  # #   --method=compile-readme \
  # #   --natural-language-objective=pt \
  # #   "${ROOTDIR}/README.template.md" \
  # #   >"${ROOTDIR}/README.pt.md"

  set +x
  printf "\t%40s\n" "${tty_green}${FUNCNAME[0]} FINISHED OKAY ${tty_normal}"
}

wikidata_civil_defense
