#!/usr/bin/python3
# ===============================================================================
#
#          FILE:  readme-from-csv.py
#                 scripts/readme-from-csv.py
#
#         USAGE:  ./scripts/readme-from-csv.py
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
#       VERSION:  v1.1
#       CREATED:  2022-08-31 05:09 UTC
#      REVISION:  2022-09-01 01:27 UTC csv-to-readme.py -> readme-from-csv.py
# ===============================================================================

import glob
import os
import argparse
import csv
from genericpath import exists
import re
import sys
from typing import List
from ast import literal_eval

DESCRIPTION = f"""
{__file__} provide some conventinent functions to convert tabular data
into output formats which could be used as partial for be injected into
README files. A common use case is generate READMEs for awesome-list.
"""

__EPILOGUM__ = f"""
------------------------------------------------------------------------------
                            EXEMPLŌRUM GRATIĀ
------------------------------------------------------------------------------
    {__file__} data/software.hxl.csv

    {__file__} data/software.hxl.csv --output-format='markdown'

    {__file__} --method=compile-readme README.template.md

Extract unique Wikidata Q items . . . . . . . . . . . . . . . . . . . . . . . .
    {__file__} --method=extract-wikidata-q 'data/*.csv'

Extract unique URLs, Except know patterns . . . . . . . . . . . . . . . . . . .
    {__file__} --method=extract-generic-url 'data/*.csv'

Extract unique URLs, Except know patterns . . . . . . . . . . . . . . . . . . .
    {__file__} --method=extract-generic-url 'data/*.csv'

------------------------------------------------------------------------------
                            EXEMPLŌRUM GRATIĀ
------------------------------------------------------------------------------
"""

STDIN = sys.stdin.buffer

cwd = os.getcwd()

ROOT_PATH = os.environ.get('ROOT_PATH', os.getcwd())

# print("todo")

