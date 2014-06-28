from txtobjs.schema.TextObjectSchema import TextObjectSchema

from txtobjs.schema.SimpleTextField import SimpleTextField
from txtobjs.schema.SubObjectDict import SubObjectDict
from txtobjs.schema.ValueListField import ValueListField

class MachineSchema(TextObjectSchema):

    text_class = 'Machine'

    name = SubObjectDictKey()

    hostname = SimpleTextField('hostname')
    interfaces = SubObjectDict('interfaces', schema=MachineInterfaceSchema())
    primary_interfaces = SimpleTextField('primary_interface')
    groups = ValueListField('groups', value_schema=SimpleTextField())
