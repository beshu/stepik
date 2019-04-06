import tempfile
from os import path

class File:
    
    def __init__(self, path):
        self.path = path
        self.name = self.path.split('/')[-1]
        
    def write(self, string):
        with open(self.path, 'a') as f:
            f.write(string)
            
    def read(self):
        with open(self.path, 'r') as f:
            return f.read()
        
    def __add__(self, other):
        name_string = 'file_from_{}_and_{}'.format(self.name, other.name)
        new_file_path = '{}/{}'.format(tempfile.gettempdir(), name_string)
        _new = File(new_file_path)
        with open(_new.path, 'w') as f:
            file_contents = '{}{}'.format(self.read(), other.read())
            f.write(file_contents)
        return _new
    
    def __repr__(self):
        return self.path
    
    def __iter__(self):
        with open(self.path, 'r') as f:
            yield f.readline()
