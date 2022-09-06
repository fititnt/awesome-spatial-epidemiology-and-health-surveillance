#!/usr/bin/python3
# ===============================================================================
#
#          FILE:  readme-from-csv.py
#                 scripts/readme-from-csv.py
#
#         USAGE:  ./scripts/readme-from-csv.py --help
#                 python ./scripts/readme-from-csv.py --help
#                 python3 ./scripts/readme-from-csv.py --help
#
#   DESCRIPTION:  ---
#
#       OPTIONS:  ---
#
#  REQUIREMENTS:  - python3
#                   - pyyaml
#                   - python-liquid
#                   - python-liquid-extra
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


import yaml
import fnmatch
import glob
import os
import argparse
import csv
from genericpath import exists
import re
import sys
from typing import List, Type
from ast import literal_eval

# from liquid import Template
# from liquid import FileSystemLoader
from liquid import StrictDefaultUndefined
from liquid import Mode
from liquid_extra import filters
from liquid import Environment
from liquid_extra.filters import Translate

# import pystache
# import chevron

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

COMPILE FINAL README ==========================================================
Simple, read file, apply generic liquid templating . . . . . . . . . . . . . . .
    {__file__} --method=compile-readme README.template.md

Internationalization, read variables from i18n/locales . . . . . . . . . . . . .
    {__file__} --method=compile-readme README.template.md \
--natural-language-objective=en

PROCESS / RE-PROCESS CSVs =====================================================

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

Rename CSV/Tabular data header . . . . . . . . . . . . . . . . . . . . . . . .
    {__file__} --method=table-rename \
--table-meta=i18n/zxx/who-collaborating-centres.meta.yml \
partials/temp/whocc.csv


------------------------------------------------------------------------------
                            EXEMPLŌRUM GRATIĀ
