from __future__ import print_function
import os
import sys
import argparse
from .parser import ECfg


def main(argv=None):
    parser = argparse.ArgumentParser(description='Parse e.cfg files')
    parser.add_argument('filename')
    parser.add_argument('--format',
                        help='Output format',
                        choices=('text', 'xml', 'json'),
                        default='text')
    args = parser.parse_args(argv)

    if not os.path.exists(args.filename):
        print('Input file not found')
        return 1

    with open(args.filename) as f:
        text = f.read()

    result = ECfg(text)

    if args.format == 'text':
        print(result.text())
    elif args.format == 'xml':
        print(result.xml())
    elif args.format == 'json':
        print(result.json(indent=2))


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
