#!/bin/bash
#===============================================================================
#
#          FILE:  common.lib.sh
#                 scripts/common.lib.sh
#
#         USAGE:  #import on other scripts
#                 . "$ROOTDIR"/scripts/common.lib.sh
#
#   DESCRIPTION:  Generic utility helper for shell
#
#  REQUIREMENTS:  - bash
#                 - python3 (used by readme-from-csv.py)
#                 - jq
#                 - github cli
#                 - csvkit
#          BUGS:  ---
#         NOTES:  ---
#        AUTHOR:  Emerson Rocha <rocha[at]ieee.org>
#       COMPANY:  EticaAI
#       LICENSE:  Public Domain dedication
#                 SPDX-License-Identifier: Unlicense
#       VERSION:  v1.1
#       CREATED:  2022-08-31 03:08 UTC
#      REVISION:  2022-09-03 14:40 UTC v1.1 build-readme.sh -> common.lib.sh
#===============================================================================
set -e

__ROOTDIR="$(pwd)"
ROOTDIR="${ROOTDIR:-$__ROOTDIR}"

__BUILDTEMPDIR="$ROOTDIR/partials/temp"
BUILDTEMPDIR="${BUILDTEMPDIR:-$__BUILDTEMPDIR}"

#### Configurable variables  - - - - - - - - - - - - - - - - - - - - - - - - - -
# from https://apps.who.int/whocc/Search.aspx
WHO_REGIONS=("AFRO" "AMRO" "EMRO" "EURO" "SEARO" "WPRO")
# WHO_CSVFIELDS=(
#   "textbox105|code"   # SOA-5 [AFRO]
#   "textbox106|status" # Active,Pending
#   "textbox113|name" # Active,Pending
#   "textbox20|region" # Active,Pending
#   "textbox19|country" # Active,Pending
#   "textbox127|website" # Active,Pending
# )

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
# crawler_who_cc raw CSVs from WHO Collaborating Centres
#
# Globals:
#   ROOTDIR
#   BUILDTEMPDIR
#   WHO_REGIONS
# Arguments:
#   repo        Repository to fetch the data
#   savepath    (optional) Path to store the metadata
# Returns
#   None
#######################################
crawler_who_cc() {
  # echo "${FUNCNAME[0]} TODO"
  printf "\n\t%40s\n" "${tty_blue}${FUNCNAME[0]} STARTED ${tty_normal}"

  _data_published="$ROOTDIR/data/who-collaborating-centre.hxl.csv"

  outputs=()
  for region in "${WHO_REGIONS[@]}"; do
    output="$BUILDTEMPDIR/$region.csv"
    outputs+=("$output")
    # crawler_who_cc_fech_region "$region" "$output"
    # frictionless validate "$output"
    # sleep 10
  done

  set -x
  # shellcheck disable=SC2048,SC2086
  csvstack ${outputs[*]} >"$BUILDTEMPDIR/whocc_all.csv"
  frictionless validate "$BUILDTEMPDIR/whocc_all.csv"
  csvsort -c 1,2 "$BUILDTEMPDIR/whocc_all.csv" >"$BUILDTEMPDIR/whocc.csv"

  ./scripts/readme-from-csv.py \
    --method=table-rename \
    --table-meta=i18n/mul/whocc.meta.yml \
    "$BUILDTEMPDIR/whocc.csv" \
    >"$BUILDTEMPDIR/whocc.hxl.csv"

  frictionless validate "$BUILDTEMPDIR/whocc.hxl.csv"

  if [ -f "$_data_published" ]; then
    echo "deleting old [$_data_published]"
    # rm "$_data_published"
  fi

  cp "$BUILDTEMPDIR/whocc.hxl.csv" "$_data_published"

  set +x
  printf "\t%40s\n" "${tty_green}${FUNCNAME[0]} FINISHED OKAY ${tty_normal}"
}

#######################################
# Used by crawler_who_cc to fetch region per region
#
# Globals:
#   ROOTDIR
#   BUILDTEMPDIR
# Arguments:
#   repo        Repository to fetch the data
#   savepath    (optional) Path to store the metadata
# Returns
#   None
#######################################
crawler_who_cc_fech_region() {
  whoccregion="$1"
  output="$2"
  printf "\n\t%40s\n" "${tty_blue}${FUNCNAME[0]} STARTED \
  [$whoccregion] [$output] ${tty_normal}"
  set -x
  node "$ROOTDIR/scripts/etc/whocc-downloader.js" \
    --who-region "$whoccregion" \
    --output "$output"
  set +x
  printf "\t%40s\n" "${tty_green}${FUNCNAME[0]} FINISHED OKAY ${tty_normal}"
}

#######################################
# Fetch repo statistics of one repository
#
# Globals:
#
# Arguments:
#   repo        Repository to fetch the data
#   savepath    (optional) Path to store the metadata
# Returns
#   None
#######################################
gh_repo_statistics() {
  repo="${1}"
  repo="${repo//https:\/\/github.com\/''/}" # Remove full url, if exist
  savepath="${2-"partials/raw"}"
  fullsavepath="${savepath}/github-repo/${repo//\//'__'}.json"

  # echo "TODO repo[$repo] savepath[$savepath] fullsavepath [$fullsavepath]"

  if [ -f "${fullsavepath}" ]; then
    echo "Cached file [${fullsavepath}]. Skiping"
    echo "@TODO implement better stale-cache system"
    return 0
  fi

  # We delete some verbose fields such as .owner and .organization with jq
  # Then, sed is used to delete lots of something_url field
  gh api \
    -H "Accept: application/vnd.github+json" \
    "/repos/${repo}" |
    jq 'del(.owner)' |
    jq 'del(.organization)' |
    sed -e '/_url/d' \
      >"${fullsavepath}"
  # exit 1
  sleep 3
}