------------------------------------------------------------------------------
"""

STDIN = sys.stdin.buffer

cwd = os.getcwd()

ROOT_PATH = os.environ.get('ROOT_PATH', os.getcwd())

# print("todo")

# @TODO use mustache as template engine http://mustache.github.io/
#       - https://github.com/PennyDreadfulMTG/pystache/
#       - https://github.com/noahmorrison/chevron
#       - https://pypi.org/project/pystache/


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
                'table-rename',
                'compile-readme',
                'extract-generic-url',
                'extract-github-url',
                'extract-github-topic-url',
                'extract-wikidata-q',
                'extract-remote-html-table',
            ],
            required=False,
            default='table-processing'
        )

        parser.add_argument(
            '--natural-language-objective',
            help='BCP47 code (such as "ar", for Arabic) for objetive '
            'natural language',
            dest='bcp47_objetive',
            nargs='?',
            default=None
        )

        parser.add_argument(
            '--natural-language-fallback',
            help='BCP47 code (such as "la", for Latin) for fallback '
            'natural language',
            dest='bcp47_fallback',
            nargs='?',
            default=None
        )

        parser_table = parser.add_argument_group(
            "table-processing",
            "Options exclusive to table processing")

        # https://stackoverflow.com/questions/54351740/how-can-i-use-f-string-with-a-variable-not-with-a-string-literal
        parser_table.add_argument(
            '--line-formatter',
            help='Line formatter using mustache formatter.'
            'Headers are converted to variables, and linear format is '
            'avalible as "raw_line"'
            'Default: "{{.}}" (print every option)',
            dest='line_formatter',
            nargs='?',
            # required=True
            # default='{{.}}'
            default=None
        )

        # parser_table.add_argument(
        #     '--line-formatter-mustache',
        #     help='Line formatter (python f-string). Headers are converted'
        #     'to variables, and linear format is avalible as "raw_line"'
        #     'Default: "{raw_line}"',
        #     dest='line_formatter_mustache',
        #     nargs='?',
        #     # required=True
        #     default='{raw_line}'
        #     # default=None
        # )

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

        parser_table.add_argument(
            '--data-merge-file-2',
            help='Path to a file to merge additiona columns with the main file',
            dest='merge_file_2',
            nargs='?',
            # required=True
            default=None
        )

        parser_table.add_argument(
            '--data-merge-key-2',
            help='When --data-merge-file-2 is used, this allow explicity '
            'say which is reference key to search on main table.',
            dest='merge_key_2',
            nargs='?',
            # required=True
            default=None
        )

        parser_table.add_argument(
            '--data-merge-foreignkey-2',
            help='When --data-merge-file-2 is used, this allow explicity '
            'say which is reference foreign key to search on the merged'
            'table.',
            dest='merge_foreignkey_2',
            nargs='?',
            # required=True
            default=None
        )

        parser_pivot = parser.add_argument_group(
            "table-pivot",
            "Options exclusive to table renaming")

        parser_pivot.add_argument(
            '--table-meta',
            help='With --method=table-rename this explain which file '
            'contains the metadata for conversion between formats. '
            'Example: "i18n/zxx/who-collaborating-centres.meta.yml"',
            dest='table_meta',
            nargs='?',
            # required=True
            default=None
        )

        parser_pivot.add_argument(
            '--table-objective',
            help='With --method=table-rename this define the target '
            'format',
            dest='table_objective',
            nargs='?',
            choices=[
                'csv',
                'csvnorm',
                'hxl',
            ],
            required=False,
            default='hxl'
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

        parser.add_argument(
            '--strictness-level',
            help='Strictness level',
            dest='strictness_level',
            nargs='?',
            choices=[
                -1,
                0,
                1,
                2,
            ],
            required=False,
            # default=0,
            # type=int
            default=0,
            type=int
        )

        parser.add_argument(
            '--logfile',
            help='Path to a logfile. Defaults to .errors.log on current dir',
            dest='logfile',
            nargs='?',
            default='.errors.log'
        )

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
                pyargs.merge_file_2,
                pyargs.merge_key_2,
                pyargs.merge_foreignkey_2,
                pyargs.input_delimiter,
                bcp47_objetive=pyargs.bcp47_objetive,
                bcp47_fallback=pyargs.bcp47_fallback,
                strictness_level=pyargs.strictness_level,
                verbose=pyargs.debug,
                # pyargs.output_format,
            )

            csv2r.prepare()
            return csv2r.print()

        if pyargs.method == 'table-rename':
            if not pyargs.table_meta:
                raise SyntaxError('--table-meta option is required')

            with open(pyargs.table_meta) as _file:
                meta = yaml.load(_file, Loader=yaml.SafeLoader)
                # return data

            # raise ValueError(meta)
            csvrename = CSVRename(
                _infile,
                meta,
                pyargs.table_objective,
                skip_unknown=True
                # pyargs.output_format,
            )

            csvrename.prepare()
            return csvrename.print()

        if pyargs.method == 'compile-readme':
            csv2r = CompileReadme(
                _infile,
                bcp47_objetive=pyargs.bcp47_objetive,
                bcp47_fallback=pyargs.bcp47_fallback,
                strictness_level=pyargs.strictness_level,
                verbose=pyargs.debug,
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

        if pyargs.method in [
            'extract-remote-html-table',
        ]:

            PANDAS_READ_HTML__INDEXTABLE = \
                os.environ.get('PANDAS_READ_HTML__INDEXTABLE', '')

            # match
            PANDAS_READ_HTML__MATCH = \
                os.environ.get('PANDAS_READ_HTML__MATCH', '')

            # table_index = 0
            # @see https://pbpython.com/pandas-html-table.html
            from unicodedata import normalize
            import pandas as pd

            def clean_normalize_whitespace(x):
                if isinstance(x, str):
                    return normalize('NFKC', x).strip()
                else:
                    return x

            if PANDAS_READ_HTML__MATCH:
                tables_html = pd.read_html(
                    _infile,
                    match=PANDAS_READ_HTML__MATCH)
            else:
                tables_html = pd.read_html(_infile)
            if not PANDAS_READ_HTML__INDEXTABLE:
                # No option specified, print all
                loop_now = -1
                for df in tables_html:
                    loop_now += 1
                    if len(tables_html) > 1:
                        print(f'=============== TABLE {loop_now}/' +
                              f'{len(tables_html)} ===============')

                    df = df.applymap(clean_normalize_whitespace)
                    print(df.to_csv(index=False))
            else:
                the_index = int(PANDAS_READ_HTML__INDEXTABLE)
                df = tables_html[the_index]
                df = df.applymap(clean_normalize_whitespace)
                print(df.to_csv(index=False).strip())

            return self.EXIT_ERROR

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
    liquid: Type['LiquidRenderer'] = None
    _base = ROOT_PATH

    def __init__(
        self,
        infile,
        bcp47_objetive: str = 'en',
        bcp47_fallback: str = 'en',
        strictness_level: int = 0,
        verbose: bool = False
    ):
        self.infile = infile
        self.bcp47_objetive = bcp47_objetive
        self.bcp47_fallback = bcp47_fallback
        self.verbose = verbose

        self.liquid = LiquidRenderer(
            bcp47_objetive=self.bcp47_objetive,
            bcp47_fallback=self.bcp47_fallback,
            strictness_level=strictness_level,
        )

    def _load_file(self, file, strict: bool = True) -> List[list]:

        if not exists(file):
            if not strict:
                return False
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
                elif extra_lines is not False:
                    # This means file exist, but empty
                    if self.verbose:
                        self.data_compiled.append(
                            f'<!-- Empty file {line} -->')
                else:
                    self.data_compiled.append("IMPORT ERROR START")
                    self.data_compiled.append(line)
                    self.data_compiled.append("IMPORT ERROR END")
            else:
                self.data_compiled.append(line)

    def print(self):
        # for line in self.data_template:
        #     print(line)
        template_string = "\n".join(self.data_compiled)
        print(self.liquid.render(
            template_string
        ).replace('\\n', "\n"))
        # for line in self.data_compiled:
        #     print(line)


class CSVtoReadme:

    data_lines: List[list] = None
    # data_dict: List[list] = None

    liquid: Type['LiquidRenderer'] = None

    def __init__(
        self, infile,
        line_formatter,
        line_select,
        line_exclude,
        group_prefix: str = None,
        group_suffix: str = None,
        output_sort: list = None,
        merge_file_2: str = None,
        merge_key_2: str = None,
        merge_foreignkey_2: str = None,
        input_delimiter=',',
        bcp47_objetive=None,
        bcp47_fallback=None,
        strictness_level: int = 0,
        verbose: bool = False
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
        self.merge_file_2 = merge_file_2
        self.merge_key_2 = merge_key_2
        self.merge_foreignkey_2 = merge_foreignkey_2
        self.input_delimiter = input_delimiter
        # self.output_format = output_format

        self.liquid = LiquidRenderer(
            bcp47_objetive=bcp47_objetive,
            bcp47_fallback=bcp47_fallback,
            strictness_level=strictness_level,
        )

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
            line_variables['raw_line'] = list(line)
            if self.line_select is not None:
                parsed_line_select = self.line_select.format(**line_variables)
                # print('parsed_line_select', parsed_line_select)
                # parsed_line_select = chevron.render(
                #     self.line_select,
                #     line_variables)
                parsed_line_select = self.liquid.render(
                    self.line_select,
                    line_variables
                )
                evaluated_line_select = evaluate(parsed_line_select)
                # print('result_line_select', result_line_select)
                if not evaluated_line_select:
                    continue

            if self.line_exclude is not None:
                parsed_line_exclude = self.line_exclude.format(
                    **line_variables)
                # parsed_line_exclude = chevron.render(
                #     self.line_exclude,
                #     line_variables)
                parsed_line_exclude = self.liquid.render(
                    self.line_exclude,
                    line_variables
                )
                evaluated_line_exclude = evaluate(parsed_line_exclude)
                if evaluated_line_exclude:
                    continue

            new_data.append(line)

        self.data_lines = new_data

    def _prepare_sort(self):
        raise NotImplementedError('@TODO _prepare_sort')

    def prepare(self):

        # Loading main file
        with open(self.infile) as csv_file:
            dialect = csv.Sniffer().sniff(csv_file.read(16384))
            csv_file.seek(0)
            csv_reader = csv.reader(csv_file, dialect)
            self.data_lines = []
            self.data_dict = []

            for row in csv_reader:
                self.data_lines.append(row)

        if self.line_select or self.line_exclude:
            self._prepare_filter()

        if self.output_sort:
            raise NotImplementedError('TODO output_sort')

        # @TODO maybe create an autodetect
        key_2 = self.merge_key_2
        foreignkey_2 = self.merge_foreignkey_2

        if self.merge_file_2:
            main_dict = []
            original_header = []
            for line in self.data_lines:
                if len(original_header) == 0:
                    original_header = line
                    continue
                main_dict.append(dict(zip(original_header, line)))

            merge_2_dict = {}
            with open(self.merge_file_2) as csv_file22:
                dialect = csv.Sniffer().sniff(csv_file22.read(16384))
                csv_file22.seek(0)
                # print('self.merge_file_2', self.merge_file_2)
                csv_dicreader = csv.DictReader(csv_file22, dialect=dialect)
                for merge_line in csv_dicreader:
                    # print('merge_line', merge_line)
                    merge_2_dict[merge_line[foreignkey_2]] = merge_line

            # print('merge_2_dict.keys()', merge_2_dict.keys())
            _keys = list(merge_2_dict.keys())[0]
            not_found_dict = dict(
                zip(_keys, [''] * len(_keys)))

            # now we try to merge
            new_main = []
            for main_line in main_dict:
                if main_line[key_2] in merge_2_dict:
                    merged_item_now = {**main_line,
                                       **merge_2_dict[main_line[key_2]]}
                else:
                    merged_item_now = {**main_line,
                                       **not_found_dict}

                if len(new_main) == 0:
                    new_main.append(merged_item_now.keys())

                new_main.append(merged_item_now.values())

            self.data_lines = new_main
        # Load merge 2 file (if any)

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

            # url = self._get_url(line)
            # headline = line[0]
            # summary = line[1]

            line_variables = dict(zip(header, line))
            line_variables['raw_line'] = list(line)

            # print(self.line_formatter.format(
            #     **line_variables).replace('\\n', "\n"))
            # print(chevron.render(
            #     self.line_formatter,
            #     line_variables).replace('\\n', "\n"))

            print(self.liquid.render(
                self.line_formatter,
                line_variables
            ).replace('\\n', "\n"))

        if self.group_suffix:
            print(self.group_suffix)


class CSVRename:

    data: List[list] = None
    # data_dict: List[list] = None

    def __init__(
        self, infile,
        meta: dict,
        table_objective: str,
        # line_select,
        # line_exclude,
        # group_prefix: str = None,
        # group_suffix: str = None,
        # output_sort: list = None,
        # merge_file_2: str = None,
        # merge_key_2: str = None,
        # merge_foreignkey_2: str = None,
        # input_delimiter=',',
        # bcp47_objetive=None,
        # bcp47_fallback=None,
        # strictness_level: int = 0,
        # verbose: bool = False
        skip_unknown: bool = True
    ):
        self.infile = infile
        self.meta = meta
        self.table_objective = table_objective
        self.skip_unknown = skip_unknown
        self._index_keep = []

    def _prepare_header(self, header: list) -> list:
        new_header = []

        def _helper(item):
            _ordering = -1
            for _key, metaitem in self.meta.items():
                _ordering += 1
                if item in metaitem.values():
                    if self.table_objective in metaitem and \
                            metaitem[self.table_objective]:
                        # return metaitem
                        return metaitem[self.table_objective], _ordering
            return None, None

        _index_keep_with_order = []
        for index, item in enumerate(header):
            metaitem_newheader, _ordering = _helper(item)
            # print('aa', index, item)
            if metaitem_newheader:
                # self._index_keep.append(index)
                _index_keep_with_order.append(
                    (_ordering, index, metaitem_newheader))
                # new_header.append(metaitem_newheader)

        _index_keep_with_order = sorted(_index_keep_with_order, reverse=False)
        # sorted(_index_keep_with_order, reverse=False)
        # print('_index_keep_with_order', _index_keep_with_order)
        for item_and_order in _index_keep_with_order:
            self._index_keep.append(item_and_order[1])
            new_header.append(item_and_order[2])
            # print(new_header[item_and_order[1]], item_and_order)
        # print('new_header', new_header)
        # print('self._index_keep', self._index_keep)
        return new_header

    def prepare(self):

        # Loading main file
        with open(self.infile) as csv_file:
            dialect = csv.Sniffer().sniff(csv_file.read(16384))
            csv_file.seek(0)
            csv_reader = csv.reader(csv_file, dialect)
            self.data = []
            # self.data_dict = []

            new_header = []
            for row in csv_reader:
                row_cleaned = []
                for item in row:
                    row_cleaned.append(item.strip())

                if len(new_header) == 0:
                    new_header = self._prepare_header(row_cleaned)
                    self.data.append(new_header)
                    # continue
                else:
                    row_cleaned_and_know = []
                    # print(self._index_keep)
                    for index in self._index_keep:
                        row_cleaned_and_know.append(row_cleaned[index])
                    self.data.append(row_cleaned_and_know)

    def print(self):
        csvwriter = csv.writer(sys.stdout)
        for line in self.data:
            # index += 1
            # print(line)
            csvwriter.writerow(line)


class DatafilesLoader:
    """ _summary_

    Allows mimic jekyll datafiles https://jekyllrb.com/docs/datafiles/
    """

    _site: dict = {}

    def __init__(
        self,
        base_paths: list = None,
        file_extensions: list = None,
        strictness_level: int = -1
    ) -> None:
        if not base_paths:
            base_paths = [
                'data',
                'i18n',
                'partials'
            ]

        self.base_paths = base_paths

        self.strictness_level = strictness_level

        if not file_extensions:
            # public/locales/{lng}/translation.json
            file_extensions = [
                'yml',
                'yaml',
                'json',
            ]
        self.file_extensions = tuple(file_extensions)

        self.load_all_from_disk()

    def get_data(self):
        return self._site

    def get_datapackage(self):
        if exists('datapackage.json'):
            datapackage = self.load_file('datapackage.json')
            # raise NotImplementedError(datapackage)
            # @TODO allow get by exact ID

            datapackage['id'] = {}
            for resource in datapackage['resources']:

                if 'id' in resource:
                    datapackage['id'][resource['id']] = resource
                else:
                    slug = resource['name'].lower().replace(
                        '-', '_').replace(r'\s', '_')

                    datapackage['id'][slug] = resource

            return datapackage
        # raise FileNotFoundError('datapackage.json')
        return {}

    def set_data(self, path: str, data_item: dict):
        # Example: i18n/zxx/biosafety-level-4-facilities.meta.yml

        base = path.split('.')[0].replace('-', '_')
        # Example: i18n/zxx/biosafety_level_4_facilities
        parts = base.split('/')

        if len(parts) > 4:
            raise NotImplementedError(
                f'Too deep ({len(parts)}). Change-me if you need more levels')

        # Maybe functools.reduce could be used here. But for now but verbose
        if len(parts) == 0:
            self._site = data_item
            return self._site
        if len(parts) == 1:
            self._site[parts[0]] = data_item
            return self._site

        if parts[0] not in self._site:
            self._site[parts[0]] = {}

        if len(parts) == 2:
            self._site[parts[0]][parts[1]] = data_item
            return self._site

        if parts[1] not in self._site[parts[0]]:
            self._site[parts[0]][parts[1]] = {}

        if len(parts) == 3:
            self._site[parts[0]][parts[1]][parts[2]] = data_item
            return self._site

        if parts[2] not in self._site[parts[0]][parts[1]]:
            self._site[parts[0]][parts[1]][parts[2]] = {}

        if len(parts) == 4:
            self._site[parts[0]][parts[1]][parts[2]][parts[3]] = data_item
            return self._site

    def load_all_from_disk(self):
        """load_all_from_disk load only files targeted for use now

        """
        # matches = []
        # current_lang = None
        # current_namespace = None
        for _base in self.base_paths:
            for root, _dirnames, filenames in os.walk(_base):
                for filename in fnmatch.filter(filenames, '*.*'):
                    root_parts = root.split('/')

                    if len(root_parts) > 4:
                        # For now, we only search up to 4 levels
                        continue

                    if not filename.endswith(self.file_extensions):
                        continue
                    path_now = os.path.join(root, filename)
                    loaded_data = self.load_file(path_now)

                    if loaded_data:
                        self.set_data(path_now, loaded_data)

    def load_file(self, file: str) -> dict:
        """load_file

        Args:
            file (str): path to file

        Returns:
            dict: return content of file as python dictionary
        """
        with open(file) as _file:
            data = yaml.load(_file, Loader=yaml.SafeLoader)
            return data


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
            with open(file, 'r') as csv_file:
                dialect = csv.Sniffer().sniff(csv_file.read(16384))
                csv_file.seek(0)
                csv_reader = csv.reader(csv_file, dialect)
                # spamreader = csv.reader(csvfile, delimiter=',')
                for row in csv_reader:
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

# @see https://shopify.github.io/liquid/
# @see https://jg-rp.github.io/liquid/
# @see https://jg-rp.github.io/liquid/extra/filters#t-translate


# template = Template("Hello, {{ you }}!")
# print(template.render(you="World"))  # Hello, World!
# print(template.render(you="Liquid"))  # Hello, Liquid!


# env = Environment()
# env.add_filter("json", filters.JSON())


class LiquidRenderer:
    """LiquidRenderer

    @see https://shopify.github.io/liquid/
    @see https://jg-rp.github.io/liquid/
    @see https://jg-rp.github.io/liquid/extra/filters#t-translate
    """

    env: Environment
    i18n_data: dict = None
    bcp47_objetive: str = None
    bcp47_fallback: str = None

    _site: dict = {}
    _datapackage: dict = {}

    def __init__(
        self,
        bcp47_objetive: str = 'en',
        bcp47_fallback: str = 'en',
        strictness_level: int = 0,
        verbose: bool = False
    ) -> None:

        self.bcp47_objetive = bcp47_objetive
        self.bcp47_fallback = bcp47_fallback
        # pass
        # self.env = Environment()
        # self.env.add_filter("json", filters.JSON())
        globals = {'locale': self.bcp47_objetive}
        self.env = Environment(
            tolerance=Mode.STRICT,
            # undefined=StrictDefaultUndefined,
            # loader=FileSystemLoader("./templates/"),
            globals=globals
        )
        self.env.add_filter("json", filters.JSON())
        tloader = TranslationLoader(
            bcp47_objetive=self.bcp47_objetive,
            bcp47_fallback=self.bcp47_fallback,
            strictness_level=strictness_level
        )
        self.i18n_data = tloader.get_data()
        # print('self.i18n_data ', self.i18n_data)

        dfloader = DatafilesLoader()

        self._site = dfloader.get_data()
        self._datapackage = dfloader.get_datapackage()

        # raise NotImplementedError

        self.env.add_filter(Translate.name, Translate(locales=self.i18n_data))

    def render(self, template: str = None, context: dict = None) -> str:
        if not context:
            context = {}

        if template is None or template is False:
            extra_context = {'current_context': context}
            compiled_template = self.env.from_string(
                '{{ current_context | json }}'
            )
        else:
            compiled_template = self.env.from_string(template)
            extra_context = context

        if 'locale' not in context:
            context['locale'] = self.bcp47_objetive

        extra_context['site'] = self._site
        extra_context['datapackage'] = self._datapackage

        # raise NotImplementedError(extra_context['datapackage'])

        result = compiled_template.render(extra_context)
        return result


class TranslationLoader:
    """ TranslationLoader abstract load translation files from disk into memory
    """

    data: dict = {
        'default': {
            'error': 'translations not loaded'
        }
    }

    def __init__(
        self,
        bcp47_objetive: str = 'pt',
        bcp47_fallback: str = 'en',
        base_namespace: str = 'translation',
        locales_base: list = None,
        file_extensions: list = None,
        strictness_level: int = -1
    ) -> None:

        self.bcp47_objetive = bcp47_objetive
        if bcp47_fallback:
            self.bcp47_fallback = bcp47_fallback
        else:
            self.bcp47_fallback = 'en'

        self.base_namespace = base_namespace
        self.strictness_level = strictness_level
        if not locales_base:
            # public/locales/{lng}/translation.json
            locales_base = [
                'i18n',
                'locales',
            ]
        if not file_extensions:
            # public/locales/{lng}/translation.json
            file_extensions = [
                'yml',
                'yaml',
                'json',
            ]

        self.locales_base = locales_base
        self.file_extensions = file_extensions
        self.data[self.bcp47_objetive] = {
            'error': 'no single translation file loaded'
        }
        self.data[self.bcp47_fallback] = {
            'error': 'no single translation file loaded'
        }

        if not self.bcp47_objetive:
            if strictness_level > 0:
                raise SyntaxError('No bcp47_objetive selected')
            # pass

        self.load_all_from_disk()

    def load_all_from_disk(self):
        """load_all_from_disk load only files targeted for use now

        """
        _base = None
        for attempted_bases in self.locales_base:
            if exists(attempted_bases):
                _base = attempted_bases
                break
        if not _base:
            # Stop if directory does not exist
            return None
        file_extensions = ','.join(self.file_extensions)
        file_pattern = f'{_base}/*/*.{{{file_extensions}}}'

        matches = []
        current_lang = None
        current_namespace = None
        for root, _dirnames, filenames in os.walk(_base):
            for filename in fnmatch.filter(filenames, '*.*'):
                root_parts = root.split('/')
                if len(root_parts) != 2:
                    # we expect something like 'i18n/en' not 'i18n/en/subdir'
                    # for now.
                    continue
                current_lang = root_parts[1]
                if current_lang not in [self.bcp47_objetive,
                                        self.bcp47_fallback, 'default']:
                    # Also skiping languages user do not specified
                    continue
                filename_parts = filename.split('.')
                current_namespace = filename_parts[0]
                loaded_data = self.load_file(os.path.join(root, filename))
                # _data_now = {
                #     current_namespace: loaded_data
                # }
                if current_namespace == self.base_namespace:
                    _data_now = loaded_data
                else:
                    _data_now = {
                        current_namespace: loaded_data
                    }

                self.data[current_lang] = {
                    **self.data[current_lang],
                    **_data_now
                }
                if 'error' in self.data[current_lang]:
                    del self.data[current_lang]['error']
                if current_lang == self.bcp47_fallback:
                    # self.data['default'] = {
                    #     current_namespace: loaded_data
                    # }
                    self.data['default'] = {
                        **self.data['default'],
                        **_data_now
                    }
                    if 'error' in self.data['default']:
                        del self.data['default']['error']

        for lang in self.data:
            if 'error' in self.data[lang]:
                if self.strictness_level == 1:
                    raise FileNotFoundError(f'TranslationLoader [{lang}]')

                if self.strictness_level == 2:
                    raise FileNotFoundError(
                        f'TranslationLoader [{lang}] [{self.data}]')

    def load_file(self, file: str) -> dict:
        """load_file

        Args:
            file (str): path to file

        Returns:
            dict: return content of file as python dictionary
        """
        with open(file) as _file:
            data = yaml.load(_file, Loader=yaml.SafeLoader)
            return data

    def get_data(self):
        return self.data

# lrenderer = LiquidRenderer()
# print(lrenderer.render("Hello, {{ you }}!", {'you': 'you value'}))

# sys.exit(1)


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
