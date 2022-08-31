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