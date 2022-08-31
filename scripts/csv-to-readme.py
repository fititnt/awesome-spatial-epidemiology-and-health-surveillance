#!/usr/bin/python3
# ===============================================================================
#
#          FILE:  csv-to-readme.py
#                 scripts/csv-to-readme.py
#
#         USAGE:  ./scripts/csv-to-readme.py
#
#   DESCRIPTION:  ---
#
#       OPTIONS:  ---
#
#  REQUIREMENTS:  - python3
#          BUGS:  ---
#         NOTES:  ---
#        AUTHOR:  Emerson Rocha <rocha[at]ieee.org>
#       COMPANY:  EticaAI
#       LICENSE:  Public Domain dedication
#                 SPDX-License-Identifier: Unlicense
#       VERSION:  v1.0
#       CREATED:  2022-08-31 05:09 UTC
#      REVISION:  ---
# ===============================================================================


import argparse
import csv
import sys
from typing import List

DESCRIPTION = f"""
{__file__} Draft!
"""

__EPILOGUM__ = f"""
------------------------------------------------------------------------------
                            EXEMPLŌRUM GRATIĀ
------------------------------------------------------------------------------
    {__file__} data/software.hxl.csv

    {__file__} data/software.hxl.csv --output-format='markdown'
------------------------------------------------------------------------------
                            EXEMPLŌRUM GRATIĀ
------------------------------------------------------------------------------
"""

STDIN = sys.stdin.buffer

print("todo")


class Cli:

    EXIT_OK = 0
    EXIT_ERROR = 1
    EXIT_SYNTAX = 2

    venandum_insectum: bool = False  # noqa: E701

    def __init__(self):
        """
        Constructs all the necessary attributes for the Cli object.
        """

    def make_args(self, hxl_output=True):
        # parser = argparse.ArgumentParser(description=DESCRIPTION)
        parser = argparse.ArgumentParser(
            prog="999999999_826165",
            description=DESCRIPTION,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=__EPILOGUM__
        )

        parser.add_argument(
            'infile',
            help='Input file',
            # required=True,
            nargs='?'
        )

        parser.add_argument(
            '--input-delimiter',
            help='Input delimiter. Defaults to ","',
            dest='input_delimiter',
            nargs='?',
            # required=True
            default=','
        )
        parser.add_argument(
            '--output-format',
            help='Output format',
            dest='output_format',
            nargs='?',
            choices=[
                'markdown',
                'asciidoctor',
                # 'data-apothecae',
                # 'hxltm-explanationi',
                # 'opus-temporibus',
                # 'status-quo',
                # 'deprecatum-dictionaria-numerordinatio'
            ],
            # required=True
            default='markdown'
        )

        parser.add_argument(
            # '--venandum-insectum-est, --debug',
            '--debug',
            help='Enable debug',
            metavar="venandum_insectum",
            dest="venandum_insectum",
            action='store_const',
            const=True,
            default=False
        )

        # parser.add_argument(
        #     'outfile',
        #     help='Output file',
        #     nargs='?'
        # )

        return parser.parse_args()

    def execute_cli(self, pyargs, stdin=STDIN, stdout=sys.stdout,
                    stderr=sys.stderr):
        # self.pyargs = pyargs

        if stdin.isatty():
            _infile = pyargs.infile
            _stdin = False
        else:
            _infile = None
            _stdin = True

        csv2r = CSVtoReadme(
            _infile,
            pyargs.input_delimiter,
            pyargs.output_format,
        )

        csv2r.prepare()
        return csv2r.print()

        # go = owlready2.get_ontology("http://purl.obolibrary.org/obo/go.owl").load()
        # obo = owlready2.get_namespace("http://purl.obolibrary.org/obo/")
        # print(obo.GO_0000001.label)
        print("TODO")

        return self.EXIT_OK

        print('Unknow option.')
        return self.EXIT_ERROR


class CSVtoReadme:

    data: List[list] = None

    def __init__(
        self, infile, input_delimiter=',', output_format='asciidoctor'
    ):
        """
        Constructs all the necessary attributes for the Cli object.
        """
        self.infile = infile
        self.input_delimiter = input_delimiter
        self.output_format = output_format

    def _get_url(self, line):
        for item in reversed(line):
            if item.startswith(('http://', 'https://')):
                return item
        return ''

    def prepare(self):
        with open(self.infile) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=self.input_delimiter)
            line_count = 0
            self.data = []
            for row in csv_reader:
                self.data.append(row)
            #     if line_count == 0:
            #         print(f'Column names are {", ".join(row)}')
            #         line_count += 1
            #     else:
            #         print(
            #             f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
            #         line_count += 1
            # print(f'Processed {line_count} lines.')

    def print(self):

        print("TODO print")
        print(self.data)
        print('')
        index = -1
        for line in self.data:
            index += 1
            if index == 0:
                continue

            url = self._get_url(line)
            headline = line[0]
            summary = line[1]
            print(f'- [**{headline}** - {summary}]({url})')

        print('print end')
        # pass


if __name__ == "__main__":

    est_cli = Cli()
    args = est_cli.make_args()

    est_cli.execute_cli(args)
