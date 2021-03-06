from txtobjs.schema.TextObjectSchema import TextObjectSchema

from txtobjs.schema.SimpleTextField import SimpleTextField
from txtobjs.schema.DateField import DateField
from txtobjs.schema.FlagField import FlagField
from txtobjs.schema.BoolField import BoolField
from txtobjs.schema.ObjIdList import ObjIdList
from txtobjs.schema.SubObjectDict import SubObjectDict

from TaskSchema import TaskSchema

class ProjectSchema(TextObjectSchema):
    '''Sample factory to parse project.yml test file'''

    text_class = 'Project'

    title = SimpleTextField('Title')
    started = DateField('Started')
    hidden = FlagField('Hidden')
    active = BoolField('Active')
    predecessors = ObjIdList('Predecesssors', text_class='Project')

    project_id = SimpleTextField('Id').identifies_obj()
    tasks = SubObjectDict('Tasks', schema=TaskSchema())