# @TODO implement jekyll includes https://jekyllrb.com/docs/includes/


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
            # prog="999999999_826165",
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
            '--method',
            help='Method of operation. Defaults to process a table.',
            dest='method',
            nargs='?',
            choices=[
                'table-processing',
                'compile-readme',
                'extract-generic-url',
                'extract-github-url',
                'extract-github-topic-url',
                'extract-wikidata-q',
            ],
            required=False,
            default='table-processing'
        )

        parser_table = parser.add_argument_group(
            "table-processing",
            "Options exclusive to table processing")

        # https://stackoverflow.com/questions/54351740/how-can-i-use-f-string-with-a-variable-not-with-a-string-literal
        parser_table.add_argument(
            '--line-formatter',
            help='Line formatter (python f-string). Headers are converted'
            'to variables, and linear format is avalible as "raw_line"'
            'Default: "{raw_line}"',
            dest='line_formatter',
            nargs='?',
            # required=True
            default='{raw_line}'
        )

        # https://stackoverflow.com/questions/54351740/how-can-i-use-f-string-with-a-variable-not-with-a-string-literal
        parser_table.add_argument(
            '--line-select',
            help='Rule to evaluate line by line if result should be printed. '
            'Default: "{raw_line[0]}"',
            dest='line_select',
            nargs='?',
            # required=True
            default='{raw_line[0]}'
        )

        # https://stackoverflow.com/questions/54351740/how-can-i-use-f-string-with-a-variable-not-with-a-string-literal
        parser_table.add_argument(
            '--line-exclude',
            help='Rule to evaluate line by line if result should NOT be '
            'printed. Same rules as --line-select',
            dest='line_exclude',
            nargs='?',
            # required=True
            default=None
        )

        # https://stackoverflow.com/questions/54351740/how-can-i-use-f-string-with-a-variable-not-with-a-string-literal
        parser_table.add_argument(
            '--output-sort',
            help='Name of columns to use for sort the output. '
            'Use "|" to specify more than one.',
            dest='output_sort',
            nargs='?',
            # required=True
            type=lambda x: x.split('|'),
            default=None
        )

        parser_table.add_argument(
            '--output-group-prefix',
            help='Content to add before generating any line output',
            dest='group_prefix',
            nargs='?',
            # required=True
            default=None
        )

        parser_table.add_argument(
            '--output-group-suffix',
            help='Content to add after all lines are outputed',
            dest='group_suffix',
            nargs='?',
            # required=True
            default=None
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

        if not _infile and not _stdin:
            print('ERROR! Try:')
            print(f'    {__file__} --help')
            return self.EXIT_ERROR

        if pyargs.method == 'table-processing':
            csv2r = CSVtoReadme(
                _infile,
                pyargs.line_formatter,
                pyargs.line_select,
                pyargs.line_exclude,
                pyargs.group_prefix,
                pyargs.group_suffix,
                pyargs.output_sort,
                pyargs.input_delimiter,
                # pyargs.output_format,
            )

            csv2r.prepare()
            return csv2r.print()

        if pyargs.method == 'compile-readme':
            csv2r = CompileReadme(
                _infile,
            )

            csv2r.prepare()
            return csv2r.print()

        if pyargs.method in [
            'extract-url',
            'extract-generic-url',
            'extract-github-url',
            'extract-github-topic-url',
            'extract-wikidata-q',
        ]:
            edff = ExtractDataFromFiles(
                _infile,
                mode=pyargs.method
            )

            edff.prepare()
            return edff.print()

        # # go = owlready2.get_ontology("http://purl.obolibrary.org/obo/go.owl").load()
        # # obo = owlready2.get_namespace("http://purl.obolibrary.org/obo/")
        # # print(obo.GO_0000001.label)
        # print("TODO")

        # return self.EXIT_OK

        print(f'Unknow option. [{pyargs.method}]')
        return self.EXIT_ERROR


class CompileReadme:
    """ Parse a README file and import partials

    Syntaxes allowed:
        - {% include_relative somedir/footer.html %}
            - https://jekyllrb.com/docs/includes/

    """

    data_template: List[list] = []
    data_compiled: List[list] = []
    _base = ROOT_PATH

    def __init__(
        self, infile,
    ):
        self.infile = infile

    def _load_file(self, file, strict: bool = True) -> List[list]:

        if not exists(file):
            if not strict:
                return None
            else:
                raise IOError(f'[{file} not found]')

        with open(file, 'r') as _file:
            # self.data_template = _file.readlines()
            lines = _file.read().splitlines()
            return lines

    def _get_import(self, line) -> str:
        if not line or len(line.strip()) == 0:
            return None
        if line.find('{% include_relative') == -1:
            return None

        rule_1 = r'.*{% include_relative (.*) %}.*'
        rule_1_result = re.match(rule_1, line)
        if rule_1_result and rule_1_result.group(1):
            file_path = rule_1_result.group(1)
            from pathlib import Path
            filename = Path(file_path).resolve()
            # raise NotImplementedError(filename)
            return filename

    def prepare(self):
        self.data_template = self._load_file(self.infile)
        for line in self.data_template:
            import_file = self._get_import(line)
            if import_file:
                extra_lines = self._load_file(import_file, strict=False)
                if extra_lines:
                    # self.data_compiled.append("IMPORTED: ")
                    self.data_compiled.extend(extra_lines)
                else:
                    self.data_compiled.append("IMPORT ERROR START")
                    self.data_compiled.append(line)
                    self.data_compiled.append("IMPORT ERROR END")
            else:
                self.data_compiled.append(line)

    def print(self):
        # for line in self.data_template:
        #     print(line)
        for line in self.data_compiled:
            print(line)


class CSVtoReadme:

    data_lines: List[list] = None
    # data_dict: List[list] = None

    def __init__(
        self, infile,
        line_formatter,
        line_select,
        line_exclude,
        group_prefix: str = None,
        group_suffix: str = None,
        output_sort: list = None,
        input_delimiter=','
    ):
        """
        Constructs all the necessary attributes for the Cli object.
        """
        self.infile = infile
        self.line_formatter = line_formatter
        self.line_select = line_select
        self.line_exclude = line_exclude
        self.group_prefix = group_prefix
        self.group_suffix = group_suffix
        self.output_sort = output_sort
        self.input_delimiter = input_delimiter
        # self.output_format = output_format

    def _get_url(self, line):
        for item in reversed(line):
            if item.startswith(('http://', 'https://')):
                return item
        return ''

    def _prepare_filter(self):

        _data_new = []
        header = []
        line_select = None
        line_exclude = None
        new_data = []
        for line in self.data_lines:
            # print('loop')
            if len(header) == 0:
                header = line
                new_data.append(header)
                continue

            line_variables = dict(zip(header, line))
            # print('oi', self.line_select, line)
            line_variables['raw_line'] = line
            if self.line_select is not None:
                parsed_line_select = self.line_select.format(**line_variables)
                # print('parsed_line_select', parsed_line_select)
                evaluated_line_select = evaluate(parsed_line_select)
                # print('result_line_select', result_line_select)
                if not evaluated_line_select:
                    continue

            if self.line_exclude is not None:
                parsed_line_exclude = self.line_exclude.format(
                    **line_variables)
                evaluated_line_exclude = evaluate(parsed_line_exclude)
                if evaluated_line_exclude:
                    continue

            new_data.append(line)

        self.data_lines = new_data

    def _prepare_sort(self):

        _data_new = []
        header = []
        line_select = None
        line_exclude = None
        new_data = []
        for line in self.data_lines:
            # print('loop')
            if len(header) == 0:
                header = line
                new_data.append(header)
                continue

            line_variables = dict(zip(header, line))
            # print('oi', self.line_select, line)
            line_variables['raw_line'] = line
            if self.line_select is not None:
                parsed_line_select = self.line_select.format(**line_variables)
                # print('parsed_line_select', parsed_line_select)
                evaluated_line_select = evaluate(parsed_line_select)
                # print('result_line_select', result_line_select)
                if not evaluated_line_select:
                    continue

            if self.line_exclude is not None:
                parsed_line_exclude = self.line_exclude.format(
                    **line_variables)
                evaluated_line_exclude = evaluate(parsed_line_exclude)
                if evaluated_line_exclude:
                    continue

            new_data.append(line)

        self.data_lines = new_data

    def prepare(self):
        with open(self.infile) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=self.input_delimiter)
            csv_dictreader = csv.reader(
                csv_file, delimiter=self.input_delimiter)
            # line_count = 0
            self.data_lines = []
            self.data_dict = []

            for row in csv_reader:
                self.data_lines.append(row)

            # for row in csv_dictreader:
            #     self.data_dict.append(row)

        if self.line_select or self.line_exclude:
            self._prepare_filter()

        if self.output_sort:
            raise NotImplementedError('TODO output_sort')

    def print(self):

        # print("TODO print")
        # print(self.data)
        # print('')
        index = -1
        header = []

        if self.group_prefix:
            print(self.group_prefix)

        for line in self.data_lines:
            index += 1
            if index == 0:
                header = line
                continue

            url = self._get_url(line)
            headline = line[0]
            summary = line[1]

            line_variables = dict(zip(header, line))
            line_variables['raw_line'] = line

            print(self.line_formatter.format(
                **line_variables).replace('\\n', "\n"))

        if self.group_suffix:
            print(self.group_suffix)


