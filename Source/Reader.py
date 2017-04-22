import codecs
import os
import zipfile

class Reader:
    datafile_ext = [".zip", ".txt"];
    field = ['url', 'title', 'description'];

    def __init__(self, filename):
        self.filename = filename;

    def Read(self):
        """
        Read database file
        Can read 2 types of file <.txt> or <.zip>
        :return: list of entries, format of entry is a dict ('url', title', 'description')
        """
        res = [];
        try:
            name, ext = os.path.splitext(self.filename);
            if ext not in Reader.datafile_ext:
                raise NameError("Data type error !");
            if ".txt" == ext:
                with codecs.open(self.filename, 'rb', encoding='utf-8') as f:
                    lines = f.readlines();
                    for line in lines:
                        val = line.split('\t');
                        res.append(dict(zip(Reader.field, val)));
            else:
                with zipfile.ZipFile(self.filename) as z:
                    for filename in z.namelist():
                        if not os.path.isdir(filename):
                            with z.open(filename) as f:
                                lines = f.readlines();
                                for line in lines:
                                    line = line.decode('utf-8')
                                    val = line.split('\t');
                                    res.append(dict(zip(Reader.field, val)));

        except IOError:
            print "Database not found !";

        except NameError:
            raise;

        return res;


class QFile:
    def __init__(self):
        pass;

    @staticmethod
    def WriteResult(filename, data):
        """
        Write result of search query to file
        :param filename: name of file result (query string)
        :param data: result of query
        :return: None
        """
        with codecs.open(filename, 'wb', encoding='utf-8') as f:
            for field in data:
                for content in field:
                    f.write(content[1] + u'\t')
                f.write(u'\n')

    @staticmethod
    def ReadQuery(filename):
        """
        Read queries from file
        :param filename: name of query file
        :return: list, each element in list is a query
                 None if error
        """
        try:
            with codecs.open(filename, 'rb', encoding='utf-8') as f:
                return f.readlines();
        except IOError:
            print "Query file not found !"
            return None;