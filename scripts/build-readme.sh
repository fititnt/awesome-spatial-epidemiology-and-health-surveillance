#!/bin/sh
#===============================================================================
#
#          FILE:  build-readme.sh
#
#         USAGE:  ./scripts/build-readme.sh
#
#   DESCRIPTION:  ---
#
#       OPTIONS:  ---
#
#  REQUIREMENTS:  - asciidoc
#                   - sudo apt install asciidoc
#                 - pandoc (version 2.17 or higher; very important)
#                   - sudo apt install pandoc
#          BUGS:  ---
#         NOTES:  ---
#        AUTHOR:  Emerson Rocha <rocha[at]ieee.org>
#       COMPANY:  EticaAI
#       LICENSE:  Public Domain dedication
#                 SPDX-License-Identifier: Unlicense
#       VERSION:  v1.0
#       CREATED:  2022-08-31 03:08 UTC
#      REVISION:  ---
#===============================================================================
set -e

# asciidoctor --backend docbook README.source.adoc --out-file README.source.xml

# @see https://matthewsetter.com/convert-markdown-to-asciidoc-withpandoc/

# pandoc --atx-headers \
#     --normalize \
#     --verbose \
#     --wrap=none \
#     --toc \
#     --reference-links \
#     -s -S -o -t asciidoc path/to/your/asciidoc/file.adoc \
#     path/to/your/markdown/file.md

# pandoc --atx-headers \
#     --normalize \
#     --verbose \
#     --wrap=none \
#     --toc \
#     --reference-links \
#     -s -S -o -t asciidoc README.source.adoc \
#     README-preview.md
# pandoc --atx-headers \
#     --verbose \
#     --wrap=none \
#     --toc \
#     --reference-links \
#     --from=asciidoc \
#     --to=markdown+smart \
#     -s README.source.adoc \
#     README-preview.md

set -x

./scripts/readme-from-csv.py \
  data/general-concepts.hxl.csv \
  --line-formatter='==== {raw_line[1]}\n`{raw_line}`\n' \
  >partials/general-concepts.md

./scripts/readme-from-csv.py \
  data/github-topics.hxl.csv \
  --line-formatter='==== {raw_line[1]}\n`{raw_line}`\n' \
  --line-select='{raw_line[0]}==1' \
  >partials/github-topics_1.md

# @TODO implement checking how many repos are in a topic
#       https://docs.github.com/en/rest/search#search-topics
# @TODO https://gist.github.com/usametov/af8f13a351a66fb05a9895f11417dd9d

./scripts/readme-from-csv.py \
  data/github-topics.hxl.csv \
  --line-formatter='- [{raw_line[1]}](https://github.com/topics/{raw_line[2]}): {raw_line[2]} repositories' \
  --line-select='{raw_line[0]}==1' \
  >partials/github-topics_1.md

./scripts/readme-from-csv.py \
  data/github-topics.hxl.csv \
  --line-formatter='- [{raw_line[1]}](https://github.com/topics/{raw_line[2]}): {raw_line[2]} repositories' \
  --line-select='{raw_line[0]}==2' \
  >partials/github-topics_2.md

./scripts/readme-from-csv.py \
  data/github-topics.hxl.csv \
  --line-formatter='- [{raw_line[1]}](https://github.com/topics/{raw_line[2]}): {raw_line[2]} repositories' \
  --line-select='{raw_line[0]}==3' \
  >partials/github-topics_3.md

./scripts/readme-from-csv.py \
  data/software.hxl.csv \
  --line-formatter='==== {raw_line[1]}\n{raw_line}\n' \
  >partials/software.md

./scripts/readme-from-csv.py \
  --method=compile-readme \
  README.template.md \
  >README-preview.md

# asciidoctor --backend docbook5 README.source.adoc --out-file README.source.xml

# NOTE: asciidoctor does not support itemizedlist spacing="compact"
# configuration so we edit the intermediary format to enforce it.
# @see https://discuss.asciidoctor.org
# /Not-finding-my-way-in-trying-to-produce-a-quot-compact-list-quot-td1210.html
# sed -i 's/<itemizedlist>/<itemizedlist spacing="compact">/g' README.source.xml

# @TODO maybe update pandoc version to > 2.17
#       see https://github.com/jgm/pandoc/issues/7799

# <itemizedlist spacing="compact">

# pandoc \
#   --read=docbook \
#   --write=markdown+smart \
#   --output=README-preview.md \
#   README.source.xml

# pandoc \
#   --wrap=none \
#   --read=docbook \
#   --write=gfm \
#   --output=README-preview.md \
#   README.source.xml

# About issues with too much spaces on lists
# - https://github.com/jgm/pandoc/issues/7172

# pandoc \
#   --wrap=none \
#   --read=docbook \
#   --write=markdown_strict \
#   --output=README-preview.md \
#   README.source.xml

# pandoc \
#   --atx-headers \
#   --wrap=none \
#   --read=docbook \
#   --write=gfm \
#   --output=README-preview.md \
#   README.source.xml

# pandoc \
#   --atx-headers \
#   --wrap=none \
#   --write=gfm \
#   --output=README-preview.md \
#   README.source.xml

# pandoc \
#   --wrap=none \
#   --write=gfm \
#   --read=docbook \
#   --output=README-preview.md \
#   README.source.xml

# sed -i '/^    $/d' README-preview.md
# sed -i '/^    $/d' README-preview.md

set +x

# frictionless describe --json data/github-topics.hxl.csv
# frictionless describe --json data/general-concepts.hxl.csv
# frictionless describe --json data/software.hxl.csv

# frictionless validate datapackage.json

# @TODO - https://github.com/sindresorhus/awesome/issues/2242
#       - https://github.com/danielecook/Awesome-Bioinformatics/blob/master/.github/workflows/url-check.yml
#       - https://github.com/peter-evans/link-checker

exit 0

# installing pandoc from source

# https://github.com/jgm/pandoc/releases/tag/2.19.2

wget https://github.com/jgm/pandoc/releases/download/2.19.2/pandoc-2.19.2-linux-amd64.tar.gz -o /tmp/pandoc.tar.gz

# @TODO implement search for topics

# gh api \
#   -H "Accept: application/vnd.github+json" \
#   /search/repositories?q=topic:bioinformatics
# https://github.com/search?q=topic%3Abioinformatics&type=Repositories&ref=advsearch&l=&l=

gh api \
  -H "Accept: application/vnd.github+json" \
  /search/repositories?q=topic:spatial-epidemiology

gh api \
  -H "Accept: application/vnd.github+json" \
  /search/repositories?q=topic:spatial-epidemiology | jq .total_count
