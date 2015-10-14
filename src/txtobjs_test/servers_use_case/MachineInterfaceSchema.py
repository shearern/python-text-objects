from txtobjs.schema.TextObjectSchema import TextObjectSchema

from txtobjs.schema.SimpleTextProperty import SimpleTextProperty
from txtobjs.schema.SubObjectDictProperty import SubObjectDictKey
from txtobjs.schema import ObjIdProperty.ObjId
from txtobjs.schema.EnumField import EnumField

class MachineInterfaceSchema(TextObjectSchema):

    text_class = 'MachineInterface'

    name = SubObjectDictKey()

    ip = SimpleTextProperty('ip')
    network = ObjIdProperty('network', text_class='Network')
    mac = SimpleTextField('mac')
    provisioned = EnumField('provisioned', valid=['dhcp', 'static'])
