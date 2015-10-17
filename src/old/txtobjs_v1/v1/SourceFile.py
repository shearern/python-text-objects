
class SourceFileLine(object):
    '''Save the path and line number used to generate an object'''

    def __init__(self, path, line_num):
        self.__path = path
        self.__line_num = line_num

    @property
    def path(self):
        return self.__path

    @property
    def line_num(self):
        return self.__line_num


class SourceFile(object):
    '''Save path of a text file used to generate an object'''


    def __init__(self, path):
        self.__path = path

    @property
    def path(self):
        return self.__path


    def note_line(self, line_num):
        return SourceFileLine(self.__path, line_num)
