import grpc
from concurrent import futures
import admin_portal_service
import admin_pb2_grpc


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    admin_portal = admin_portal_service.AdminPortalService()
    admin_pb2_grpc.add_AdminPortalServicer_to_server(admin_portal, server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("server is running")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
