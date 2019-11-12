#!/usr/bin/env python3.7

import argparse
import json
import sys


def matches(parts, subject):
    if len(parts) == 0:
        yield subject
        return

    part, *rest = parts

    # If we're extracting something from `subject`, and `subject` is neither a
    # list nor a dict, then there's nothing to extract.  Whether this is an
    # error or just a no-op was part of how my original solution was wrong.
    if type(subject) not in [list, dict]:
        return

    if type(subject) is list:
        if part == '*':
            for child in subject:
                yield from matches(rest, child)
            return

        try:
            index = int(part)
        except ValueError:
            return  # can't extract a property name from a list

        yield from matches(rest, subject[index])
    else:
        assert type(subject) is dict

        if part == '*':
            for child in subject.values():
                yield from matches(rest, child)
        elif part in subject:
            yield from matches(rest, subject[part])


def parse(pattern):
    # Corner case:  If the pattern is empty, then splitting on "." would yield
    # `[""]` instead of `[]`.
    if len(pattern) == 0:
        return []
    else:
        return pattern.split('.')


def extract(pattern, subject):
    parts = parse(pattern)
    results = list(matches(parts, subject))

    # If there were no wildcards in the query, then at most one thing can be
    # matched.  Avoid the redundant outer list when possible.
    if '*' in parts:
        return results  # list of results

    if len(results) == 0:
        return None

    assert len(results) == 1
    return results[0]


def parse_command_line(args):
    parser = argparse.ArgumentParser(description='Extract values from JSON.')

    parser.add_argument('pattern',
                        help='JSON query (path) to extract from input')

    return parser.parse_args()


if __name__ == '__main__':
    options = parse_command_line(sys.argv[1:])
    result = extract(options.pattern, json.load(sys.stdin))

    if result is not None:
        json.dump(result, sys.stdout, indent=4, sort_keys=True)

    print()  # for the newline
