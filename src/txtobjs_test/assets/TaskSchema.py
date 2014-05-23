from txtobjs.schema.TextObjectSchema import TextObjectSchema

from txtobjs.schema.SimpleTextField import SimpleTextField
from txtobjs.schema.ObjIdList import ObjIdList

class TaskSchema(TextObjectSchema):
    '''Sample factory to parse project.yml test file'''

    text_class = 'Task'

    title = SimpleTextField('Title')
    predecessors = ObjIdList('pred', text_class='Project')


