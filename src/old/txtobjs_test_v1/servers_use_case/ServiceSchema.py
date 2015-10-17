from txtobjs.schema.TextObjectSchema import TextObjectSchema

from txtobjs.schema import SimpleTextProperty.SimpleTextField
from txtobjs.schema.SubObjectDict import SubObjectDict
from txtobjs.schema.ValueListField import ValueListField

class ServiceSchema(TextObjectSchema):

    text_class = 'Service'

    name = SubObjectDictKey()

    role_name = SimpleTextProperty('role_name')
    hosts = ObjIdList('hosts', text_class='Machine')
    firewall = SubObjectDict('firewall', schema=ServiceFirewallSchema())
