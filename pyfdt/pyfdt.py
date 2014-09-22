# -*- coding: utf-8 -*-
"""
Device Tree Blob Parser

   Copyright 2014  Neil 'superna' Armstrong <superna9999@gmail.com>

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

@author: Neil 'superna' Armstrong <superna9999@gmail.com>
"""

import string
from struct import Struct, unpack, pack

FDT_MAGIC = 0xd00dfeed
FDT_BEGIN_NODE = 0x1
FDT_END_NODE = 0x2
FDT_PROP = 0x3
FDT_NOP = 0x4
FDT_END = 0x9

INDENT = ' ' * 4

FDT_MAX_VERSION = 17


class FdtProperty(object):
    """ Represents an empty property"""

    def __init__(self, name):
        """Init with name"""
        self.name = name

    def get_name(self):
        """Get property name"""
        return self.name

    def dts_represent(self, depth=0):
        """Get dts string representation"""
        return INDENT*depth + self.name + ';'

    def dtb_represent(self, string_store, pos=0, version=17):
        """Get blob representation"""
        # print "%x:%s" % (pos, self)
        strpos = string_store.find(self.name+'\0')
        if strpos < 0:
            strpos = len(string_store)
            string_store += self.name+'\0'
        pos += 12
        return (pack('>III', FDT_PROP, 0, strpos),
                string_store, pos)

    @staticmethod
    def __check_prop_strings(value):
        """Check property string validity
           Python version of util_is_printable_string from dtc
        """
        pos = 0
        posi = 0
        end = len(value)
        
        if not len(value):
            return None
        
        if ord(value[-1]) > 0:
            return None

        while pos < end:
            posi = pos
            while pos < end and ord(value[pos]) > 0 \
                  and value[pos] in string.printable \
                  and value[pos] not in ('\r', '\n'):
                pos += 1

            if ord(value[pos]) > 0 or pos == posi:
                return None
            pos += 1

        return True

    @staticmethod
    def new_raw_property(name, raw_value):
        """Instantiate property with raw value type"""
        if FdtProperty.__check_prop_strings(raw_value):
            return FdtPropertyStrings.init_raw(name, raw_value)
        elif len(raw_value) and len(raw_value) % 4 == 0:
            return FdtPropertyWords.init_raw(name, raw_value)
        elif len(raw_value) and len(raw_value):
            return FdtPropertyBytes.init_raw(name, raw_value)
        else:
            return FdtProperty(name)


class FdtPropertyStrings(FdtProperty):
    """Property with strings as value"""

    @classmethod
    def __extract_prop_strings(cls, value):
        """Extract strings from raw_value"""
        return [st for st in value.split('\0') if len(st)]

    def __init__(self, name, strings):
        """Init with strings"""
        FdtProperty.__init__(self, name)
        if not strings:
            raise Exception("Invalid strings")
        self.strings = strings

    @classmethod
    def init_raw(cls, name, raw_value):
        """Init from raw"""
        return cls(name, cls.__extract_prop_strings(raw_value))

    def dts_represent(self, depth=0):
        """Get dts string representation"""
        return INDENT*depth + self.name + ' = "' + \
            '", "'.join(self.strings) + '";'

    def dtb_represent(self, string_store, pos=0, version=17):
        """Get blob representation"""
        # print "%x:%s" % (pos, self)
        blob = ''
        for chars in self.strings:
            blob += chars + '\0'
        blob_len = len(blob)
        if version < 16 and (pos+12) % 8 != 0:
            blob = '\0'*(8-((pos+12) % 8)) + blob
        if blob_len % 4:
            blob += '\0'*(4-(blob_len % 4))
        strpos = string_store.find(self.name+'\0')
        if strpos < 0:
            strpos = len(string_store)
            string_store += self.name+'\0'
        blob = pack('>III', FDT_PROP, blob_len, strpos) + blob
        pos += len(blob)
        return (blob, string_store, pos)

    def __str__(self):
        """String representation"""
        return "Property(Strings:%s)" % self.strings

    def __getattr__(self, index):
        """Get strings"""
        return getattr(self.strings, index)

    def __len__(self):
        """Get strings count"""
        return len(self.strings)


