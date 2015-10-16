from txtobjs.schema.TextObjectSchema import TextObjectSchema

from txtobjs.schema import SimpleTextProperty.SimpleTextField
from txtobjs.schema.SubObjectDict import SubObjectDictKey

class NetworkSchema(TextObjectSchema):

    text_class = 'Network'

    name = SubObjectDictKey()

    abbrv = SimpleTextProperty('abbrv')
    ip = SimpleTextProperty('ip')
    netmask = SimpleTextProperty('netmask')
    vlan = SimpleTextProperty('vlan')
    gateway = SimpleTextProperty('gateway')
