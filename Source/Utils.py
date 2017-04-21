import re

class Utils:
    def __init__(self):
        pass;

    @staticmethod
    def FilenameToURL(filename):
        return (u"http://" + filename).replace(u"~", u"/").replace(u".txt", u"");

    @staticmethod
    def URLToFilename(URL):
        return URL.replace(u"http://", u"").replace(u"/", u"~") + u".txt";

    @staticmethod
    def QueryToFilename(query):
        format = re.compile(r'[\\/*?:"<>|]', re.UNICODE);
        query = format.sub('_', query);
        return query + u".txt";

    @staticmethod
    def PrintResult(results):
        for i in range(len(results)):
            print "------------- Result %d --------------" % i;
            for content in results[i]:
                print content[0], " : ", content[1];
            print "\n"