class FdtPropertyWords(FdtProperty):
    """Property with words as value"""

    def __init__(self, name, words):
        """Init with words"""
        FdtProperty.__init__(self, name)
        if not len(words):
            raise Exception("Invalid Words")
        self.words = words

    @classmethod
    def init_raw(cls, name, raw_value):
        """Init from raw"""
        if len(raw_value) % 4 == 0:
            words = [unpack(">I", raw_value[i:i+4])[0]
                     for i in range(0, len(raw_value), 4)]
            return cls(name, words)
        else:
            raise Exception("Invalid raw Words")

    def dts_represent(self, depth=0):
        """Get dts string representation"""
        return INDENT*depth + self.name + ' = <' + \
               ' '.join(["0x%08x" % word for word in self.words]) + ">;"

    def dtb_represent(self, string_store, pos=0, version=17):
        """Get blob representation"""
        # # print "%x:%s" % (pos, self)
        strpos = string_store.find(self.name+'\0')
        if strpos < 0:
            strpos = len(string_store)
            string_store += self.name+'\0'
        blob = pack('>III', FDT_PROP, len(self.words)*4, strpos) + \
                ''.join([pack('>I', word) for word in self.words])
        pos += len(blob)
        return (blob, string_store, pos)

    def __str__(self):
        """String representation"""
        return "Property(Words:%s)" % self.words

    def __getattr__(self, index):
        """Get words"""
        return getattr(self.words, index)

    def __len__(self):
        """Get words count"""
        return len(self.words)


class FdtPropertyBytes(FdtProperty):
    """Property with bytes as value"""

    def __init__(self, name, bytez):
        """Init with bytes"""
        FdtProperty.__init__(self, name)
        if not bytez:
            raise Exception("Invalid Bytes")
        self.bytes = bytez

    @classmethod
    def init_raw(cls, name, raw_value):
        """Init from raw"""
        return cls(name, [unpack('b', byte)[0] for byte in raw_value])

    def dts_represent(self, depth=0):
        """Get dts string representation"""
        return INDENT*depth + self.name + ' = [' + \
            ' '.join(["%02x" % (byte & int('ffffffff',16)) 
                      for byte in self.bytes]) + "];"

    def dtb_represent(self, string_store, pos=0, version=17):
        """Get blob representation"""
        # print "%x:%s" % (pos, self)
        strpos = string_store.find(self.name+'\0')
        if strpos < 0:
            strpos = len(string_store)
            string_store += self.name+'\0'
        blob = pack('>III', FDT_PROP, len(self.bytes), strpos)
        blob += ''.join([pack('>b', byte) for byte in self.bytes])
        if len(blob) % 4:
            blob += '\0'*(4-(len(blob) % 4))
        pos += len(blob)
        return (blob, string_store, pos)

    def __str__(self):
        """String representation"""
        return "Property(Bytes:%s)" % self.bytes

    def __getattr__(self, index):
        """Get bytes"""
        return getattr(self.bytes, index)

    def __len__(self):
        """Get bytes count"""
        return len(self.bytes)


class FdtNop(object):  # pylint: disable-msg=R0903
    """Nop child representation"""

    def __init__(self):
        """Init with nothing"""

    def get_name(self):  # pylint: disable-msg=R0201
        """Return name"""
        return None

    def dts_represent(self, depth=0):  # pylint: disable-msg=R0201
        """Get dts string representation"""
        return INDENT*depth+'// [NOP]'

    def dtb_represent(self, string_store, pos=0, version=17):
        """Get blob representation"""
        # print "%x:%s" % (pos, self)
        pos += 4
        return (pack('>I', FDT_NOP), string_store, pos)


