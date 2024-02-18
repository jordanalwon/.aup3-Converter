import struct

class XMLObject():
    def __init__(self, binary_stream, object_names):
        self.binary_stream = binary_stream
        self.object_names = object_names

        while bool(self.binary_stream):
            indecator = self._indecator()

            match indecator:
                case 1:
                    obj_name = self._object_name()
                    if hasattr(self, obj_name):
                        if type(getattr(self, obj_name)) == list:
                            getattr(self,obj_name).append(XMLObject(self.binary_stream, self.object_names))
                        else:
                            setattr(self, obj_name, [getattr(self,obj_name),XMLObject(self.binary_stream, self.object_names)])
                    else:
                        setattr(self, obj_name, XMLObject(self.binary_stream, self.object_names))
                case 2:
                    self.binary_stream(2)
                    break
                case 3:
                    obj_name = self._object_name()
                    text = self._text(self._block_length())
                    setattr(self, obj_name, text)
                case 4:
                    obj_name = self._object_name()
                    value = self._integer()
                    setattr(self, obj_name, value)
                case 5:
                    obj_name = self._object_name()
                    boolean = self._bool()
                    setattr(self, obj_name, boolean)
                case 6:
                    obj_name = self._object_name()
                    value = self._integer()
                    setattr(self,obj_name, value)
                case 7:
                    obj_name = self._object_name()
                    long = self._long_long()
                    setattr(self, obj_name, long)
                case 8:
                    obj_name = self._object_name()
                    value = self._integer()
                    setattr(self, obj_name, value)
                case 10:
                    obj_name = self._object_name()
                    value = self._double()
                    setattr(self, obj_name, value)
                    self.binary_stream(4) # Skip unknown sequence (FFFF) TODO
                case 12:
                    obj_name = "head"
                    text = self._text(self._block_length())
                    if hasattr(self,obj_name):
                        self.head += text
                    else:
                        setattr(self,obj_name, text)
                case _:
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
        for _ in range(l//2):
            s += struct.unpack('s', self.binary_stream(2)[:1])[0].decode(encoding='utf-8')
        
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