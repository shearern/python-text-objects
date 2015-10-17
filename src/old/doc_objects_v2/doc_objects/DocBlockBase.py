from abc import ABCMeta, abstractproperty
from weakref import ref
from textwrap import wrap
import string

import markdown2

from ..exceptions import DocBlockStructureError
from ..exceptions import InvalidAttributeValueClass 
from ..utils import describe_block_loc

class AttributeDefinition(object):
    def __init__(self):
        self.name = None
        self.help = None
        self.expected = False
        self.markdown = False
        self.expected_class = None
        self.default_value = None
        

class LinkDefinintion(object):
    def __init__(self):
        self.name = None
        self.attr_name = None
        self.doc_classes = None
        self.multiple = False
    @property
    def is_reverse(self):
        return False
    
    
class ReversedLinkDefinition(object):
    def __init__(self):
        self.name = None
        self.linking = list()   # (doc_class, link_name)
    @property
    def is_reverse(self):
        return True
    @property
    def multiple(self):
        return True
        

class TransitivePropertyDefinition(object):
    '''.property -> .propA.propB.propC...'''
    def __init__(self):
        self.name = None
        self.property_chain = list()
        
        
class MissingLinkError(object):
    '''Record info about a link target that couldn't be found'''
    def __init__(self, source_block, link_name, link_value, possible_doc_types):
        self.source_block = source_block
        self.link_name = link_name
        self.link_value = link_value
        self.possible_doc_types = possible_doc_types
    def __str__(self):
        msg = "Could not find block '%s' in doc classes (%s) as referenced by %s"
        return msg % (self.link_value,
                      ', '.join(self.possible_doc_types),
                      self.link_name)
        

class TodoItem(object):
    '''Record a task that needs to be completed to complete the documentation'''
    
    HIGH_LVL='high'
    NORM_LVL='normal'
    LOW_LVL='low'
    
    def __init__(self, msg, level='normal', sort_order=0):
        self.msg = msg
        self.level = level
        self.sort_order = sort_order
        self.doc_block = None
        
        if level == self.HIGH_LVL:
            self.sort_order += 100
        elif level == self.LOW_LVL:
            self.sort_order -= 100
            
    @property
    def alert_class(self):
        if self.level == self.HIGH_LVL:
            return 'danger'
        elif self.level == self.NORM_LVL:
            return 'warning'
        elif self.level == self.LOW_LVL:
            return 'info'        
        
    
    @property
    def as_html(self):
        html = list()
        
        html.append("<div class='alert alert-%s' role='alert'>" % (
            self.alert_class))
        html.append("<div><b>%s</b>: %s</div>" % (
            self.doc_block.full_name, self.msg))
        html.append(describe_block_loc(self.doc_block))
        html.append("</div>")
        
        return "\n".join(html)


SAFE_CHARS = set(string.letters)
SAFE_CHARS = SAFE_CHARS.union(set(string.digits))

def sanitize_name(name):
    global SAFE_CHARS
    new_name = ''
    for c in name:
        if c in SAFE_CHARS:
            new_name += c
        else:
            new_name += '_'
    return new_name


