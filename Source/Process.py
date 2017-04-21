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
    CACHE_FOLDER = 'Cache';

    def __init__(self, database_filename):
        self.entries = [];
        self.database_filename = database_filename;
        self.Cache = set();

    def __Readfile(self, filename):
        rd = Reader(filename);
        self.entries = rd.Read();
        if 0 == len(self.entries):
            return False;
        return True;

    def __Indexing(self):
        indexer = Indexer(folder=Process.INDEX_FOLDER, name=Process.INDEX_NAME, entries=self.entries);
        indexer.Index();

    def __Training(self):
        if self.__Readfile(self.database_filename):
            self.__Indexing();

    '''mode : True : query with string, file is otherwise'''
    def Run(self, mode, filename=None, query=None):
        if not os.path.exists(Process.INDEX_FOLDER):
            os.mkdir(Process.INDEX_FOLDER);

        if not Indexer.Check_exists(Process.INDEX_FOLDER, Process.INDEX_NAME):
            print "Building model .............";
            start_time = time.time();
            self.__Training();
            print "Done, Building time: %f" % (time.time() - start_time);

        ix = Indexer(folder=Process.INDEX_FOLDER, name=Process.INDEX_NAME);
        if mode:
            print query
            query = query.decode('utf-8');
            results = ix.QueryString(query);
            Utils.PrintResult(results);
        else:
            ix.QueryFile(filename);
            print "Please check result in %s folder !" % Indexer.RESULT_QUERY_FOLDER;



    # def __LoadCache(self):
    #     try:
    #         os.mkdir(Process.CACHE_FOLDER);
    #     except:
    #         for file in os.listdir(Process.CACHE_FOLDER):
    #             if file.endswith(".txt"):
    #                 file = file.decode(encoding='utf-8');
    #                 self.Cache.add(Utils.FilenameToURL(file));
    #

    #
    # def __CreateCrawlThread(self):
    #     threads = [];
    #     num_thread = len(self.entries) / Process.NUM_PAGES_PER_THREAD;
    #     print num_thread
    #     for i in range(0, num_thread):
    #         begin = Process.NUM_PAGES_PER_THREAD * i;
    #         end = begin + Process.NUM_PAGES_PER_THREAD;
    #         thread = CrawlThread(i, "Thread-" + str(i), [self.entries[j] for j in range(begin, end)]);
    #         thread.start();
    #         threads.append(thread);
    #
    #     if 0 < len(self.entries) % Process.NUM_PAGES_PER_THREAD:
    #         begin = Process.NUM_PAGES_PER_THREAD * num_thread;
    #         end = begin + len(self.entries) % Process.NUM_PAGES_PER_THREAD;
    #         thread = CrawlThread(num_thread, "Thread-"+str(num_thread),
    #                              [self.entries[j] for j in range(begin, end)])
    #         thread.start();
    #         threads.append(thread);
    #
    #     for thread in threads:
    #         thread.join();
    #
    #     return threads;
    #
    #



