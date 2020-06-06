from hashlib import md5

class VerticaWireHandler():
    
    """To build out as an actual handler when more is added--for now, string conversion. For now, pretty gratuituous """
    
    def __init__(self, data):
        self.data = data
        
        
    @property
    def message(self):
        return self.data[5:-1].decode().upper()
    
    @property
    def message_length_bytes(self):
        return self.data[1:5]
        
    @property
    def key(self):
        return md5(self.data[5:-1]).hexdigest()

    @property
    def message_type(self):
        return self.data[0]