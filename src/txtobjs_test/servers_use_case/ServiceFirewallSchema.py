from txtobjs.schema.TextObjectSchema import TextObjectSchema

from txtobjs.schema.SimpleTextField import SimpleTextField
from txtobjs.schema.SubObjectDict import SubObjectDict
from txtobjs.schema.SubObjectDictKey import SubObjectDictKey
from txtobjs.schema.ObjId import ObjId
from txtobjs.schema.EnumField import EnumField

class ServiceFirewallSchema(TextObjectSchema):

    text_class = 'ServiceFirewall'

    name = SubObjectDictKey()

    type = EnumField('type', valid=['INPUT', 'OUTPUT', 'FORWARD'])
    ports = ValueListField('ports', value_schema=SimpleTextField())
    allowed_nets = ObjIdList('allowed_nets', text_class='Network')