class DocBlockBase(object, metaclass=ABCMeta):
    '''Wrappers for interpreting RawDocBlocks'''
    
    def __init__(self, raw_doc_block):
        super(DocBlockBase, self).__init__()
        
        self.__raw = list()
        
        self.__doc_class = self.__class__.__name__
        self.__name = raw_doc_block.name
        self.__safe_name = None
        
        self.__attr_order = list()
        self.__attr_defs = dict()
        self.__attr_values = dict()
        
        self.__link_defs = dict()
        self.__linked_objs = dict()
        
        self.__trans_properties = dict()
        
        self.__embedded_blocks_attrs = set()
        
        self._col = None  # WeakRef link to parent collection.  Set by Collect.
        
        self._link_errors = list()   # Errors placed here during link_and_validate()
        
            
    @property
    def doc_class(self):
        return self.__doc_class
    
    @property
    def name(self):
        return self.__name
    
    @property
    def safe_name(self):
        if self.__safe_name is None:
            self.__safe_name = sanitize_name(self.__name)
        return self.__safe_name
    
    @property
    def full_name(self):
        return '%s.%s' % (self.__doc_class, self.name)

    @property
    def attr_names(self):
        return list(self.__attr_values.keys())

    @property
    def attributes(self):
        return list(self.__attr_values.values())
    
    
    def is_attr_expected(self, name):
        return self.__attr_defs[name].expected

    
    @property
    def col(self):
        '''Collection'''
        if self._col is None:
            raise Exception("Add to collection first")
        return self._col()
    
    
    @property
    def raw_blocks(self):
        return self.__raw[:]
    
    
    @property
    def def_locs_str(self):
        '''String list of locations this block is defined at'''
        return ', '.join(self.block_locs)
        
        
    @property
    def block_locs(self):
        '''List of locations this block is defined at'''
        for raw_block in self.__raw:
            yield raw_block.loc
            
            
    @property
    def _link_definitions(self):
        for link_def in list(self.__link_defs.values()):
            yield link_def
    

    def __repr__(self):
        return "%s('%s')" % (self.doc_class, self.name)
        
        
    def _def_attribute(self, name, help_txt, expected=False, markdown=False,
                       link_to=None, link_name=None, link_multiple=False,
                       expected_class=str, default=None):
        if name in self.__attr_defs:
            raise Exception("Duplicate attribute name: '%s'" % (name))
        
        attr_def = AttributeDefinition()
        attr_def.name = name
        attr_def.help = help_txt
        attr_def.expected = expected
        attr_def.markdown = markdown
        attr_def.expected_class = expected_class
        attr_def.default_value = default

        self.__attr_defs[name] = attr_def
        
        self.__attr_order.append(name)
        
        if link_name is not None:
            if link_to is None:
                raise Exception("If link_name, then link_to")
            self._def_link(link_name, name, link_to, link_multiple)
        
            
    def _def_link(self, name, attr_name, links_to, multiple=False):
        '''Define an attribute that holds names of other objects
        
        This is called in __init__() to assist with:
         - Validating linked objects exist during validation
        
        @param attr_name: Name of the attribute holding the name
        @param name: Name of property on this object to access linked blocks.
        @param links_to: List of doc classes name can be found in.
        @param multiple: Allow list of multiple references
        '''
        if name in self.__link_defs:
            raise IndexError("Link named '%s' already defined" % (name))
        
        link_def = LinkDefinintion()
        link_def.name = name
        link_def.attr_name = attr_name
        link_def.doc_classes = links_to
        if link_def.doc_classes.__class__ is str:
            link_def.doc_classes = (link_def.doc_classes, )
        link_def.multiple = multiple
        
        self.__link_defs[name] = link_def
        self.__linked_objs[name] = list()
        
        
    def _def_trans_property(self, name, property_chain):
        '''Define a property that accesses a property of a sub property
        
        When a property refers to 1 or 0 other blocks, then this can be used
        to provide a shortcut to the referred to blocks property.  Accessing
        these properties will respond with None if one of the properties
        in the chain is None.
        
        @param name: Name of the property/shortcut to create on this class
        @param chain: Name of the properties to access in order to get the value
        '''
        if name in self.__attr_defs:
            msg = "An attribute with name '%s' is already defined"
            raise IndexError(msg % (name))
        if name in self.__link_defs:
            msg = "A link with name '%s' is already defined"
            raise IndexError(msg % (name))
        if name in self.__trans_properties:
            msg = "A transitive property with name '%s' is already defined"
            raise IndexError(msg % (name))
        
        prop = TransitivePropertyDefinition()
        prop.name = name
        prop.property_chain = property_chain
        
        self.__trans_properties[name] = prop
        
        
    def _def_reverse_link(self, name, from_doc_class, from_link_name):
        '''Define a property that returns info blocks linking *to* this block
        
        Call multiple times to capture multiple links.
        
        Makes available self.name to return blocks linking to this block.
        
        @param name: Name of the link (becomes property name)
        @param from_doc_class: doc_class of block linking to this block
        @param from_link_name: Name of the 
        '''
        if name in self.__link_defs:
            if not self.__link_defs[name].is_reverse:
                raise IndexError("Link named '%s' already defined" % (name))
        
        if name not in self.__link_defs:
            link_def = ReversedLinkDefinition()
            link_def.name = name
            self.__link_defs[name] = link_def
            self.__linked_objs[name] = list()
            
        self.__link_defs[name].linking.append((from_doc_class, from_link_name))
        
        
    def _def_embedded_block_attr(self, name):
        '''Define an attribute that holds sub-blocks
        
        _extract_embedded_doc_blocks(name, value, filename, linenum) must be
        defined to translate the attribute value into raw doc_blocks.
        
        @param name: Name of the attribute
        '''
        self.__embedded_blocks_attrs.add(name)
        
        
    def get_embedded_blocks(self):
        '''Get any embedded Doc Blocks'''
        for name in self.__embedded_blocks_attrs:
            if name in self.__attr_values:
                value = self.__attr_values[name].value
                fn = self.__attr_values[name].filename
                line = self.__attr_values[name].line
                for erb in self._extract_embedded_doc_blocks(name, value, fn, line):
                    yield erb

    
    def _extract_embedded_doc_blocks(self, name, value, filename, line):
        '''Extract RawDocBlocks from the given attribute value
        
        @param name: Name of the attribute
        @param value: Value stored in the attribute from this DocBlock
        @param filename: Filename where this attribute was set
        @param line: Line number where this attribute was set
        '''
        msg = "_extract_embedded_doc_blocks() needs to be defined for attribute '%s'"
        raise NotImplementedError(msg % (name))

            
    def clear_links(self):
        '''Clear existing links in case of calling link_and_validate() again'''
        self.__linked_objs = dict()
        for link in list(self.__link_defs.values()):
            self.__linked_objs[link.name] = list()        
            
            
    def link_and_validate(self):
        '''Check for attribute errors'''
        
        # Reset link errors
        self._link_errors = list()
        
        # Resolve links
        for link in list(self.__link_defs.values()):
            if not link.is_reverse:
                for linked_name in self._get_list_attr_values(link.attr_name):
                    
                    # Resolve link
                    linked_objs = list()
                    for doc_class in link.doc_classes:
                        try:
                            linked_objs.append(self.col.get(
                                doc_class, linked_name))
                        except IndexError:
                            pass
                    
                    # Handle named block not found
                    if len(linked_objs) == 0:
                        self._link_errors.append(MissingLinkError(
                            source_block=self,
                            link_name=link.name,
                            link_value=linked_name,
                            possible_doc_types=link.doc_classes))
                        
