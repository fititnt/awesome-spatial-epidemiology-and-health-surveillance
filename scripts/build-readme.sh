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
#                 - pandoc
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

./scripts/csv-to-readme.py \
  data/general-concepts.hxl.csv \
  --line-formatter='==== {raw_line[1]}\n`{raw_line}`\n' \
  >partials/general-concepts.adoc

./scripts/csv-to-readme.py \
  data/github-topics.hxl.csv \
  --line-formatter='==== {raw_line[1]}\n`{raw_line}`\n' \
  --line-select='{raw_line[0]}==1' \
  >partials/github-topics_1.adoc

./scripts/csv-to-readme.py \
  data/github-topics.hxl.csv \
  --line-formatter='==== {raw_line[1]}\n`{raw_line}`\n' \
  --line-select='{raw_line[0]}==2' \
  >partials/github-topics_2.adoc

./scripts/csv-to-readme.py \
  data/github-topics.hxl.csv \
  --line-formatter='==== {raw_line[1]}\n`{raw_line}`\n' \
  --line-select='{raw_line[0]}==3' \
  >partials/github-topics_3.adoc

./scripts/csv-to-readme.py \
  data/software.hxl.csv \
  --line-formatter='==== {raw_line[1]}\n`{raw_line}`\n' \
  >partials/software.adoc

asciidoctor --backend docbook README.source.adoc --out-file README.source.xml

# pandoc \
#   --read=docbook \
#   --write=markdown+smart \
#   --output=README-preview.md \
#   README.source.xml

pandoc \
  --read=docbook \
  --write=gfm \
  --output=README-preview.md \
  README.source.xml

set +x

# frictionless describe --json data/github-topics.hxl.csv
# frictionless describe --json data/general-concepts.hxl.csv
# frictionless describe --json data/software.hxl.csv

# frictionless validate datapackage.json

# @TODO - https://github.com/sindresorhus/awesome/issues/2242
#       - https://github.com/danielecook/Awesome-Bioinformatics/blob/master/.github/workflows/url-check.yml
#       - https://github.com/peter-evans/link-checker
