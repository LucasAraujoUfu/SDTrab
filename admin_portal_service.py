import admin_pb2
from admin_pb2_grpc import AdminPortalServicer
from messages import Client, Product


class AdminPortalService(AdminPortalServicer):
    def __init__(self):
        self.clients = {}
        self.products = {}

    def CreateClient(self, request, context):
        client = Client(request.CID, request.data)
        self.clients[client.CID] = client
        return admin_pb2.Reply(error=0)

    def RetrieveClient(self, request, context):
        cl = self.clients.get(request.ID)

        if cl:
            return admin_pb2.Client(CID=cl.CID, data=cl.data)
        else:
            return admin_pb2.Client(CID='', data='')

    def UpdateClient(self, request, context):
        client = self.clients.get(request.CID)
        if client:
            client.data = request.data
            return admin_pb2.Reply(error=0)
        else:
            return admin_pb2.Reply(error=1, description="Client not found")

    def DeleteClient(self, request, context):
        client = self.clients.pop(request.ID, None)
        if client:
            return admin_pb2.Reply(error=0)
        else:
            return admin_pb2.Reply(error=1, description="Client not found")

    def CreateProduct(self, request, context):
        product = Product(request.PID, request.data)
        self.products[product.PID] = product
        return admin_pb2.Reply(error=0)

    def RetrieveProduct(self, request, context):
        product = self.products.get(request.ID)
        if product:
            return admin_pb2.Product(PID=product.PID, data=product.data)
        else:
            return admin_pb2.Product(PID='', data='')

    def UpdateProduct(self, request, context):
        product = self.products.get(request.PID)
        if product:
            product.data = request.data
            return admin_pb2.Reply(error=0)
        else:
            return admin_pb2.Reply(error=1, description="Product not found")

    def DeleteProduct(self, request, context):
        product = self.products.pop(request.ID, None)
        if product:
            return admin_pb2.Reply(error=0)
        else:
            return admin_pb2.Reply(error=1, description="Product not found")