class ExtractDataFromFiles:

    data_template: List[list] = []
    data_compiled: List[list] = []
    mode: str = None
    data_mined = List = []
    _base = ROOT_PATH

    know_modes = {
        'extract-url': r'(https?://[www\.]?\S+)',
        'extract-generic-url': r'(https?://[www\.]?[^github]\S+)',
        'extract-github-url':
        r'(https?://[www\.]?(github\.com/)(?!topics/)\S+)',
        'extract-github-topic-url':
        r'(https?://[www\.]?(github\.com/)(topics/)\S+)',
        # This needs more testing
        'extract-wikidata-q': r'(Q[1-9]\S+)',
    }

    def __init__(
        self, file_pattern,
        mode: str = 'extract-generic-url',
        regex: str = None,
    ):
        self.file_pattern = file_pattern
        self.mode = mode

        if not regex:
            self.regex = self.know_modes[mode]
        else:
            self.regex = regex

    def _load_file(self, file, strict: bool = True) -> List:
        delimiters = {
            '.csv': ',',
            '.tsv': "\t",
            '.tab': "\t"
        }

        if not exists(file):
            if not strict:
                return None
            else:
                raise IOError(f'[{file} not found]')

        # If is tabular, this clean up delimiters
        if file.endswith(tuple(delimiters.keys())):
            # raise NotImplementedError('todo')
            items = set()
            with open(file, 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                for row in spamreader:
                    [items.add(item) for item in row]
            return items

        with open(file, 'r') as _file:
            lines = set(_file.read().splitlines())
            return lines

    def prepare(self):
        _data_mined = set()
        for name in glob.glob(self.file_pattern):
            # print(name)
            file_now = self._load_file(name)
            for line in file_now:
                results = re.findall(self.regex, line)
                if results:
                    for item in results:
                        if not isinstance(item, str):
                            item = item[0]
                        _data_mined.add(item)
        self.data_mined = sorted(_data_mined)

    def print(self):
        # for line in self.data_template:
        #     print(line)
        for line in self.data_mined:
            print(line)
            pass


def evaluate(textoperation: str) -> bool:
    """evaluate evaluate simple text operations like "1==2"

    As 2022-08-31, the ast.literal_eval have no know security issues.
    Actually, is very simple, only convert like "None" to None, so
    it cant access complex functions. But is know that ast.literal_eval with
    large string could crash the interpreter.

    Args:
        textoperation (str): An unary or simple 2 clause operation

    Returns:
        bool: True or False result
    """
    # print('evaluate', textoperation)
    # print('evaluate2', literal_eval("\"Q5282121\""))
    operations = {
        '==': lambda a, b: a == b,
        '>=': lambda a, b: a >= b,
        '>': lambda a, b: a <= b,
        '<=': lambda a, b: a <= b,
        '<': lambda a, b: a <= b,
    }

    if not textoperation or len(textoperation.strip()) == 0:
        return False

    textoperation = textoperation.strip()
    op_func = None
    var_a = None
    var_b = None

    def _literal_eval(textitem):
        # Avoid "ValueError: malformed node or string:" errors for strings
        # without ' or "
        if not textitem.startswith(('"', "'")) and \
            isinstance(textitem[0], str) and \
                textitem not in ['True', 'False', 'None']:
            textitem = f'"{textitem}"'
        return literal_eval(textitem)

    for op in operations.keys():
        if textoperation.find(op) > -1:
            op_func = operations[op]
            var_a, var_b = textoperation.split(op)
            var_a = _literal_eval(var_a)
            var_b = _literal_eval(var_b)
    if not op_func:
        # No function, Let's assume it's a literal
        return bool(_literal_eval(textoperation))
    return op_func(var_a, var_b)


if __name__ == "__main__":

    est_cli = Cli()
    args = est_cli.make_args()

    est_cli.execute_cli(args)
