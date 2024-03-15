import struct

class NameSpace():
    def __init__(self, binary_stream):
        self.binary_stream = binary_stream
        self.name_space = {}

        # Skip start element
        self.binary_stream(1)

        self.string_block_size = self._indecator()

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
        for _ in range(l//self.string_block_size):
            s += struct.unpack('s', self.binary_stream(self.string_block_size)[:1])[0].decode(encoding='utf-8')   # TODO why are string blocks 4 chars long and not 2? 2. file char as indecator?
        return s
