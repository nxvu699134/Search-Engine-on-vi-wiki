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
        rd = Reader(filename);
        self.entries = rd.Read();
        if 0 == len(self.entries):
            return False;
        return True;

    def __Indexing(self):
        indexer = Indexer(folder=Process.INDEX_FOLDER, name=Process.INDEX_NAME, entries=self.entries);
        indexer.Index();

    def Build(self, database_filename):
        if not os.path.exists(Process.INDEX_FOLDER):
            os.mkdir(Process.INDEX_FOLDER);

        if not Indexer.Check_exists(Process.INDEX_FOLDER, Process.INDEX_NAME):
            print "Building model .............";
            start_time = time.time();
            if self.__Readfile(database_filename):
                self.__Indexing();
            print "Done, Building time: %f" % (time.time() - start_time);

    '''mode : True : query with string, file is otherwise'''
    def Search(self, mode, filename=None, query=None):
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