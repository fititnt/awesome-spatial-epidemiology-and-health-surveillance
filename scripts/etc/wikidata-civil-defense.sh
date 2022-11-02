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


  objectivum_archivum="${ROOTDIR}/data/3/wikidata-civil-defense.hxl.csv"
  objectivum_archivum_temporarium_csv="${BUILDTEMPDIR}/wikidata_civil_defense.TEMP.csv"

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

  curl --header "Accept: text/csv" --silent --show-error \
    --get https://query.wikidata.org/sparql --data-urlencode query='
SELECT ?country ?unm49 ?iso3166n ?iso3166p1a2 ?iso3166p1a3 ?osmrelid ?unescot ?usciafb ?usfips4 ?gadm
WHERE
{
  ?country wdt:P31 wd:Q6256 ;
  OPTIONAL { ?country wdt:P2082 ?unm49. }
  OPTIONAL { ?country wdt:P299 ?iso3166n. }
  OPTIONAL { ?country wdt:P297 ?iso3166p1a2. }
  OPTIONAL { ?country wdt:P298 ?iso3166p1a3. }
  OPTIONAL { ?country wdt:P402 ?osmrelid. }
  OPTIONAL { ?country wdt:P3916 ?unescot. }
  OPTIONAL { ?country wdt:P9948 ?usciafb. }
  OPTIONAL { ?country wdt:P901 ?usfips4. }
  OPTIONAL { ?country wdt:P8714 ?gadm. }   
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE]". }
}
' >"$objectivum_archivum_temporarium_csv"

  set +x
  printf "\t%40s\n" "${tty_green}${FUNCNAME[0]} FINISHED OKAY ${tty_normal}"
}

wikidata_civil_defense
