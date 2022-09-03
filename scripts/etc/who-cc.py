#!/usr/bin/python3
# ===============================================================================
#
#          FILE:  who-cc.py
#                 scripts/etc/who-cc.py
#
#         USAGE:  ./scripts/etc/who-cc.py
#
#   DESCRIPTION:  ---
#
#       OPTIONS:  ---
#
#  REQUIREMENTS:  - python3
#                   - requests-html
#          BUGS:  ---
#         NOTES:  ---
#        AUTHOR:  Emerson Rocha <rocha[at]ieee.org>
#       COMPANY:  EticaAI
#       LICENSE:  Public Domain dedication
#                 SPDX-License-Identifier: Unlicense
#       VERSION:  v1.0
#       CREATED:  2022-09-03 06:53 UTC
#      REVISION:  ---
# ===============================================================================

import argparse
import os
import sys

from requests_html import HTMLSession

DESCRIPTION = f"""
{__file__} provide some conventinent functions to convert tabular data
into output formats which could be used as partial for be injected into
README files. A common use case is generate READMEs for awesome-list.

The template engine uses Mustache https://mustache.github.io/ \
(Demo here https://mustache.github.io/#demo)
"""

__EPILOGUM__ = f"""
------------------------------------------------------------------------------
                            EXEMPLŌRUM GRATIĀ
------------------------------------------------------------------------------
    {__file__} data/software.hxl.csv

    {__file__} --method=compile-readme README.template.md

Extract unique Wikidata Q items . . . . . . . . . . . . . . . . . . . . . . . .
    {__file__} --method=extract-wikidata-q 'data/*.csv'

Extract unique URLs, Except know patterns . . . . . . . . . . . . . . . . . . .
    {__file__} --method=extract-generic-url 'data/*.csv'

Extract unique URLs, Except know patterns . . . . . . . . . . . . . . . . . . .
    {__file__} --method=extract-generic-url 'data/*.csv'

Merge data files in memory before render templated result . . . . . . . . . . .

    {__file__} data/software.hxl.csv \
--data-merge-file-2='partials/raw/github-projects.tsv' \
--data-merge-key-2='#item+repository+url' \
--data-merge-foreignkey-2='repo'

------------------------------------------------------------------------------
                            EXEMPLŌRUM GRATIĀ
------------------------------------------------------------------------------
"""

STDIN = sys.stdin.buffer


class Cli:

    EXIT_OK = 0
    EXIT_ERROR = 1
    EXIT_SYNTAX = 2

    def __init__(self):
        """
        Constructs all the necessary attributes for the Cli object.
        """

    def make_args(self, hxl_output=True):
        # parser = argparse.ArgumentParser(description=DESCRIPTION)
        parser = argparse.ArgumentParser(
            # prog="999999999_826165",
            description=DESCRIPTION,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=__EPILOGUM__
        )

        # parser.add_argument(
        #     'infile',
        #     help='Input file',
        #     # required=True,
        #     nargs='?'
        # )

        # parser.add_argument(
        #     '--input-delimiter',
        #     help='Input delimiter. Defaults to ","',
        #     dest='input_delimiter',
        #     nargs='?',
        #     # required=True
        #     default=','
        # )

        parser.add_argument(
            '--method',
            help='Method of operation.',
            dest='method',
            nargs='?',
            choices=[
                'fetch-crappy-csv',
            ],
            required=False,
            default='fetch-crappy-csv'
        )

        parser.add_argument(
            # '--venandum-insectum-est, --debug',
            '--debug',
            help='Enable debug',
            metavar="debug",
            dest="debug",
            action='store_const',
            const=True,
            default=False
        )

        return parser.parse_args()

    def execute_cli(self, pyargs, stdin=STDIN, stdout=sys.stdout,
                    stderr=sys.stderr):
        # self.pyargs = pyargs

        # if stdin.isatty():
        #     _infile = pyargs.infile
        #     _stdin = False
        # else:
        #     _infile = None
        #     _stdin = True

        # if not _infile and not _stdin:
        #     print('ERROR! Try:')
        #     print(f'    {__file__} --help')
        #     return self.EXIT_ERROR

        if pyargs.method == 'fetch-crappy-csv':
            whocc = WHOCC(
                # pyargs.output_format,
            )

            whocc.prepare()
            return whocc.print()

        # return self.EXIT_OK

        print(f'Unknow option. [{pyargs.method}]')
        return self.EXIT_ERROR


class WHOCC:

    session: HTMLSession
    r_search = None

    _search_selector: str = '#ctl00_ContentPlaceHolder1_DropDownList1'

    def __init__(self) -> None:
        self.session = HTMLSession()

    def prepare(self):
        self.r_search = self.session.get(
            'https://apps.who.int/whocc/Search.aspx')

        print(self.r_search.html.links)
        print(self.r_search.html)
        print(self.r_search)

        selector = self.r_search.find(self._search_selector)

        # cc_region

    def print(self):
        pass
