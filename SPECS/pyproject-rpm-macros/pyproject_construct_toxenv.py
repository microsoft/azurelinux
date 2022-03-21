import argparse
import sys


def main(argv):
    parser = argparse.ArgumentParser(
        description='Parse -e arguments instead of RPM getopt.'
    )
    parser.add_argument('-e', '--toxenv', action='append')
    args, _ = parser.parse_known_args(argv)
    return ','.join(args.toxenv)


if __name__ == '__main__':
    print(main(sys.argv[1:]))
