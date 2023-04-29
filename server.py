import grpc
import admin_pb2
import admin_pb2_grpc
from concurrent import futures


class AdminServicer(admin_pb2_grpc.AdminPortalServicer):
    def CreateClient(self, request, context):
        # Extrai o Client ID e o JSON de dados do cliente do objeto de solicitação
        cid = request.CID
        data = request.data

        # Processa os dados do cliente
        # Aqui você pode executar as operações necessárias para criar um novo cliente no banco de dados ou em outro sistema de armazenamento.
        # Vamos apenas imprimir os dados para fins de demonstração.
        print(f"Creating new client with CID {cid} and data {data}")

        # Cria um objeto Reply com código de erro 0 (sucesso) e retorna-o
        reply = admin_pb2.Reply(error=0)
        return reply


def RetrieveClient(self, request, context):
    for client in clients:
        if client.CID == request.ID:
            return client
    # Se o cliente não for encontrado, retorna uma mensagem de erro
    return admin_pb2.Client(CID="", data="", error=1, description="Client not found")


def UpdateClient(self, request, context):
    try:
        # Obtemos o ID do cliente a ser atualizado
        client_id = request.CID

        # Verificamos se o cliente existe na nossa lista de clientes
        if client_id not in self.clients:
            return admin_pb2.Reply(error=1, description="Cliente não encontrado")

        # Atualizamos os dados do cliente com os novos dados enviados na mensagem
        self.clients[client_id]["data"] = request.data

        # Retornamos uma mensagem de sucesso
        return admin_pb2.Reply(error=0)

    except Exception as e:
        # Em caso de erro, retornamos uma mensagem de erro com a descrição do erro
        return admin_pb2.Reply(error=1, description=str(e))


def DeleteClient(self, request, context):
    # Obtenha o ID do cliente a ser excluído
    client_id = request.ID

    # Verifique se o cliente existe
    if client_id not in self.clients:
        # Cliente não encontrado, retorne mensagem de erro
        return admin_pb2.Reply(error=1, description="Cliente não encontrado")

    # Exclua o cliente
    del self.clients[client_id]

    # Retorne mensagem de sucesso
    return admin_pb2.Reply(error=0)


def CreateProduct(self, request, context):
    try:
        # Recupera os dados do produto a partir da mensagem de requisição
        data = json.loads(request.data)
        # Verifica se o produto já existe
        if cache.exists(request.PID):
            # Caso já exista, retorna uma mensagem de erro
            return project_pb2.Reply(error=1, description="Product already exists")
        # Caso contrário, adiciona o produto ao cache
        cache.set(request.PID, data)
        # Retorna uma mensagem de sucesso
        return project_pb2.Reply(error=0)
    except:
        # Caso ocorra algum erro, retorna uma mensagem de erro genérica
        return project_pb2.Reply(error=1, description="Error creating product")


def RetrieveProduct(self, request, context):
    pid = request.ID
    if pid in self.products:
        p = self.products[pid]
        return product_pb2.Product(PID=pid, data=p)
    else:
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details('Product not found')
        return product_pb2.Product()
# pid = request.ID: extrai o ID do produto a partir da mensagem ID recebida como entrada.
# if pid in self.products:: verifica se o produto existe no dicionário self.products.
# p = self.products[pid]: se o produto existir, recupera seus dados.
# return product_pb2.Product(PID=pid, data=p): retorna a mensagem Product contendo o ID do produto e seus dados.
# else:: se o produto não existir, configura o contexto com um código de erro e uma mensagem de detalhes.
# return product_pb2.Product(): retorna uma mensagem Product vazia.


def UpdateProduct(self, request, context):
    # Recupera o produto existente
    existing_product = db.get_product(request.PID)

    # Verifica se o produto existe
    if not existing_product:
        # Retorna uma mensagem de erro se o produto não existir
        return admin_pb2.Reply(error=1, description=f"Product {request.PID} not found")

    # Atualiza os dados do produto com os dados recebidos na mensagem
    existing_product.update(json.loads(request.data))

    # Salva as alterações no banco de dados
    db.save_product(existing_product)

    # Retorna uma mensagem de sucesso
    return admin_pb2.Reply(error=0)


def DeleteProduct(self, request, context):
    # Obtém o ID do produto a ser excluído
    product_id = request.ID

    # Remove o produto da lista de produtos
    if product_id in self.products:
        del self.products[product_id]
        return reply(error=0)
    else:
        return reply(error=1, description="Produto não encontrado.")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    admin_pb2_grpc.add_AdminPortalServicer_to_server(AdminServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
