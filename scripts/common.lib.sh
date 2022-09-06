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

woah_LANGS=("EN" "FR" "ES")
# from https://apps.who.int/whocc/Search.aspx
WHO_REGIONS=("AFRO" "AMRO" "EMRO" "EURO" "SEARO" "WPRO")
LSF_REMOTE_GIT="https://github.com/EticaAI/lexicographi-sine-finibus.git"
LSF_LOCAL_CLONED="$ROOTDIR/scripts/lexicographi-sine-finibus"
LSF_OFFICINA="$LSF_LOCAL_CLONED/officina"
#NUMERORDINATIO_BASIM="$LSF_OFFICINA"

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
# Compile HTML pages only
#
# Globals:
#   ROOTDIR
#   BUILDTEMPDIR
# Arguments:
#
# Returns
#   None
#######################################
compile_html_only() {
  printf "\n\t%40s\n" "${tty_blue}${FUNCNAME[0]} STARTED ${tty_normal}"
  set -x

  ./scripts/readme-from-csv.py \
    --method=compile-readme \
    --natural-language-objective=en \
    "${ROOTDIR}/index.template.html" \
    >"${ROOTDIR}/spatial-epidemiology-and-health-surveillance.html"

  # ./scripts/readme-from-csv.py \
  #   --method=compile-readme \
  #   --natural-language-objective=pt \
  #   "${ROOTDIR}/README.template.md" \
  #   >"${ROOTDIR}/README.pt.md"

  set +x
  printf "\t%40s\n" "${tty_green}${FUNCNAME[0]} FINISHED OKAY ${tty_normal}"
}

#######################################
# Compile READMEs
#
# Globals:
#   ROOTDIR
#   BUILDTEMPDIR
# Arguments:
#
# Returns
#   None
#######################################
compile_readme_only() {
  printf "\n\t%40s\n" "${tty_blue}${FUNCNAME[0]} STARTED ${tty_normal}"
  set -x

  ./scripts/readme-from-csv.py \
    --method=compile-readme \
    --natural-language-objective=en \
    "${ROOTDIR}/README.template.md" \
    >"${ROOTDIR}/README.md"

  ./scripts/readme-from-csv.py \
    --method=compile-readme \
    --natural-language-objective=pt \
    "${ROOTDIR}/README.template.md" \
    >"${ROOTDIR}/README.pt.md"

  set +x
  printf "\t%40s\n" "${tty_green}${FUNCNAME[0]} FINISHED OKAY ${tty_normal}"
}

#######################################
# crawler_who_cc fetch reference laboratories from
# World Organisation for Animal Health (WOAH, founded as OIE)
#
# Globals:
#   ROOTDIR
#   BUILDTEMPDIR
#   woah_LANGS
# Arguments:
#   repo        Repository to fetch the data
#   savepath    (optional) Path to store the metadata
# Returns
#   None
#######################################
crawler_woah_reflab() {
  # echo "${FUNCNAME[0]} TODO"
  printf "\n\t%40s\n" "${tty_blue}${FUNCNAME[0]} STARTED ${tty_normal}"

  _temp_merged_csv="$BUILDTEMPDIR/woah_reflab_all.csv"
  _temp_merged_sorted_csv="$BUILDTEMPDIR/woah_reflab.csv"
  _temp_merged_hxltm="$BUILDTEMPDIR/woah-reference-laboratories.csv"
  _data_published_hxltm="$ROOTDIR/data/woah-reference-laboratories.hxl.csv"

  outputs=()
  for lang in "${woah_LANGS[@]}"; do
    output="$BUILDTEMPDIR/woah_reflab_$lang.csv"

    # outputs+=("$output")
    if [ "$lang" = 'FR' ]; then
      outputs+=("$output")
    else
      echo "TODO is not possible to align translations, so we're using only \
french instead of merge then"
      continue
    fi
    # crawler_woah_reflab "$lang" "$output"
    set -x
    node "$ROOTDIR/scripts/etc/woah-reflab-downloader.js" \
      --woah-language "$lang" \
      --output "$output"
    set +x
    frictionless validate "$output"
    sleep 10
  done

  echo "NOTE is not possible to merge/align translations, so we're using only french"

  set -x
  # shellcheck disable=SC2048,SC2086
  csvjoin ${outputs[*]} >"$_temp_merged_csv"
  head -n 2 "$_temp_merged_csv"
  frictionless validate "$_temp_merged_csv"
  csvsort -c 1,2 "$_temp_merged_csv" >"$_temp_merged_sorted_csv"
  # # csvsort -c 1,2 "$BUILDTEMPDIR/woah_reflab_.csv" >"$BUILDTEMPDIR/whocc.csv"

  # echo "@TODO"

  # exit 1
  ./scripts/readme-from-csv.py \
    --method=table-rename \
    --table-meta=i18n/zxx/woah-reference-laboratories.yml \
    "$_temp_merged_sorted_csv" \
    >"$_temp_merged_hxltm"

  head -n 2 "$_temp_merged_hxltm"

  frictionless validate "$_temp_merged_hxltm"
  set +x

  if [ -f "$_data_published_hxltm" ]; then
    echo "deleting old [$_data_published_hxltm]"
    # rm "$_data_published"
  fi

  cp "$_temp_merged_hxltm" "$_data_published_hxltm"

  set +x
  printf "\t%40s\n" "${tty_green}${FUNCNAME[0]} FINISHED OKAY ${tty_normal}"
}

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

  _data_published="$ROOTDIR/data/who-collaborating-centres.hxl.csv"

  outputs=()
  for region in "${WHO_REGIONS[@]}"; do
    output="$BUILDTEMPDIR/$region.csv"
    outputs+=("$output")
    crawler_who_cc_fech_region "$region" "$output"
    frictionless validate "$output"
    sleep 10
  done

  set -x
  # shellcheck disable=SC2048,SC2086
  csvstack ${outputs[*]} >"$BUILDTEMPDIR/whocc_all.csv"
  frictionless validate "$BUILDTEMPDIR/whocc_all.csv"
  csvsort -c 1,2 "$BUILDTEMPDIR/whocc_all.csv" >"$BUILDTEMPDIR/whocc.csv"

  # @TODO: make this part more resilient to timeout errors

  ./scripts/readme-from-csv.py \
    --method=table-rename \
    --table-meta=i18n/zxx/who-collaborating-centres.meta.yml \
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
# Build local copy of crosswalk
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
crawler_wikidata_who_icd() {
  # whoccregion="$1"
  # output="$2"
  printf "\n\t%40s\n" "${tty_blue}${FUNCNAME[0]} STARTED ${tty_normal}"
  # echo "TODO"

  temporarium_hxltm="$BUILDTEMPDIR/P7329~P493+P494+P5806+P7329+P7807.tm.hxl.csv"
  temporarium_hxltm_data="$ROOTDIR/data/who-icd-crosswalk.tm.hxl.csv"
  set -x
  # node "$ROOTDIR/scripts/etc/whocc-downloader.js" \
  #   --who-region "$whoccregion" \
  #   --output "$output"
  printf "P7329\n" |
    NUMERORDINATIO_BASIM="${LSF_OFFICINA}" "${LSF_OFFICINA}/999999999/0/1603_3_12.py" \
      --actionem-sparql \
      --de=P \
      --query \
      --ex-interlinguis \
      --identitas-ex-wikiq \
      --cum-interlinguis=P493,P494,P5806,P7329,P7807 |
    NUMERORDINATIO_BASIM="${LSF_OFFICINA}" "${LSF_OFFICINA}/999999999/0/1603_3_12.py" \
      --actionem-sparql \
      --identitas-ex-wikiq \
      --csv --hxltm \
      >"$temporarium_hxltm"

  # Reasoning for --skip-errors=type-error: SNOMED CT identifier is interpreted
  # as integer (which is correct) but we can have joined values
  # (such as 250102002|203597000) for the primary key
  frictionless validate \
    --skip-errors=type-error \
    "$temporarium_hxltm"

  head -n 11 "$temporarium_hxltm" >"$temporarium_hxltm_data"

  set +x
  printf "\t%40s\n" "${tty_green}${FUNCNAME[0]} FINISHED OKAY ${tty_normal}"
}

