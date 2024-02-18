class BinaryStream():
    index = 0

    def __init__(self, path):
        # Read binary
        with open(path, 'rb') as file:
            self.data = file.read()

    def __len__(self):
        return len(self.data)

    def __call__(self, l):
        output = self.data[self.index:self.index+l]
        self.index += l

        return output
    
    def __bool__(self):
        return self.index < len(self.data)