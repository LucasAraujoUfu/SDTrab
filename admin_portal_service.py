import admin_pb2
import lmdb
import pysyncobj
import json
from admin_pb2_grpc import AdminPortalServicer
from messages import Client, Product


class AdminPortalService(AdminPortalServicer):
    def __init__(self):
        self.clients = {}
        self.products = {}
        self.db_path = None
        self.db = None
        self.sync_obj = None

    def __enter__(self):
        self.db = lmdb.open(self.db_path, map_size=10485760)
        self.sync_obj = pysyncobj.SyncObj("0.0.0.0:12345", [self.db], use_fsync=True)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()
        self.sync_obj.stop()

    def CreateClient(self, request, context):
        try:
            client = Client(request.CID, request.data)

            client_json = json.dumps(client.to_dict())

            with self.db.begin(write=True) as txn:
                txn.put(client.CID.encode(), client_json.encode())

            return admin_pb2.Reply(error=0)
        except lmdb.Error:
            return admin_pb2.Reply(error=1, description="Database Error")

    def RetrieveClient(self, request, context):
        try:
            with self.db.begin() as txn:
                client_json = txn.get(request.ID.encode())

            if client_json:
                client_dict = json.loads(client_json.decode())
                client = Client(client_dict['CID'], client_dict['data'])
                return admin_pb2.Client(CID=client.CID, data=client.data)
            else:
                return None
        except lmdb.Error:
            return None

    def UpdateClient(self, request, context):
        try:
            with self.db.begin(write=True) as txn:
                client_json = txn.get(request.CID.encode())

                if not client_json:
                    return admin_pb2.Reply(error=1, description="Client not found")

                client_dict = json.loads(client_json.decode())
                client_dict["data"] = request.data

                txn.put(request.CID.encode(), json.dumps(client_dict).encode())

            return admin_pb2.Reply(error=0)
        except lmdb.Error:
            return admin_pb2.Reply(error=1, description="Client not found")

    def DeleteClient(self, request, context):
        try:
            with self.db.begin(write=True) as txn:
                client_json = txn.pop(request.ID.encode(), None)

                if not client_json:
                    return admin_pb2.Reply(error=1, description="Client not found")

                return admin_pb2.Reply(error=0)
        except lmdb.Error:
            return admin_pb2.Reply(error=1, description="Client not found")

    def CreateProduct(self, request, context):
        try:
            product = Product(request.PID, request.data)

            product_json = json.dumps(product.to_dict())

            with self.db.begin(write=True) as txn:
                txn.put(product.PID.encode(), product_json.encode())

            return admin_pb2.Reply(error=0)
        except lmdb.Error:
            return admin_pb2.Reply(error=1, description="Database Error")

    def RetrieveProduct(self, request, context):
        try:
            with self.db.begin() as txn:
                product_json = txn.get(request.ID.encode())

            if product_json:
                product_dict = json.loads(product_json.decode())
                product = Product(product_dict['PID'], product_dict['data'])
                return admin_pb2.Product(PID=product.PID, data=product.data)
            else:
                return None
        except lmdb.Error:
            return None

    def UpdateProduct(self, request, context):
        try:
            with self.db.begin(write=True) as txn:
                product_json = txn.get(request.ID.encode())

                if not product_json:
                    return admin_pb2.Reply(error=1, description="Product not found")

                product_dict = json.loads(product_json.decode())

                txn.put(request.PID.encode(), json.dumps(product_dict).encode())

            return admin_pb2.Reply(error=0)
        except lmdb.Error:
            return admin_pb2.Reply(error=1, description="Product not found")

    def DeleteProduct(self, request, context):
        try:
            with self.db.begin(write=True) as txn:
                product_json = txn.pop(request.ID.encode(), None)

                if not product_json:
                    return admin_pb2.Reply(error=1, description="Product not found")

            return admin_pb2.Reply(error=0)

        except lmdb.Error:
            return admin_pb2.Reply(error=1, description="Product not found")