#######################################
# Build local copy of crosswalk
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
crawler_wikipedia_bsl4facilities() {
  # whoccregion="$1"
  # output="$2"
  printf "\n\t%40s\n" "${tty_blue}${FUNCNAME[0]} STARTED ${tty_normal}"
  echo "TODO"

  # exit 1

  source_url="https://en.wikipedia.org/wiki/Biosafety_level"
  temporarium_csv="$ROOTDIR/partials/raw/wikipedia-table/biosafety-level-4-laboratories.csv"
  temporarium_hxl="$BUILDTEMPDIR/biosafety-level-4-laboratories.hxl.csv"
  frictionless_tempdir="$ROOTDIR/partials/raw/wikipedia-table/"
  frictionless_tempdir_datapackage="biosafety-level-4-laboratories.datapackage.json"
  frictionless_tempdir_datapackage="biosafety-level-4-laboratories.datapackage.json"
  temporarium_hxltm_data="$ROOTDIR/partials/raw/wikipedia-table/biosafety-level-4-laboratories.csv"

  _data_published="$ROOTDIR/data/biosafety-level-4-laboratories.hxl.csv"

  set -x

  PANDAS_READ_HTML__INDEXTABLE=1 ./scripts/readme-from-csv.py \
    --method='extract-remote-html-table' \
    "$source_url" >"$temporarium_csv"

  head -n 2 "$temporarium_csv"

  cd "$frictionless_tempdir"

  # If something goes wrong, frictionless will warn us already at this point
  frictionless validate "$frictionless_tempdir_datapackage"

  cd "$ROOTDIR"

  ./scripts/readme-from-csv.py \
    --method=table-rename \
    --table-meta=i18n/zxx/biosafety-level-4-facilities.meta.yml \
    "$temporarium_csv" \
    >"$temporarium_hxl"

  head -n 2 "$temporarium_hxl"

  frictionless validate "$temporarium_hxl"

  set +x
  if [ -f "$_data_published" ]; then
    echo "deleting old [$_data_published]"
    rm "$_data_published"
  fi

  cp "$temporarium_hxl" "$_data_published"
  printf "\t%40s\n" "${tty_green}${FUNCNAME[0]} FINISHED OKAY ${tty_normal}"
}

#######################################
# Clone remote LSF git to local path (for additional heavy build process)
#
# Globals:
#   ROOTDIR
#   LSF_REMOTE_GIT
#   LSF_LOCAL_CLONED
# Arguments:
#
# Returns
#   None
#######################################
gh_clone_lsf_to_scripts() {
  remote_git="$LSF_REMOTE_GIT"
  local_dir="$LSF_LOCAL_CLONED"

  if [ -f "${local_dir}" ]; then
    echo "Already cached [${local_dir}]. Skiping"
    return 0
  fi

  set -x
  git clone "$remote_git" "$local_dir"
  set +x
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
