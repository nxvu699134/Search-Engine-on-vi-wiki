from Process import Process;
from Log import Setup_logging;
import argparse;

DATA_NAME = 'data.txt'


def main():
    Setup_logging();
    arg_parser = argparse.ArgumentParser();
    arg_parser.add_argument("-b", "--build", nargs=1, type=str, metavar='DATABASE_FILE',
                            help="Build model with database file. Name of database file <.txt> or <.zip>");
    arg_parser.add_argument("-q", "--query", nargs=1, type=str, help="Search with a query");
    arg_parser.add_argument("-qf", "--queryfile", nargs=1, type=str,
                            help="Search with a file that contains some queries");
    args = arg_parser.parse_args()
    p = Process();
    if args.query:
        p.Search(True, query=args.query[0]);
    elif args.queryfile:
        p.Search(False, filename=args.queryfile[0]);
    elif args.build:
        p.Build(args.build[0]);


if '__main__' == __name__:
    main();
