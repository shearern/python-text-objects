
class TextOjbectLoader(object):
    '''Class to supervise the laoding and parsing of the test objects

    Typical usage is:
        txt = TxtParser()
        xml = XmlParser()

        loader = TextObjectLoader()
        proj_a = loader.parse_single_object_file(
            path = 'project_a.txt',
            parser = txt,
            schema = ProjectSchema())
        proj_b = loader.parse_single_object_file(
            path = 'project_b.txt',
            parser = txt,
            schema = ProjectSchema(),
            obj_id='project_b')
        task_list = loader.parse_object_list_file(
            path = 'tasks.xml',
            parser = xml,
            item_schema = TaskSchema())
        loader.link()
    '''

    def __init__(self):
        self.__objs = list()

        # Indexes
        self.__objs_by_text_class = dict()
        self.__objs_by_id = dict()


    def _load(self, text_object, schema):
        '''Register a new text object'''


    def parse_single_object_file(self, path, parser, schema, object_id=None):
        '''Parse a text file that contains a single text object

        @param path: Path to text file to parse
        @param parser: Text syntax parser to use (see txt_parsers.TextParser)
        @param schema: TextObject schema to use
        @param object_id: Id to give TextObject if it can't be determined from
            the TextObject attributes (for example, if it's from the filename)
        '''
        with open(path, 'rt') as fh:
            tobj_gen = parser.parse(
                src = fh.read(),
                schema = schema,
                multiple = False)
            for tobj in tobj_gen:
                self._load(tobj, schema)



    def parse_object_list_file(self, path, parser, item_schema):
        '''Parse a text file that contains a list of text objects

        This is to handle a text file where the root/document level data struct
        is a list of TextObject
        '''


