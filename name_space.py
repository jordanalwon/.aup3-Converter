import struct

class NameSpace():
    def __init__(self, binary_stream):
        self.binary_stream = binary_stream
        self.name_space = {}

        # Skip unkown start sequence
        self.binary_stream(2)

        while bool(self.binary_stream):
            indecator = self._indecator()

            if indecator == 15:
                index = self._index()
                l = self._block_length()
                text = self._text(l)

                self.name_space[index] = text
            else:
                raise ValueError("Unknown Indecator!")
            
    def __getitem__(self, index):
        return self.name_space[index]

    def _indecator(self):
        return struct.unpack('B', self.binary_stream(1))[0]
    
    def _index(self):
        return struct.unpack('H', self.binary_stream(2))[0]
    
    def _block_length(self):
        return struct.unpack('H', self.binary_stream(2))[0]
    
    def _text(self, l):
        s = ''
        for _ in range(l//2):
            s += struct.unpack('s', self.binary_stream(2)[:1])[0].decode(encoding='utf-8')   
        return s