class FdtNode(object):
    """Node representation"""

    def __init__(self, name):
        """Init node with name"""
        self.name = name
        self.subdata = []
        self.parent = None

    def get_name(self):
        """Get property name"""
        return self.name

    def add_raw_attribute(self, name, raw_value):
        """Construct a raw attribute and add to child"""
        self.subdata.append(FdtProperty.new_raw_property(name, raw_value))

    def add_subnode(self, node):
        """Add child"""
        self.subdata.append(node)

    def set_parent_node(self, node):
        """Set parent node"""
        self.parent = node

    def get_parent_node(self):
        """Get parent node"""
        return self.parent

    def __str__(self):
        """String representation"""
        return "Node(%s)" % self.name

    def dts_represent(self, depth=0):
        """Get dts string representation"""
        result = ('\n').join([sub.dts_represent(depth+1)
                                         for sub in self.subdata])
        if len(result) > 0:
            result += '\n'
        return INDENT*depth + self.name + ' {\n' + \
               result + INDENT*depth + "};"

    def dtb_represent(self, strings_store, pos=0, version=17):
        """Get blob representation"""
        # print "%x:%s" % (pos, self)
        strings = strings_store
        if self.get_name() == '\\':
            blob = pack('>II', FDT_BEGIN_NODE, 0)
        else:
            blob = pack('>I', FDT_BEGIN_NODE)
            blob += self.get_name() + '\0'
        if len(blob) % 4:
            blob += '\0'*(4-(len(blob) % 4))
        pos += len(blob)
        for sub in self.subdata:
            (data, strings, pos) = sub.dtb_represent(strings, pos, version)
            blob += data
        pos += 4
        blob += pack('>I', FDT_END_NODE)
        return (blob, strings, pos)

    def __getattr__(self, index):
        """Get child attribute or node"""
        return getattr(self.subdata, index)

    def __len__(self):
        """Get child count"""
        return len(self.subdata)


class Fdt(object):
    """Flattened Device Tree representation"""

    def __init__(self, version=17, last_comp_version=16, boot_cpuid_phys=0):
        self.header = {'magic': FDT_MAGIC,
                       'totalsize': 0,
                       'off_dt_struct': 0,
                       'off_dt_strings': 0,
                       'off_mem_rsvmap': 0,
                       'version': version,
                       'last_comp_version': last_comp_version,
                       'boot_cpuid_phys': boot_cpuid_phys,
                       'size_dt_strings': 0,
                       'size_dt_struct': 0}
        self.rootnode = None
        self.prenops = None
        self.postnops = None
        self.reserve_entries = None

    def add_rootnode(self, rootnode, prenops=None, postnops=None):
        """Add root node"""
        self.rootnode = rootnode
        self.prenops = prenops
        self.postnops = postnops

    def add_reserve_entries(self, reserve_entries):
        """Add reserved entries as list of dict with
           'address' and 'size' keys"""
        self.reserve_entries = reserve_entries

    def to_dts(self):
        """Export to DTS representation in string format"""
        result = "/dts-v1/;\n"
        result += "// version:\t\t%d\n" % self.header['version']
        result += "// last_comp_version:\t%d\n" % \
                  self.header['last_comp_version']
        if self.header['version'] >= 2:
            result += "// boot_cpuid_phys:\t0x%x\n" % \
                self.header['boot_cpuid_phys']
        result += '\n'
        if self.reserve_entries is not None:
            for entry in self.reserve_entries:
                result += "/memreserve/ "
                if entry['address']:
                    result += "%#x " % entry['address']
                else:
                    result += "0 "
                if entry['size']:
                    result += "%#x" % entry['size']
                else:
                    result += "0"
                result += ";\n"
        if self.prenops:
            result += '\n'.join([nop.dts_represent() for nop in self.prenops])
            result += '\n'
        if self.rootnode is not None:
            result += self.rootnode.dts_represent()
        if self.postnops:
            result += '\n'
            result += '\n'.join([nop.dts_represent() for nop in self.postnops])
        return result

    def to_dtb(self):
        """Export to Blob format"""
        if self.rootnode is None or self.reserve_entries is None:
            return None
        blob_reserve_entries = ''
        if self.reserve_entries is not None:
            for entry in self.reserve_entries:
                blob_reserve_entries += pack('>QQ',
                                             entry['address'],
                                             entry['size'])
        blob_reserve_entries += pack('>QQ', 0, 0)
        header_size = 7 * 4
        if self.header['version'] >= 2:
            header_size += 4
        if self.header['version'] >= 3:
            header_size += 4
        if self.header['version'] >= 17:
            header_size += 4
        dt_start = header_size + len(blob_reserve_entries)
        # print "dt_start %d" % dt_start
        (blob_dt, blob_strings, dt_pos) = \
            self.rootnode.dtb_represent('', dt_start, self.header['version'])
        if self.prenops is not None:
            blob_dt = ''.join([nop.dtb_represent('')[0] 
                               for nop in self.prenops])\
                      + blob_dt
        if self.postnops is not None:
            blob_dt += ''.join([nop.dtb_represent('')[0] 
                                for nop in self.postnops])
        blob_dt += pack('>I', FDT_END)
        self.header['size_dt_strings'] = len(blob_strings)
        self.header['size_dt_struct'] = len(blob_dt)
        self.header['off_mem_rsvmap'] = header_size
        self.header['off_dt_struct'] = dt_start
        self.header['off_dt_strings'] = dt_start + len(blob_dt)
        self.header['totalsize'] = dt_start + len(blob_dt) + len(blob_strings)
        blob_header = pack('>IIIIIII', self.header['magic'],
                           self.header['totalsize'],
                           self.header['off_dt_struct'],
                           self.header['off_dt_strings'],
                           self.header['off_mem_rsvmap'],
                           self.header['version'],
                           self.header['last_comp_version'])
        if self.header['version'] >= 2:
            blob_header += pack('>I', self.header['boot_cpuid_phys'])
        if self.header['version'] >= 3:
            blob_header += pack('>I', self.header['size_dt_strings'])
        if self.header['version'] >= 17:
            blob_header += pack('>I', self.header['size_dt_struct'])
        return blob_header + blob_reserve_entries + blob_dt + blob_strings


