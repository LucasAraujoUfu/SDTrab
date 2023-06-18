import admin_pb2
import lmdb
import pysyncobj
import json
from messages import Order


class OrderPortalService:
    def __init__(self):
        self.orders = {}
        self.db_path = 'database/'
        self.db = lmdb.open(self.db_path, map_size=10485760)

    def CreateOrder(self, request, context):
        # TODO: validar CID
        try:
            order = Order(request.OID, request.CID, request.data)

            order_json = json.dumps({'OID': order.OID, 'CID': order.CID, 'data': order.data})

            with self.db.begin(write=True) as txn:
                client = txn.get(order.CID.encode())

                if not client:
                    return admin_pb2.Reply(error=1, description="Client not found")

                txn.put(order.OID.encode(), order_json.encode())

            return admin_pb2.Reply(error=0)
        except lmdb.Error:
            return admin_pb2.Reply(error=1, description="Database Error")

    def RetrieveOrder(self, request, context):
        try:
            with self.db.begin() as txn:
                order_json = txn.get(request.ID.encode())

            if order_json:
                order_dict = json.loads(order_json.decode())
                order = Order(order_dict['OID'], order_dict['CID'], order_dict['data'])
                return admin_pb2.Order(OID=order.OID, CID=order.CID, data=order.data)
            else:
                return admin_pb2.Order(OID="", CID="", data="")
        except lmdb.Error:
            return admin_pb2.Order(OID="", CID="", data="")

    def UpdateOrder(self, request, context):
        try:
            with self.db.begin(write=True) as txn:
                order_json = txn.get(request.OID.encode())

                if not order_json:
                    return admin_pb2.Reply(error=1, description="Order not found")

                client = txn.get(request.CID.encode())

                if not client:
                    return admin_pb2.Reply(error=1, description="Client not found")

                order_dict = json.loads(order_json.decode())
                order_dict["CID"] = request.CID
                order_dict["data"] = request.data

                txn.put(request.OID.encode(), json.dumps(order_dict).encode())

            return admin_pb2.Reply(error=0)
        except lmdb.Error:
            return admin_pb2.Reply(error=1, description="Database Error")

    def DeleteOrder(self, request, context):
        try:
            with self.db.begin(write=True) as txn:
                order_json = txn.pop(request.ID.encode(), None)

                if not order_json:
                    return admin_pb2.Reply(error=1, description="Order not found")

            return admin_pb2.Reply(error=0)
        except lmdb.Error:
            return admin_pb2.Reply(error=1, description="Database Error")

    def RetrieveClientOrders(self, request, context):
        # TODO: essa função inteira
        for order in self.orders.values():
            if order.CID == request.ID:
                yield order
