import admin_pb2
from messages import Order, Reply, ID


class OrderPortalService:
    def __init__(self):
        self.orders = {}

    def CreateOrder(self, request, context):
        order = Order(request.OID, request.CID, request.data)
        self.orders[order.OID] = order
        return admin_pb2.Reply(error=0)

    def RetrieveOrder(self, request, context):
        order = self.orders.get(request.ID)
        if order:
            return admin_pb2.Order(OID=order.OID, CID=order.CID, data=order.data)
        else:
            return None

    def UpdateOrder(self, request, context):
        order = self.orders.get(request.OID)
        if order:
            order.CID = request.CID
            order.data = request.data
            return admin_pb2.Reply(error=0)
        else:
            return admin_pb2.Reply(error=1, description="Order not found")

    def DeleteOrder(self, request, context):
        order = self.orders.pop(request.ID, None)
        if order:
            return admin_pb2.Reply(error=0)
        else:
            return admin_pb2.Reply(error=1, description="Order not found")

    def RetrieveClientOrders(self, request, context):
        for order in self.orders.values():
            if order.CID == request.ID:
                yield order
