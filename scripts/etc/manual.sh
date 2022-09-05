#!/bin/bash
#===============================================================================
#
#          FILE:  manual.sh
#
#         USAGE:  ./scripts/etc/manual.sh
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

dos2unix partials/raw/etc/whocc/*.csv

frictionless validate partials/raw/etc/whocc/AFRO.csv
csvformat validate partials/raw/etc/whocc/AFRO.csv

csvformat partials/raw/etc/whocc/AFRO.csv | frictionless validate

csvformat partials/raw/etc/whocc/AFRO.csv > partials/raw/temp/whocc---AFRO.csv
csvformat partials/raw/etc/whocc/AFRO.csv > partials/temp/whocc---AFRO.csv
frictionless validate partials/temp/whocc---AFRO.csv

cat partials/raw/etc/whocc/AFRO.csv | perl -0pe 's/(text\s*=\s*)".*?"/$1""/s'

cat partials/raw/etc/whocc/AFRO.csv | sed 's/WHO Collaborating Centres\n\nGlobal database/WHO Collaborating Centres Global database/'

cat partials/raw/etc/whocc/AFRO.csv | sed 's/\r\n/'
cat partials/raw/etc/whocc/AFRO.csv | sed -z 's/Centres\r\nGlobal/Centres Global/g'

cat partials/raw/etc/whocc/AFRO.csv | sed -E "s/WHO Collaborating Centres[[:space:]]+Global database/WHO Collaborating Centres Global database/g"

cat partials/raw/etc/whocc/AFRO.csv | sed -E "s/Centres[[:space:]]+Global/Centres Global/g"
cat partials/raw/etc/whocc/AFRO.csv | sed -E "s/Centres\s\sGlobal/Centres Global/g"

cat partials/raw/etc/whocc/AFRO.csv | sed '/^tomcat\.util.*$/,/^.*[^\]$/d'

WHO Collaborating Centres Global database

# Replaces =========================================
cat partials/raw/etc/whocc/AMRO.csv | sed 's/Centres\
\
Global/Centres Global/g'
cat partials/raw/etc/whocc/AMRO.csv | sed 's/Centres\
Global/Centres Global/g'

expression='/Centres '\
'Global/d'
cat partials/raw/etc/whocc/AMRO.csv  | sed -E -e "$expression"

sed -e '
  /BEGIN/,/END/!b
  //!d;/END/!b
  r content.js
  N
' long.js

sed -e '/Centres/,/Global/!b' -e '/end/!d;r file2.txt' -e 'd' file1.txt

cat partials/raw/etc/whocc/AMRO.csv  | sed -n '1h;1!H;${g;s/search/replace/;p;}'


source_1="WHO Collaborating Centres

Global database"
target_1="WHO Collaborating Centres Global database"

# Remove extra line breaks inside text files
source_1='.

"'
target_1='."'

cat partials/raw/etc/whocc/AFRO.csv | tr -d '\r' | sed -e 's/Collaborating Centres\nGlobal database/Collaborating Centres\nGlobal database/g'


# https://github.com/robdmc/pandashells


frictionless validate datapackage.json

# shellcheck disable=SC2002
cat data/software.hxl.csv | p.df 'df.describe().T' -o table


PANDAS_READ_HTML__INDEXTABLE=1 ./scripts/readme-from-csv.py --method='extract-remote-html-table' https://en.wikipedia.org/wiki/Biosafety_level > partials/raw/wikipedia-table/biosafety-level-4-laboratories.csv

cd partials/raw/wikipedia-table/
frictionless validate biosafety-level-4-laboratories.datapackage.json

PANDAS_READ_HTML__INDEXTABLE=0 ./scripts/readme-from-csv.py --method='extract-remote-html-table' https://en.wikipedia.org/wiki/List_of_infectious_diseases > partials/temp/List_of_infectious_diseases.csv


./scripts/readme-from-csv.py --method='extract-remote-html-table' 'https://apps.who.int/whocc/List.aspx?UHfehFaaKUEdGSfqs%2fFGLg=%3d' > partials/raw/who-collaborating-centresg.csv

./scripts/readme-from-csv.py --method='extract-remote-html-table' https://en.wikipedia.org/wiki/Infections_associated_with_diseases > partials/temp/Infections_associated_with_diseases.csv


# wc -l partials/temp/who-collaborating-centresg/*.tsv
#     30 partials/temp/who-collaborating-centresg/who-collaborating-centresg-chrome-scrapper_AFRO.tsv
#    181 partials/temp/who-collaborating-centresg/who-collaborating-centresg-chrome-scrapper_AMRO.tsv
#     55 partials/temp/who-collaborating-centresg/who-collaborating-centresg-chrome-scrapper_EMRO.tsv
#    265 partials/temp/who-collaborating-centresg/who-collaborating-centresg-chrome-scrapper_EURO.tsv
#     99 partials/temp/who-collaborating-centresg/who-collaborating-centresg-chrome-scrapper_SEARO.tsv
#    197 partials/temp/who-collaborating-centresg/who-collaborating-centresg-chrome-scrapper_WPRO.tsv
#    827 total


