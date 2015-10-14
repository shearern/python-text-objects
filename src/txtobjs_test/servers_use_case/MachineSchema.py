from txtobjs.schema.TextObjectSchema import TextObjectSchema

from txtobjs.schema import SimpleTextProperty.SimpleTextField
from txtobjs.schema.SubObjectDict import SubObjectDict
from txtobjs.schema.ValueListField import ValueListField

class MachineSchema(TextObjectSchema):

    text_class = 'Machine'

    name = SubObjectDictKey()

    hostname = SimpleTextProperty('hostname')
    interfaces = SubObjectDict('interfaces', schema=MachineInterfaceSchema())
    primary_interfaces = SimpleTextProperty('primary_interface')
    groups = ValueListField('groups', value_schema=SimpleTextProperty())
