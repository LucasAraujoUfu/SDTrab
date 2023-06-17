import admin_pb2
import lmdb
import pysyncobj
import json
from messages import Order


class OrderPortalService:
    def __init__(self):
        self.orders = {}

    def __enter__(self):
        self.db = lmdb.open(self.db_path, map_size=10485760)
        self.sync_obj = pysyncobj.SyncObj("0.0.0.0:12345", [self.db], use_fsync=True)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()
        self.sync_obj.stop()

    def CreateOrder(self, request, context):
        # TODO: validar CID
        try:
            order = Order(request.OID, request.CID, request.data)

            order_json = json.dumps(order.to_dict())

            with self.db.begin(write=True) as txn:
                txn.put(order.OID.encode(), order_json.encode())

            return admin_pb2.Reply(error=0)
        except lmdb.Error:
            return admin_pb2.Reply(error=1, description="Database Error")

    def RetrieveOrder(self, request, context):
        with self.db.begin() as txn:
            order_json = txn.get(request.ID.encode())

        if order_json:
            order_dict = json.loads(order_json.decode())
            order = Order(order_dict['OID'], order_dict['CID'], order_dict['data'])
            return admin_pb2.Order(OID=order.OID, CID=order.CID, data=order.data)
        else:
            return None

    def UpdateOrder(self, request, context):
        # TODO: validar CID
        with self.db.begin(write=True) as txn:
            order_json = txn.get(request.OID.encode())

            if not order_json:
                return admin_pb2.Reply(error=1, description="Order not found")

            order_dict = json.loads(order_json.decode())
            order_dict["CID"] = request.CID
            order_dict["data"] = request.data

            txn.put(request.OID.encode(), json.dumps(order_dict).encode())

        return admin_pb2.Reply(error=0)

    def DeleteOrder(self, request, context):
        with self.db.begin(write=True) as txn:
            order_json = txn.pop(request.ID.encode(), None)

            if not order_json:
                return admin_pb2.Reply(error=1, description="Order not found")

        return admin_pb2.Reply(error=0)

    def RetrieveClientOrders(self, request, context):
        # TODO: essa função inteira
        for order in self.orders.values():
            if order.CID == request.ID:
                yield order
