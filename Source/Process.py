# -*- coding: utf-8 -*-
import os;
import time;
from Reader import Reader;
from Indexer import Indexer;
from Utils import Utils;


class Process:
    NUM_PAGES_PER_THREAD = 5000;
    INDEX_FOLDER = 'indexdir';
    INDEX_NAME = 'wiki';

    def __init__(self):
        self.entries = [];

    def __Readfile(self, filename):
        """
        Read file database
        :param filename: name of data, <.txt> or <.zip>
        :return:
            True: if read successfully
            False: otherwise
        """
        rd = Reader(filename);
        self.entries = rd.Read();
        if 0 == len(self.entries):
            return False;
        return True;

    def __Indexing(self):
        indexer = Indexer(folder=Process.INDEX_FOLDER, name=Process.INDEX_NAME, entries=self.entries);
        indexer.Index();

    def Build(self, database_filename):
        """
        Call _Readfile and _Indexing
        :param database_filename: name of data base pass to __Readfile(filename)
        :return: None
        """
        if not os.path.exists(Process.INDEX_FOLDER):
            os.mkdir(Process.INDEX_FOLDER);

        if not Indexer.Check_exists(Process.INDEX_FOLDER, Process.INDEX_NAME):
            print "Building model .............";
            start_time = time.time();
            if self.__Readfile(database_filename):
                self.__Indexing();
            print "Done, Building time: %f" % (time.time() - start_time);

    def Search(self, mode, filename=None, query=None):
        """
        :param mode: True: search with query string
                     False: search with file of queries
        :param filename: string, name of file query, not None if mode is False
        :param query: string, input query, not None if mode is True,
        :return: None
        """
        if not os.path.exists(Process.INDEX_FOLDER) \
                or not Indexer.Check_exists(Process.INDEX_FOLDER, Process.INDEX_NAME):
            print "Please run : python Main.py --build <DATABASE_FILE>"
            return;

        ix = Indexer(folder=Process.INDEX_FOLDER, name=Process.INDEX_NAME);
        if mode:
            query = query.decode('utf-8');
            results = ix.QueryString(query);
            Utils.PrintResult(results);
        else:
            ix.QueryFile(filename);
            print "Please check result in %s folder !" % Indexer.RESULT_QUERY_FOLDER;