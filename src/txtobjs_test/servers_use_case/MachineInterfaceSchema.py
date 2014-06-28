from txtobjs.schema.TextObjectSchema import TextObjectSchema

from txtobjs.schema.SimpleTextField import SimpleTextField
from txtobjs.schema.SubObjectDict import SubObjectDictKey
from txtobjs.schema.ObjId import ObjId
from txtobjs.schema.EnumField import EnumField

class MachineInterfaceSchema(TextObjectSchema):

    text_class = 'MachineInterface'

    name = SubObjectDictKey()

    ip = SimpleTextField('ip')
    network = ObjId('network', text_class='Network')
    mac = SimpleTextField('mac')
    provisioned = EnumField('provisioned', valid=['dhcp', 'static'])