#######################################
# Iterate list with all repositories and call gh_repo_statistics()
#
# Globals:
#
# Arguments:
#   repo_list  (optional)  File with list of repositories
# Returns
#   None
#######################################
gh_repo_statistics_list() {
  repo_list="${1-"partials/raw/github-projects-list.txt"}"
  repo_summary="${2-"partials/raw/github-projects.tsv"}"

  while read -r line; do
    # echo "$line"
    gh_repo_statistics "$line"
  done <"$repo_list"

  touch "$repo_summary"
  printf "%s\n" "repo	created_at	updated_at	pushed_at	stargazers_count	watchers_count	forks_count	open_issues_count	language	license	homepage	description" >"$repo_summary"
  for fullpath in partials/raw/github-repo/*.json; do
    full_name=$(jq --raw-output '.full_name' <"$fullpath")
    created_at=$(jq --raw-output '.created_at' <"$fullpath")
    updated_at=$(jq --raw-output '.updated_at' <"$fullpath")
    pushed_at=$(jq --raw-output '.pushed_at' <"$fullpath")
    stargazers_count=$(jq '.stargazers_count' <"$fullpath")
    watchers_count=$(jq '.watchers_count' <"$fullpath")
    forks_count=$(jq '.forks_count' <"$fullpath")
    open_issues_count=$(jq '.open_issues_count' <"$fullpath")
    language=$(jq --raw-output '.language ' <"$fullpath")
    license=$(jq --raw-output '.license.spdx_id ' <"$fullpath")
    homepage=$(jq --raw-output '.homepage ' <"$fullpath")
    description=$(jq --raw-output '.description' <"$fullpath")
    repo="https://github.com/$full_name"
    printf "%s\n" "$repo	$created_at	$updated_at	$pushed_at	$stargazers_count	$watchers_count	$forks_count	$open_issues_count	$language	$license	$homepage	$description" >>"$repo_summary"
  done
}

#######################################
# Fetch repo statistics of one repository
#
# Globals:
#
# Arguments:
#   repo        Repository to fetch the data
#   savepath    (optional) Path to store the metadata
# Returns
#   None
#######################################
gh_topic_statistics() {
  topic="${1}"
  topic="${topic//https:\/\/github.com\/topics\/''/}" # Remove full url, if exist
  savepath="${2-"partials/raw"}"
  fullsavepath="${savepath}/github-topic/${topic}.json"

  # echo "TODO gh_topic_statistics topic[$topic] savepath[$savepath] fullsavepath [$fullsavepath]"
  # exit 1
  if [ -f "${fullsavepath}" ]; then
    echo "Cached file [${fullsavepath}]. Skiping"
    echo "@TODO implement better stale-cache system"
    return 0
  fi

  # set -x
  # Here we delete only items (which would return the repositories for this topic)
  gh api \
    -H "Accept: application/vnd.github+json" \
    "/search/repositories?q=topic:${topic}" |
    jq 'del(.items)' \
      >"${fullsavepath}"
  # exit 1
  sleep 3
}

#######################################
# Iterate list with all topics and call gh_topic_statistics()
#
# Globals:
#
# Arguments:
#   topics_list     (optional)  File with list of topics
#   topics_summary  (optional)  File with list of topics
# Returns
#   None
#######################################
gh_topics_statistics_list() {
  topics_list="${1-"partials/raw/github-topic-list.txt"}"
  topics_summary="${2-"partials/raw/github-topic.tsv"}"

  while read -r line; do
    # echo "gh_topics_statistics_list [$line]"
    gh_topic_statistics "$line"
  done <"$topics_list"

  touch "$topics_summary"
  echo "topic	url	total_count" >"$topics_summary"
  for fullpath in partials/raw/github-topic/*.json; do
    topic=$(basename "$fullpath" .json)
    url="https://github.com/topics/$topic"
    # echo "TODO filename[$fullpath]"
    count=$(jq '.total_count' <"$fullpath")
    # echo "topic[$topic] count[$count]"
    echo "$topic	$url	$count" >>"$topics_summary"
  done
}

#######################################
# Iterate list with all topics and call gh_topic_statistics()
#
# Globals:
#
# Arguments:
#   topics_current   (optional)  File with list of topics
#   topics_summary   (optional)  File with list of topics
# Returns
#   None
#######################################
gh_topics_statistics_consolidate() {
  #topics_current="${1-"partials/raw/github-topic.csv"}"
  #topics_history="${1-"data/github-topics-evolution.csv"}"

  echo "@TODO gh_topics_statistics_consolidate"

  # while read -r line; do
  #   # echo "gh_topics_statistics_list [$line]"
  #   gh_topic_statistics "$line"
  # done <"$topics_current"

  # touch "$topics_summary"
  # echo "topic,url,total_count" >"$topics_summary"
  # for fullpath in partials/raw/github-topic/*.json; do
  #   topic=$(basename "$fullpath" .json)
  #   url="https://github.com/topics/$topic"
  #   # echo "TODO filename[$fullpath]"
  #   count=$(jq '.total_count' <"$fullpath")
  #   # echo "topic[$topic] count[$count]"
  #   echo "$topic,$url,$count" >>"$topics_summary"
  # done
}
