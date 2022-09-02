#!/bin/bash
#===============================================================================
#
#          FILE:  manual.sh
#
#         USAGE:  ./scripts/manual.sh
#
#   DESCRIPTION:  Generic non automated commands.
#
#       OPTIONS:  ---
#
#  REQUIREMENTS:  - pandashells (https://github.com/robdmc/pandashells)
#                 - frictionless https://github.com/frictionlessdata/framework
#          BUGS:  ---
#         NOTES:  ---
#        AUTHOR:  Emerson Rocha <rocha[at]ieee.org>
#       COMPANY:  EticaAI
#       LICENSE:  Public Domain dedication
#                 SPDX-License-Identifier: Unlicense
#       VERSION:  v1.0
#       CREATED:  2022-09-02 12:19 UTC
#      REVISION:  ---
#===============================================================================
set -e

echo "README, not execute me"
exit 1

# https://github.com/robdmc/pandashells


frictionless validate datapackage.json

# shellcheck disable=SC2002
cat data/software.hxl.csv | p.df 'df.describe().T' -o table


PANDAS_READ_HTML__INDEXTABLE=1 ./scripts/readme-from-csv.py --method='extract-remote-html-table' https://en.wikipedia.org/wiki/Biosafety_level > partials/temp/biosafety.csv

PANDAS_READ_HTML__INDEXTABLE=0 ./scripts/readme-from-csv.py --method='extract-remote-html-table' https://en.wikipedia.org/wiki/List_of_infectious_diseases > partials/temp/List_of_infectious_diseases.csv


./scripts/readme-from-csv.py --method='extract-remote-html-table' 'https://apps.who.int/whocc/List.aspx?UHfehFaaKUEdGSfqs%2fFGLg=%3d' > partials/temp/who-ccg.csv
