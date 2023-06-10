class Client:
    def __init__(self, CID, data):
        self.CID = CID
        self.data = data


class Product:
    def __init__(self, PID, data):
        self.PID = PID
        self.data = data


class Order:
    def __init__(self, OID, CID, data):
        self.OID = OID
        self.CID = CID
        self.data = data


class Reply:
    def __init__(self, error, description=None):
        self.error = error
        self.description = description


class ID:
    def __init__(self, ID):
        self.ID = ID
