from txtobjs.TextObjectFactory import TextObjectFactory

from txtobjs.model.SimpleTextField import SimpleTextField

class ProjectFactory(TextObjectFactory):
    '''Sample factory to parse project.yml test file'''

    text_class = 'Project'

    title = TextField('Title')
    started = DateField('Started')
    hidden = FlagField('Hidden')
    active = BoolField('Active')
    predecessors = RemoteObjList('Predecesssors',
                                 text_class='Project')

    project_id = TextField('Id').identifies_obj()
    tasks = SubObjectDict('Tasks', factory=ProjectTaskFactory())

