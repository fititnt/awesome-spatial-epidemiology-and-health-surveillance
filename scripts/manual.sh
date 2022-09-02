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


PANDAS_READ_HTML__INDEXTABLE=1 ./scripts/readme-from-csv.py --method='extract-remote-html-table' https://en.wikipedia.org/wiki/Biosafety_level > partials/raw/wikipedia-table/biosafety-level-laboratories.csv

PANDAS_READ_HTML__INDEXTABLE=0 ./scripts/readme-from-csv.py --method='extract-remote-html-table' https://en.wikipedia.org/wiki/List_of_infectious_diseases > partials/temp/List_of_infectious_diseases.csv


./scripts/readme-from-csv.py --method='extract-remote-html-table' 'https://apps.who.int/whocc/List.aspx?UHfehFaaKUEdGSfqs%2fFGLg=%3d' > partials/raw/who-ccg.csv

./scripts/readme-from-csv.py --method='extract-remote-html-table' https://en.wikipedia.org/wiki/Infections_associated_with_diseases > partials/temp/Infections_associated_with_diseases.csv


# wc -l partials/temp/who-ccg/*.tsv
#     30 partials/temp/who-ccg/who-ccg-chrome-scrapper_AFRO.tsv
#    181 partials/temp/who-ccg/who-ccg-chrome-scrapper_AMRO.tsv
#     55 partials/temp/who-ccg/who-ccg-chrome-scrapper_EMRO.tsv
#    265 partials/temp/who-ccg/who-ccg-chrome-scrapper_EURO.tsv
#     99 partials/temp/who-ccg/who-ccg-chrome-scrapper_SEARO.tsv
#    197 partials/temp/who-ccg/who-ccg-chrome-scrapper_WPRO.tsv
#    827 total
