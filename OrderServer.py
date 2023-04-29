import grpc
import json
import service_pb2
import uuid
from concurrent import futures
from service_pb2_grpc import OrderPortal, add_OrderPortalServicer_to_server


class OrderPortalServ(OrderPortal):
    def CreateOrder(self, request, context):
        try:
            # Verifica se o cliente informado existe
            client = self._retrieve_client(request.CID)
            if not client:
                return service_pb2.Reply(error=1, description="Client not found")

            # Converte a string JSON com os detalhes do pedido em um dicionário Python
            order_data = json.loads(request.data)

            # Cria a ordem de compra
            order_id = str(uuid.uuid4())
            order = service_pb2.Order(OID=order_id, CID=request.CID, data=order_data)
            self.orders[order_id] = order

            # Retorna a resposta com sucesso
            return service_pb2.Reply(error=0)

        except Exception as e:
            return service_pb2.Reply(error=1, description=str(e))


    def RetrieveOrder(self, request, context):
        try:
            # Verifica se a ordem de compra solicitada existe
            order_id = request.ID
            if order_id not in self.orders:
                return service_pb2.Order()

            # Retorna a ordem de compra solicitada
            return self.orders[order_id].to_proto()

        except Exception as e:
            return service_pb2.Order()

    def UpdateOrder(self, request, context):
        try:
            # Verifica se a ordem de compra solicitada existe
            order_id = request.OID
            if order_id not in self.orders:
                return service_pb2.Reply(error=1, description="Order not found")

            # Atualiza a ordem de compra com os novos detalhes fornecidos
            order_data = json.loads(request.data)
            self.orders[order_id].update(order_data)

            # Retorna a resposta com sucesso
            return service_pb2.Reply(error=0)

        except Exception as e:
            return service_pb2.Reply(error=1, description=str(e))

    def DeleteOrder(self, request, context):
        try:
            # Verifica se a ordem de compra solicitada existe
            order_id = request.ID
            if order_id not in self.orders:
                return service_pb2.Reply(error=1, description="Order not found")

            # Remove a ordem de compra da lista
            del self.orders[order_id]

            # Retorna a resposta com sucesso
            return service_pb2.Reply(error=0)

        except Exception as e:
            return service_pb2.Reply(error=1, description=str(e))

    def RetrieveClientOrders(self, request, context):
        try:
            # Verifica se o cliente informado existe
            client = self._retrieve_client(request.ID)
            if not client:
                return

            # Retorna uma sequência de ordens de compra associadas ao cliente
            for order in self.orders.values():
                if order.CID == request.ID:
                    yield order.to_proto()

        except Exception as e:
            return


def runServer():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_OrderPortalServicer_to_server(OrderPortalServ(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    runServer()
