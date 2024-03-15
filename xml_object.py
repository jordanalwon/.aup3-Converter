import struct

class XMLObject():
    def __init__(self, binary_stream, object_names):
        self.binary_stream = binary_stream
        self.object_names = object_names
        self.string_block_size = self.object_names['string_block_size']

        while bool(self.binary_stream):
            indecator = self._indecator()

            if indecator ==  1:
                obj_name = self._object_name()
                if hasattr(self, obj_name):
                    if type(getattr(self, obj_name)) == list:
                        getattr(self,obj_name).append(XMLObject(self.binary_stream, self.object_names))
                    else:
                        setattr(self, obj_name, [getattr(self,obj_name),XMLObject(self.binary_stream, self.object_names)])
                else:
                    setattr(self, obj_name, XMLObject(self.binary_stream, self.object_names))
            elif indecator == 2:
                self.binary_stream(2)
                break
            elif indecator == 3:
                obj_name = self._object_name()
                text = self._text(self._block_length())
                setattr(self, obj_name, text)
            elif indecator == 4:
                obj_name = self._object_name()
                value = self._integer()
                setattr(self, obj_name, value)
            elif indecator == 5:
                obj_name = self._object_name()
                boolean = self._bool()
                setattr(self, obj_name, boolean)
            elif indecator == 6:
                obj_name = self._object_name()
                value = self._integer()
                setattr(self,obj_name, value)
            elif indecator == 7:
                obj_name = self._object_name()
                long = self._long_long()
                setattr(self, obj_name, long)
            elif indecator == 8:
                obj_name = self._object_name()
                value = self._integer()
                setattr(self, obj_name, value)
            elif indecator == 10:
                obj_name = self._object_name()
                value = self._double()
                setattr(self, obj_name, value)
                self.binary_stream(4) # Skip unknown sequence (FFFF) TODO
            elif indecator == 12:
                obj_name = "head"
                text = self._text(self._block_length())
                if hasattr(self,obj_name):
                    self.head += text
                else:
                    setattr(self,obj_name, text)
            else:
                raise ValueError("Unknown Indecator!")

    def _indecator(self):
        return struct.unpack('B', self.binary_stream(1))[0]
    
    def _object_name(self):
        obj_nr = struct.unpack('H', self.binary_stream(2))[0]

        return self.object_names[obj_nr]
    
    def _block_length(self):
        return self._integer()
    def _text(self, l):
        s = ''
        for _ in range(l//self.string_block_size):
            s += struct.unpack('s', self.binary_stream(self.string_block_size)[:1])[0].decode(encoding='iso-8859-1')
        
        return s
    
    def _integer(self):
        return struct.unpack('i', self.binary_stream(4))[0]
    
    def _long_long(self):
        return struct.unpack('Q', self.binary_stream(8))[0]
    
    def _double(self):
        return struct.unpack('d', self.binary_stream(8))[0]

    def _bool(self):
        return struct.unpack('?', self.binary_stream(1))[0]
    
    def todict(self):
        variables = {}

        for key, value in self.__dict__.items():
            if key in ['binary_stream', 'object_names']:
                continue
            
            if type(value) in [str, int, float, bool, bytes]:
                pass
            elif type(value) == list:
                value = [item.todict() for item in value]

            else:
                value = value.todict()

            variables[key] = value

        return variables