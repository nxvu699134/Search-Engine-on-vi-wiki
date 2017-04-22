# -*- coding: utf-8 -*-
import logging
import whoosh.index as index;
from whoosh.index import *
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.analysis.analyzers import StemmingAnalyzer
from whoosh import scoring
from Reader import QFile
from Utils import Utils


class Indexer:
    RESULT_QUERY_FOLDER = 'Query_Result'
    NUMBER_PAGE_FETCH = 20;

    def __init__(self, folder, name, entries=None):
        self.name = name;
        self.folder = folder;
        self.entries = entries;


    def Index(self):
        """
        Create index
        :param: None
        :return: None
        """
        schema = Schema(url=ID(stored=True), # ID field is distinct, stored=True is save url to display
                        title=TEXT(stored=True, analyzer=StemmingAnalyzer(stoplist=None, minsize=1)),
                        description=TEXT(analyzer=StemmingAnalyzer(stoplist=None, minsize=1)));
        ix = create_in(dirname=self.folder, schema=schema, indexname=self.name);
        # with limitmb is amount RAM per processor, in this case is 256 * 4
        with ix.writer(procs=4, limitmb=256) as writer:
            for entry in self.entries:
                try:
                    writer.add_document(url=entry['url'], title=entry['title'],
                                        description=entry['description']);
                except:
                    logging.info("Index has been failed successfully: %s" % (entry['url']));

    @staticmethod
    def Check_exists(folder_name, index_name):
        """
        Check index existed
        :param folder_name: index folder
        :param index_name: name of index
        :return:
            True: if existed
            False: otherwise
        """
        return index.exists_in(folder_name, index_name);

    def QueryString(self, strQuery):
        """
        Search on index with a direct query string
        :param strQuery: query string
        :return: res: a list of results contain tuple ('url', 'title')
        """
        ix = open_dir(dirname=self.folder, indexname=self.name);
        # set scorer is TF-IDF
        with ix.searcher(weighting=scoring.TF_IDF()) as searcher:
            res = [];
            # query by title first
            title = QueryParser("title", ix.schema).parse(strQuery)
            # limit is number of page want to hit, in this case is 20
            title_results = searcher.search(title, limit=Indexer.NUMBER_PAGE_FETCH, reverse=False);
            n = 10 if 10 < len(title_results) else len(title_results);
            for i in range(n):
                res.append(zip(title_results[i].keys(), title_results[i].values()));

            # query by content
            content = QueryParser("description", ix.schema).parse(strQuery);
            content_results = searcher.search(content, limit=Indexer.NUMBER_PAGE_FETCH, reverse=False);
            remaining = Indexer.NUMBER_PAGE_FETCH - len(title_results);
            n = remaining if remaining < len(content_results) else len(content_results)
            for i in range(n):
                res.append(zip(content_results[i].keys(), content_results[i].values()))
            return res;

    def QueryFile(self, filename):
        """
        Search on index with a file of query that contain some queries
        :param filename: name of file
        :return: None, Result will be written to file in Query_Result folder
        """
        print filename
        # read file query
        queries = QFile.ReadQuery(filename);
        if queries is not None:
            results = [];
            for query in queries:
                results.append(self.QueryString(query));
            # write result
            try:
                os.mkdir(Indexer.RESULT_QUERY_FOLDER);
            except:
                pass;
            for result, query in zip(results, queries):
                QFile.WriteResult(Indexer.RESULT_QUERY_FOLDER + u"/" + Utils.QueryToFilename(query), result);