class FdtBlobParse(object):  # pylint: disable-msg=R0903
    """Parse from file input"""

    __fdt_header_format = ">IIIIIII"
    __fdt_header_names = ('magic', 'totalsize', 'off_dt_struct',
                          'off_dt_strings', 'off_mem_rsvmap', 'version',
                          'last_comp_version')

    __fdt_reserve_entry_format = ">QQ"
    __fdt_reserve_entry_names = ('address', 'size')

    __fdt_dt_cell_format = ">I"
    __fdt_dt_prop_format = ">II"
    __fdt_dt_tag_name = {FDT_BEGIN_NODE: 'node_begin',
                         FDT_END_NODE: 'node_end',
                         FDT_PROP: 'prop',
                         FDT_NOP: 'nop',
                         FDT_END: 'end'}

    def __extract_fdt_header(self):
        """Extract DTB header"""
        header = Struct(self.__fdt_header_format)
        header_entry = Struct(">I")
        data = self.infile.read(header.size)
        result = dict(zip(self.__fdt_header_names, header.unpack_from(data)))
        if result['version'] >= 2:
            data = self.infile.read(header_entry.size)
            result['boot_cpuid_phys'] = header_entry.unpack_from(data)[0]
        if result['version'] >= 3:
            data = self.infile.read(header_entry.size)
            result['size_dt_strings'] = header_entry.unpack_from(data)[0]
        if result['version'] >= 17:
            data = self.infile.read(header_entry.size)
            result['size_dt_struct'] = header_entry.unpack_from(data)[0]
        return result

    def __extract_fdt_reserve_entries(self):
        """Extract reserved memory entries"""
        header = Struct(self.__fdt_reserve_entry_format)
        entries = []
        self.infile.seek(self.fdt_header['off_mem_rsvmap'])
        while True:
            data = self.infile.read(header.size)
            result = dict(zip(self.__fdt_reserve_entry_names,
                              header.unpack_from(data)))
            if result['address'] == 0 and result['size'] == 0:
                return entries
            entries.append(result)

    def __extract_fdt_nodename(self):
        """Extract node name"""
        data = ''
        pos = self.infile.tell()
        while True:
            byte = self.infile.read(1)
            if ord(byte) == 0:
                break
            data += byte
        align_pos = pos + len(data) + 1
        align_pos = (((align_pos) + ((4) - 1)) & ~((4) - 1))
        self.infile.seek(align_pos)
        return data

    def __extract_fdt_string(self, prop_string_pos):
        """Extract string from string pool"""
        data = ''
        pos = self.infile.tell()
        self.infile.seek(self.fdt_header['off_dt_strings']+prop_string_pos)
        while True:
            byte = self.infile.read(1)
            if ord(byte) == 0:
                break
            data += byte
        self.infile.seek(pos)
        return data

    def __extract_fdt_prop(self):
        """Extract property"""
        prop = Struct(self.__fdt_dt_prop_format)
        pos = self.infile.tell()
        data = self.infile.read(prop.size)
        (prop_size, prop_string_pos,) = prop.unpack_from(data)

        prop_start = pos + prop.size
        if self.fdt_header['version'] < 16 and prop_size >= 8:
            prop_start = (((prop_start) + ((8) - 1)) & ~((8) - 1))

        self.infile.seek(prop_start)
        value = self.infile.read(prop_size)

        align_pos = self.infile.tell()
        align_pos = (((align_pos) + ((4) - 1)) & ~((4) - 1))
        self.infile.seek(align_pos)

        return (self.__extract_fdt_string(prop_string_pos), value)

    def __extract_fdt_dt(self):
        """Extract tags"""
        cell = Struct(self.__fdt_dt_cell_format)
        tags = []
        self.infile.seek(self.fdt_header['off_dt_struct'])
        while True:
            data = self.infile.read(cell.size)
            if len(data) < cell.size:
                break
            tag, = cell.unpack_from(data)
            # print "*** %s" % self.__fdt_dt_tag_name.get(tag, '')
            if self.__fdt_dt_tag_name.get(tag, '') in 'node_begin':
                name = self.__extract_fdt_nodename()
                if len(name) == 0:
                    name = '/'
                tags.append((tag, name))
            elif self.__fdt_dt_tag_name.get(tag, '') in ('node_end', 'nop'):
                tags.append((tag, ''))
            elif self.__fdt_dt_tag_name.get(tag, '') in 'end':
                tags.append((tag, ''))
                break
            elif self.__fdt_dt_tag_name.get(tag, '') in 'prop':
                propdata = self.__extract_fdt_prop()
                tags.append((tag, propdata))
            else:
                print "Unknown Tag %d" % tag
        return tags

    def __init__(self, infile):
        """Init with file input"""
        self.infile = infile
        self.fdt_header = self.__extract_fdt_header()
        if self.fdt_header['magic'] != FDT_MAGIC:
            raise Exception('Invalid Magic')
        if self.fdt_header['version'] > FDT_MAX_VERSION:
            raise Exception('Invalid Version %d' % self.fdt_header['version'])
        if self.fdt_header['last_comp_version'] > FDT_MAX_VERSION-1:
            raise Exception('Invalid last compatible Version %d' %
                            self.fdt_header['last_comp_version'])
        self.fdt_reserve_entries = self.__extract_fdt_reserve_entries()
        self.fdt_dt_tags = self.__extract_fdt_dt()

    def __to_nodes(self):
        """Represent fdt as Node and properties structure
           Returns a set with the pre-node Nops, the Root Node,
            and the post-node Nops.
        """
        prenops = []
        postnops = []
        rootnode = None
        curnode = None
        for tag in self.fdt_dt_tags:
            if self.__fdt_dt_tag_name.get(tag[0], '') in 'node_begin':
                newnode = FdtNode(tag[1])
                if rootnode is None:
                    rootnode = newnode
                if curnode is not None:
                    curnode.add_subnode(newnode)
                    newnode.set_parent_node(curnode)
                curnode = newnode
            elif self.__fdt_dt_tag_name.get(tag[0], '') in 'node_end':
                if curnode is not None:
                    curnode = curnode.get_parent_node()
            elif self.__fdt_dt_tag_name.get(tag[0], '') in 'nop':
                if curnode is not None:
                    curnode.add_subnode(FdtNop())
                elif rootnode is not None:
                    postnops.append(FdtNop())
                else:
                    prenops.append(FdtNop())
            elif self.__fdt_dt_tag_name.get(tag[0], '') in 'prop':
                if curnode is not None:
                    curnode.add_raw_attribute(tag[1][0], tag[1][1])
            elif self.__fdt_dt_tag_name.get(tag[0], '') in 'end':
                continue
        return (prenops, rootnode, postnops)

    def to_fdt(self):
        """Create a fdt object
            Returns a Fdt object
        """
        if self.fdt_header['version'] >= 2:
            boot_cpuid_phys = self.fdt_header['boot_cpuid_phys']
        else:
            boot_cpuid_phys = 0
        fdt = Fdt(version=self.fdt_header['version'],
                  last_comp_version=self.fdt_header['last_comp_version'],
                  boot_cpuid_phys=boot_cpuid_phys)
        (prenops, rootnode, postnops) = self.__to_nodes()
        fdt.add_rootnode(rootnode, prenops=prenops, postnops=postnops)
        fdt.add_reserve_entries(self.fdt_reserve_entries)
        return fdt
