import argparse
import csv
import json
import os
from pathlib import PosixPath

from pyproject_save_files import BuildrootPath


def read_record(record_path):
    """
    A generator yielding individual RECORD triplets.

    https://www.python.org/dev/peps/pep-0376/#record

    The triplet is str-path, hash, size -- the last two optional.
    We will later care only for the paths anyway.

    Example:

        >>> g = read_record(PosixPath('./test_RECORD'))
        >>> next(g)
        ['../../../bin/__pycache__/tldr.cpython-....pyc', '', '']
        >>> next(g)
        ['../../../bin/tldr', 'sha256=...', '12766']
        >>> next(g)
        ['../../../bin/tldr.py', 'sha256=...', '12766']
    """
    with open(record_path, newline="", encoding="utf-8") as f:
        yield from csv.reader(
            f, delimiter=",", quotechar='"', lineterminator=os.linesep
        )


def parse_record(record_path, record_content):
    """
    Returns a list with BuildrootPaths parsed from record_content

    params:
    record_path: RECORD BuildrootPath
    record_content: list of RECORD triplets
                    first item is a str-path relative to directory where dist-info directory is
                    (it can also be absolute according to the standard, but not from pip)

    Examples:
        >>> parse_record(BuildrootPath('/usr/lib/python3.7/site-packages/requests-2.22.0.dist-info/RECORD'),
        ...                            [('requests/sessions.py', 'sha256=xxx', '666')])
        ['/usr/lib/python3.7/site-packages/requests/sessions.py']

        >>> parse_record(BuildrootPath('/usr/lib/python3.7/site-packages/tldr-0.5.dist-info/RECORD'),
        ...                            [('../../../bin/tldr', 'sha256=yyy', '777')])
        ['/usr/bin/tldr']
    """
    sitedir = record_path.parent.parent  # trough the dist-info directory
    # / with absolute right operand will remove the left operand
    # any .. parts are resolved via normpath
    return [str((sitedir / row[0]).normpath()) for row in record_content]


def save_parsed_record(record_path, parsed_record, output_file):
    content = {}
    if output_file.is_file():
        content = json.loads(output_file.read_text())
    content[str(record_path)] = parsed_record
    output_file.write_text(json.dumps(content))


def main(cli_args):
    record_path = BuildrootPath.from_real(cli_args.record, root=cli_args.buildroot)
    parsed_record = parse_record(record_path, read_record(cli_args.record))
    save_parsed_record(record_path, parsed_record, cli_args.output)


def argparser():
    parser = argparse.ArgumentParser()
    r = parser.add_argument_group("required arguments")
    r.add_argument("--buildroot", type=PosixPath, required=True)
    r.add_argument("--record", type=PosixPath, required=True)
    r.add_argument("--output", type=PosixPath, required=True)
    return parser


if __name__ == "__main__":
    cli_args = argparser().parse_args()
    main(cli_args)