#                         msg = "Reference not found from %s to %s in (%s)"
#                         raise DocBlockStructureError(msg % (
#                             self.full_name,
#                             linked_name,
#                             ", ".join(link.doc_classes)))

                    elif len(linked_objs) > 1:
                        msg = "Reference from %s to %s in (%s) "
                        msg += "matched multiple blocks: %s"
                        raise DocBlockStructureError(msg % (
                            self.full_name,
                            linked_name,
                            ", ".join(link.doc_classes),
                            ", ".join([o.full_name for o in linked_objs])))
                                    
                    # print "%s.%s -> %s" % (self.full_name, link.name,
                    #     ", ".join([str(i) for i in linked_objs]))
                    
                    if len(linked_objs) > 0:
                        self.__linked_objs[link.name].append(ref(linked_objs[0]))
                    
                        # Record reverse link
                        linked_objs[0].__record_rev_link(self, link.name)
                    
        # Check for too many links
        for link in list(self.__link_defs.values()):
            if not link.is_reverse:
                if not link.multiple:
                    if len(self.__linked_objs[link.name]) > 1:
                        msg = "Link %s (from attribute %s) on %s "
                        msg += " linked to too many blocks"
                        raise DocBlockStructureError(msg % (link.name,
                                                            link.attr_name,
                                                            self.full_name))
            
        
        # Check for expected attributes
        for attr_def in list(self.__attr_defs.values()):
            if attr_def.expected:
                if attr_def.name not in self.__attr_values:
                    msg = "Doc block %s is missing required attribute [%s]\n"
                    msg += "Defined at:\n"
                    for raw_block in self.__raw:
                        msg += " - " + raw_block.loc + "\n"
                    raise DocBlockStructureError(msg % (self.full_name,
                                                        attr_def.name))
        
        # Report Link Errors
        for link_error in self._link_errors:
            print(self.full_name + ": " + str(link_error)) 
            
            
    def __record_rev_link(self, linking_block, link_name):
        
        # Find reverse link definition
        for link_def in list(self.__link_defs.values()):
            if link_def.is_reverse:
                for sel_doc_class, sel_link_name in link_def.linking:
                    if linking_block.doc_class == sel_doc_class:
                        if link_name == sel_link_name:
                            link = ref(linking_block)
                            self.__linked_objs[link_def.name].append(link)
                            return
                    
        # No reverse link defined
        msg = "Block %s linked to block %s, but reverse link"
        msg += " not defined.  To enable, add to __init__() of %s: "
        msg += "self._def_reverse_link(name, '%s', '%s')"
        print("WARNING: " + msg % (linking_block.full_name,
                                   self.full_name,
                                   self.__class__.__name__,
                                   linking_block.doc_class,
                                   link_name))
            
    
    def _take_attributes_from(self, raw_doc_block):
        '''Incorporate attribute values from a raw_doc_block'''
        
        self.__raw.append(raw_doc_block)
        
        if raw_doc_block.doc_class != self.__doc_class:
            msg = "doc block class is [%s], this is [%s]"
            raise Exception(msg % (raw_doc_block.doc_class, self.__doc_class))
        
        if raw_doc_block.name != self.__name:
            msg = "doc block name is [%s], this is [%s]"
            raise Exception(msg % (raw_doc_block.name, self.name))
        
        for attribute in raw_doc_block.attributes:
            if attribute.name in self.__attr_values:
                msg = "Overwriting attribute [%s] with value from %s. "
                msg += "previously set at %s"
                print("WARNING:", msg % (attribute.full_name,
                                         raw_doc_block.loc,
                                         self.__attr_values[attribute.name].loc))
                
            # Normal Attributes
            if attribute.name in self.__attr_defs:
                
                # Translate value
                attribute.value = self._translate_attr_value(
                    attribute.name, attribute.value)
                
                # Validate value
                emsg = self._validate_value(attribute.name, attribute.value)
                if emsg is None:
                    # Validate type
                    try:
                        attribute.value = self._validate_value_class(
                            attribute.name, attribute.value)
                    except InvalidAttributeValueClass as e:
                        emsg = str(e)
                        
                if emsg is not None:
                    msg = "ERROR: Value '%s' failed validation for '%s.%s': %s"
                    msg += "\n(ignoring value)"
                    try:
                        value = str(attribute.value)
                    except UnicodeEncodeError as e:
                        value = str(e)
                    print(msg % (value, self.full_name, attribute.name, emsg))
                
                else:
                    self.__attr_values[attribute.name] = attribute
                    
            # Embedded blocks
            elif attribute.name in self.__embedded_blocks_attrs:
                emsg = self._validate_value(attribute.name, attribute.value)
                if emsg is not None:
                    msg = "ERROR: Value '%s' failed validation for '%s.%s': %s"
                    msg += "\n(ignoring value)"
                    try:
                        value = str(attribute.value)
                    except UnicodeEncodeError as e:
                        value = str(e)
                    print(msg % (value, self.full_name, attribute.name, emsg))
                else:
                    self.__attr_values[attribute.name] = attribute
                
            
            # Unknown attribute
            else:
                msg = "WARNING: Ignoring unknown attribute %s set at %s"
                print(msg % (attribute.full_name, attribute.loc))
                
    
    
    def _get_list_attr_values(self, name):
        '''Return each item of an attribute that can have multiple values'''
        if name in self.__attr_values:
            return self.__attr_values[name].value_as_list
        return list()
        
        
    # Auto-resolve attribute names
    def __getattr__(self, name):
        
        if name.startswith("_"):
            raise AttributeError("Unknown attribute: %s.%s" % (
            self.__class__.__name__, name))
        
        # Check for transitive properties
        if name in self.__trans_properties:
            return self._get_transitive_property(name)
        
        # Check for links to objects from _def_link() and _def_reverse_link()
        if name in self.__link_defs:
            return self._get_linked_attribute_value(name)
         
        # Use attribute names from _def_attribute()
        if name in self.__attr_defs:
            return self._get_attribute_value(name)
                        
        raise AttributeError("Unknown attribute: %s.%s" % (
            self.__class__.__name__, name))
        
        
    def _get_transitive_property(self, name):
        prop = self.__trans_properties[name]
        return self.__resolve_transitive_property(prop.property_chain)
        
                
    def __resolve_transitive_property(self, property_chain):
        if len(property_chain) == 1:
            return getattr(self, property_chain[0])
        else:
            next_prop_name = property_chain[0]
            if next_prop_name in self.__link_defs:
                if not self.__link_defs[next_prop_name].multiple:
                    next_obj = getattr(self, next_prop_name)
                    if next_obj is None:
                        return None
                    chain = property_chain[1:]
                    return next_obj.__resolve_transitive_property(chain)
                else:
                    msg = "Transitive property can't use link %s.%s"
                    msg += " since allows multiple targets"
                    raise Exception(msg % (self.doc_class, next_prop_name))
            else:
                msg = "Transitive property can't use %s.%s"
                msg += " since no link exists with that name"
                raise Exception(msg % (self.doc_class, next_prop_name))
            
            
    def _get_linked_attribute_value(self, name):
            link = self.__link_defs[name]
            if link.is_reverse or  link.multiple:
                return [r() for r in self.__linked_objs[name]]
            else:
                if len(self.__linked_objs[name]) == 1:
                    return self.__linked_objs[name][0]()
                return None
    
    
    def _get_attribute_value(self, name):
        '''Return value stored for attribute (ignores links, transitive, etc)'''
        attr_def = self.__attr_defs[name]
        if name in self.__attr_values:
            value = self.__attr_values[name].value
            if attr_def.markdown:
                md_text = markdown2.markdown(
                    text = value,
                    extras = [
                        'code-friendly',
                        'fenced-code-blocks',
                        'tables',
                        ])
                # If value is just a <p>..</p>, then strip paragraph tags
                if md_text.strip().startswith('<p>'):
                    if md_text.strip().endswith('</p>'):
                        inner_text = md_text.strip()[3:-4]
                        if '<' not in inner_text:
                            if '>' not in inner_text:
                                md_text = inner_text
                # Wrap in div
                value = "<div class='markdown'>%s</div>" % (md_text)
            return value
        else:
            return attr_def.default_value
    
    
    
    def get_todo_items(self):
        '''Report tasks that need to be completed to complete documentation'''
        if False:
            yield None
            
            
    def _get_link_errors_as_todo(self):
        for link_error in self._link_errors:
            yield TodoItem(
                str(link_error),
                level = TodoItem.HIGH_LVL,
                sort_order = -10)
                    
            
    def _get_all_todo_items(self):
        '''Get todo items defined in child class and this class'''
        for todo_item in self.get_todo_items():
            yield todo_item
        
        for todo_item in self._get_link_errors_as_todo():
            yield todo_item

            
    
    def _translate_attr_value(self, field_name, value):
        '''Give code a chance to convert the value'''
        return value
            
            
    def _validate_value_class(self, field_name, value):
        '''Assert value class is valid.
        
        Raises InvalidAttributeValueClass if class is invalid.
        
        Can return a new value if class conversion is required
        '''
        if value is None:
            return None
        
        if field_name in self.__attr_defs:
            
            expected = self.__attr_defs[field_name].expected_class
            def validate_value(value, expected):
                if value.__class__ is not expected:
                    try:
                        value = expected(value)
                        return value
                    
                    except:
                        msg = "Field value has class %s, but expected %s"
                        raise InvalidAttributeValueClass(msg % (
                            value.__class__.__name__, expected.__name__))
                return value
            
            # Handle multiple values gracefully
            if value.__class__ is list:
                for i, sub_value in enumerate(value):
                    value[i] = validate_value(sub_value, expected)
                    
            # Else, assume a single value
            else:
                value = validate_value(value, expected)

            return value
                
        # Not sure when this will happen
        return value
            
            
    def _validate_value(self, field_name, value):
        '''Assert value valid.  If string is returned, attribute is dropped'''
        return None
            
    
    def get_todo_item_objs(self):
        for task in self._get_all_todo_items():
            if task.__class__ is str:
                task = TodoItem(task)
            task.doc_block = self
            yield task
        
            
    def all_todo_items_in_col(self):
        '''Get all todo items from the collection'''
        if 'todo' not in self.col.cache:
            # Search all doc blocks for TODO items
            self.col.cache['todo'] = list()
            for doc_block in self.col.get_all():
                for item in doc_block.get_todo_item_objs():
                    self.col.cache['todo'].append(item)
        return self.col.cache['todo'][:]
    
                
    def any_todo_items_in_col(self):
        '''Check to see if any blocks in the collection have todo items'''
        for task in self.all_todo_items_in_col():
            return True
        return False
        
        
    def print_doc_class_help(self):
        '''Print out doc class meaning and attributes to help developer'''
        
        def print_with_indent(line, wrap_at, indent_len):
            '''Print a line with wordwrap, indenting lines under the first'''
            
            # Wrap first line at wrap_at
            lines = wrap(line, wrap_at)
            print(lines[0])
            
            # Re-wrap remaining lines at wrap_at - indent_len
            lines = wrap("\n".join(lines[1:]), wrap_at - indent_len)
            for line in lines:
                print(" "*indent_len, line)
            
        
        wrap_at=79
        indent_len=26
        
        print_with_indent("[%s]  %s" % (self.__class__.__name__, self.__doc__),
                          wrap_at, 0)
        
        # Attributes
        print("  Attributes:")
        for attr_name in self.__attr_order:
            attr = self.__attr_defs[attr_name]
            name = attr.name
            if attr.expected:
                name += ' *'
            
            help_text = attr.help
            addl_help = list()
            if attr.markdown:
                addl_help.append("MD")
            for link_def in list(self.__link_defs.values()):
                if not link_def.is_reverse:
                    if link_def.attr_name == attr.name:
                        doc_classes = '|'.join(link_def.doc_classes)
                        addl_help.append("Links to %s" % (doc_classes))
                if link_def.name == attr.name:
                    addl_help.append("Hidden by link")
            if len(addl_help) > 0:
                help_text += ' (%s)' % (', '.join(addl_help))
            
            print_with_indent("    %-20s - %s" % (name, help_text),
                              wrap_at, indent_len)
        
        # Transitive Properties
        if len(self.__trans_properties) > 0:
            for prop in list(self.__trans_properties.values()):
                msg = "    %-20s - %s"
                print_with_indent(msg % (
                    prop.name,
                    '.'.join(prop.property_chain)),
                    wrap_at, indent_len)
            
        # Links
        links = [l for l in list(self.__link_defs.values()) if not l.is_reverse]
        if len(links) > 0:
            print("  Links:")
            for link_def in links:
                doc_classes = '|'.join(link_def.doc_classes)
                multiplicty = '(*)'
                if not link_def.multiple:
                    multiplicty = '(1)'
                msg = "    %-20s - Get linked %s %s through %s"
                print_with_indent(msg % (link_def.name,
                    doc_classes, multiplicty, link_def.attr_name),
                    wrap_at, indent_len)
            
        # Reversed Links
        links = [l for l in list(self.__link_defs.values()) if l.is_reverse]
        if len(links) > 0:
            print("  Reversed Links:")
            for link_def in links:
                sources = ['%s.%s' % (c, n) for c, n in link_def.linking]
                msg = "    %-20s - Get objects linking from %s"
                print_with_indent(msg % (link_def.name, ', '.join(sources)),
                    wrap_at, indent_len)
                
        print("")
        
        
    def list_all_attribute_names(self):
        yielded = set()
        for name in self._list_all_attribute_names():
            if name not in yielded:
                yield name
                yielded.add(name)


    def _list_all_attribute_names(self):
        # Standard attributes
        for name in self.__attr_order:
            yield name
            
        # Transitive properties
        for prop in list(self.__trans_properties.values()):
            yield prop.name
            
        # Links
        for link in list(self.__link_defs.values()):
            yield link.name
            
            