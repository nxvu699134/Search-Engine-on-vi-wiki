import re

class Utils:
    def __init__(self):
        pass;

    @staticmethod
    def QueryToFilename(query):
        """
        Convert query string to a valid file name for result
        :param query: query string
        :return: string, valid file name
        """
        format = re.compile(r'[\\/*?:"<>|]', re.UNICODE);
        query = format.sub('_', query);
        return query + u".txt";

    @staticmethod
    def PrintResult(results):
        """
        Print result to console
        :param results: list, list of results
        :return: None
        """
        for i in range(len(results)):
            print "------------- Result %d --------------" % i;
            for content in results[i]:
                print content[0], " : ", content[1];
            print "\n"



