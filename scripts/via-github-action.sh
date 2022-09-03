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

if [ "$OPERATION" = "build-readme" ]; then
  echo "$OPERATION"
  exit 0
fi
if [ "$OPERATION" = "crawler_who_cc" ]; then
  crawler_who_cc
fi

echo "unknow operation [$OPERATION]"
exit 1
