#!/bin/bash
#===============================================================================
#
#          FILE:  via-github-action.sh
#
#         USAGE:  OPERATION='<type>'./scripts/via-github-action.sh
#
#   DESCRIPTION:  ---
#
#       OPTIONS:  ---
#
#  REQUIREMENTS:  - bash
#                 - python3 (used by readme-from-csv.py)
#                 - jq
#                 - github cli
#          BUGS:  ---
#         NOTES:  ---
#        AUTHOR:  Emerson Rocha <rocha[at]ieee.org>
#       COMPANY:  EticaAI
#       LICENSE:  Public Domain dedication
#                 SPDX-License-Identifier: Unlicense
#       VERSION:  v1.1
#       CREATED:  2022-08-31 03:08 UTC
#      REVISION:  2022-09-03 14:40 UTC v1.1 functons moved to common.lib.sh
#===============================================================================
set -e

__ROOTDIR="$(pwd)"
ROOTDIR="${ROOTDIR:-$__ROOTDIR}"

#### Functions _________________________________________________________________

# shellcheck source=common.lib.sh
. "$ROOTDIR"/scripts/common.lib.sh

#### Main ______________________________________________________________________

# OPERATION=compile_html_only ./scripts/via-github-action.sh
if [ "$OPERATION" = "compile_html_only" ]; then
  compile_html_only
  exit 0
fi
# OPERATION=compile_readme_only ./scripts/via-github-action.sh
if [ "$OPERATION" = "compile_readme_only" ]; then
  compile_readme_only
  exit 0
fi

## WARNING: this part may have some timeouts; so try again 1 or 2 times if fail
# OPERATION=crawler_who_cc ./scripts/via-github-action.sh
if [ "$OPERATION" = "crawler_who_cc" ]; then
  crawler_who_cc
fi

# OPERATION=gh_clone_lsf_to_scripts ./scripts/via-github-action.sh
if [ "$OPERATION" = "gh_clone_lsf_to_scripts" ]; then
  gh_clone_lsf_to_scripts
  exit 0
fi

# OPERATION=crawler_wikidata_who_icd ./scripts/via-github-action.sh
if [ "$OPERATION" = "crawler_wikidata_who_icd" ]; then
  crawler_wikidata_who_icd
  exit 0
fi

# OPERATION=crawler_woah_reflab ./scripts/via-github-action.sh
if [ "$OPERATION" = "crawler_woah_reflab" ]; then
  crawler_woah_reflab
  exit 0
fi

# OPERATION=crawler_wikipedia_bsl4facilities ./scripts/via-github-action.sh
if [ "$OPERATION" = "crawler_wikipedia_bsl4facilities" ]; then
  crawler_wikipedia_bsl4facilities
  exit 0
fi

echo "unknow operation [$OPERATION]"
exit 1
