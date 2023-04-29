import grpc
import admin_pb2
import admin_pb2_grpc

# Cria um canal de gRPC apontando para o servidor em localhost:50051
channel = grpc.insecure_channel('localhost:50051')

# Cria um objeto stub gRPC para a interface do serviço administrativo
admin_stub = admin_pb2_grpc.AdminPortalStub(channel)

# Cria uma mensagem de solicitação para criar um novo cliente
new_client_request = admin_pb2.Client(CID='12345', data='{"name": "Alice"}')

# Chama o método CreateClient no stub, passando a mensagem de solicitação
response = admin_stub.CreateClient(new_client_request)

# Verifica se a operação foi bem-sucedida
if response.error == 0:
    print("Client created successfully")
else:
    print("Error creating client:", response.description)
