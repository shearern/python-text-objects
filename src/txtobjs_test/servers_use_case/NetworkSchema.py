from txtobjs.schema.TextObjectSchema import TextObjectSchema

from txtobjs.schema.SimpleTextField import SimpleTextField
from txtobjs.schema.SubObjectDict import SubObjectDictKey

class NetworkSchema(TextObjectSchema):

    text_class = 'Network'

    name = SubObjectDictKey()

    abbrv = SimpleTextField('abbrv')
    ip = SimpleTextField('ip')
    netmask = SimpleTextField('netmask')
    vlan = SimpleTextField('vlan')
    gateway = SimpleTextField('gateway')
