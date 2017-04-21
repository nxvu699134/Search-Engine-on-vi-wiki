from Process import Process;
from Log import Setup_logging;
import argparse;

DATA_NAME = 'data.txt'


def main():
    Setup_logging();
    arg_parser = argparse.ArgumentParser();
    arg_parser.add_argument("[DATABASE_NAME]", type=str, help="Name of database file <.txt> or <.zip>");
    arg_parser.add_argument("-q", "--query", nargs=1, help="Search with a query");
    arg_parser.add_argument("-f", "--file", nargs=1, help="Search with a file that contains some queries");
    args = arg_parser.parse_args()
    p = Process(DATA_NAME);
    if args.query:
        p.Run(True, query=args.query[0]);
    elif args.file:
        p.Run(False, filename=args.file[0]);
    # else:
    #     print args.help


if '__main__' == __name__:
    main();
