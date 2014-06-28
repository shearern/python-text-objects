from txtobjs.schema.TextObjectSchema import TextObjectSchema

from txtobjs.schema.SimpleTextField import SimpleTextField
from txtobjs.schema.SubObjectDict import SubObjectDict

from NetworkSchema import NetworkSchema
from MachineSchema import MachineSchema
from ServiceSchema import ServiceSchema

class SiteSchema(TextObjectSchema):

    text_class = 'Site'

    name = SimpleTextField('Title')

    networks = SubObjectDict('networks', schema=NetworkSchema())
    machines = SubObjectDict('machines', schema=MachineSchema())
    services = SubObjectDict('services', schema=ServiceSchema())
