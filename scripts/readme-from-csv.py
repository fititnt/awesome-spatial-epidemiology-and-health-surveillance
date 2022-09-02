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
#                   - chevron (pip install chevron)
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
from typing import List, Type
from ast import literal_eval

from liquid import Template
from liquid import FileSystemLoader
from liquid import StrictUndefined
from liquid import Mode
from liquid_extra import filters
from liquid import Environment
from liquid_extra.filters import Translate

# import pystache
import chevron

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
            help='Line formatter using mustache formatter.'
            'Headers are converted to variables, and linear format is '
            'avalible as "raw_line"'
            'Default: "{{.}}" (print every option)',
            dest='line_formatter',
            nargs='?',
            # required=True
            default='{{.}}'
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
                pyargs.merge_file_2,
                pyargs.merge_key_2,
                pyargs.merge_foreignkey_2,
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
        self,
        infile,
        verbose: bool = False
    ):
        self.infile = infile
        self.verbose = verbose

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
        for line in self.data_compiled:
            print(line)


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
        self.merge_file_2 = merge_file_2
        self.merge_key_2 = merge_key_2
        self.merge_foreignkey_2 = merge_foreignkey_2
        self.input_delimiter = input_delimiter
        # self.output_format = output_format

        self.liquid = LiquidRenderer()

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
                parsed_line_select = chevron.render(
                    self.line_select,
                    line_variables)
                evaluated_line_select = evaluate(parsed_line_select)
                # print('result_line_select', result_line_select)
                if not evaluated_line_select:
                    continue

            if self.line_exclude is not None:
                parsed_line_exclude = self.line_exclude.format(
                    **line_variables)
                parsed_line_exclude = chevron.render(
                    self.line_exclude,
                    line_variables)
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
            print(chevron.render(
                self.line_formatter,
                line_variables).replace('\\n', "\n"))

            # print(self.liquid.render(
            #     self.line_formatter,
            #     line_variables
            # ))

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

    default_template: Type['Template'] = None
    env: Environment

    def __init__(self) -> None:

        self.default_template = Template(
            "Hello, {{ you }}!",
            # tolerance=Mode.STRICT,
            # undefined=StrictUndefined,
        )
        # pass
        # self.env = Environment()
        # self.env.add_filter("json", filters.JSON())
        self.env = Environment(
            tolerance=Mode.STRICT,
            undefined=StrictUndefined,
            # loader=FileSystemLoader("./templates/"),
        )
        self.env.add_filter("json", filters.JSON())

        some_locales = {
            "default": {
                "layout": {
                    "greeting": r"Hello {{ name }}",
                },
                "cart": {
                    "general": {
                        "title": "Shopping Basket",
                    },
                },
                "pagination": {
                    "next": "Next Page",
                },
            },
            "de": {
                "layout": {
                    "greeting": r"Hallo {{ name }}",
                },
                "cart": {
                    "general": {
                        "title": "Warenkorb",
                    },
                },
                "pagination": {
                    "next": "Nächste Seite",
                },
            },
        }
        self.env.add_filter(Translate.name, Translate(locales=some_locales))

    def render(self, template: str = None, context: dict = None) -> str:

        # env = Environment()
        # env.add_filter("index", filters.index)
        # env.add_filter("json", filters.JSON())
        # if template is None:
        #     compiled_template = self.default_template
        # else:
        #     compiled_template = Template(
        #         # "Hello, {{ you }}!",
        #         template,
        #         # tolerance=Mode.STRICT,
        #         # undefined=StrictUndefined,
        #     )
        if template is None or template is False:
            extra_context = {'current_context': context}
            compiled_template = self.env.from_string(
                '{{ current_context | json }}'
            )
        else:
            compiled_template = self.env.from_string(template)
            extra_context = context

        result = compiled_template.render(extra_context)
        return result


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
