import grpc
from concurrent import futures
import order_portal_service
import admin_pb2_grpc


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    order_portal = order_portal_service.OrderPortalService()
    admin_pb2_grpc.add_OrderPortalServicer_to_server(order_portal, server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("server is running")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
