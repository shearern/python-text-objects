from txtobjs.TextObjectFactory import TextObjectSchema

from txtobjs.model.SimpleTextField import SimpleTextField
from txtobjs.model.DateField import DateField
from txtobjs.model.FlagField import FlagField
from txtobjs.model.BoolField import BoolField
from txtobjs.model.RemoteObjList import RemoteObjList
from txtobjs.model.SubObjectDict import SubObjectDict

class ProjectSchema(TextObjectSchema):
    '''Sample factory to parse project.yml test file'''

    text_class = 'Project'

    title = SimpleTextField('Title')
    started = DateField('Started')
    hidden = FlagField('Hidden')
    active = BoolField('Active')
    predecessors = RemoteObjList('Predecesssors',
                                 text_class='Project')

    project_id = SimpleTextField('Id').identifies_obj()
    tasks = SubObjectDict('Tasks', factory=ProjectTaskFactory())

