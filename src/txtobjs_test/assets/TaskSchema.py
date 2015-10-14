from txtobjs.schema.TextObjectSchema import TextObjectSchema

from txtobjs.schema import SimpleTextProperty.SimpleTextField
from txtobjs.schema import ObjIdListProperty.ObjIdList

class TaskSchema(TextObjectSchema):
    '''Sample factory to parse project.yml test file'''

    text_class = 'Task'

    title = SimpleTextField('Title')
    predecessors = ObjIdListProperty('pred', text_class='Project')


