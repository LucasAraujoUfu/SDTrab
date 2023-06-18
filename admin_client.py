import grpc
import os
import admin_pb2
import admin_pb2_grpc


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = admin_pb2_grpc.AdminPortalStub(channel)

    data_t = {1: "Client", 2: "Product"}
    while True:
        menu()
        op = int(input("option: "))

        if op == 0:
            break
        if op not in data_t:
            continue
        menu_menage(data_t[op])
        op2 = int(input("option: "))
        os.system("clear")
        if op == 1:
            if op2 == 1:
                id = input("Nome de Usuario: ")
                nome = input("Qual o nome do cliente: ")
                client = admin_pb2.Client(CID=f"{id}", data=f"{{'name': {nome}}}")
                response = stub.CreateClient(client)
            elif op2 == 2:
                id = input("Id so usuario a ser atualizado: ")
                nome = input("Novo nome: ")
                client = admin_pb2.Client(CID=f"{id}", data=f"{{'name': {nome}}}")
                response = stub.UpdateClient(client)
            elif op2 == 3:
                id = input("Id do usuario deseja recuperar: ")
                response = stub.RetrieveClient(admin_pb2.ID(ID=f"{id}"))
                print(response)
                input("press ENTER")
            elif op2 == 4:
                id = input("Id do usuario para ser apagado: ")
                response = stub.DeleteClient(admin_pb2.ID(ID=f"{id}"))
                input("Cliente deletado\nPress Enter")
        else:
            if op2 == 1:
                id = input("Identificador do produto: ")
                nome = input("Nome do produto: ")
                preco = float(input("Valor do produto: R$ "))
                qtd = int(input("Quantidade desse produto no estoque: "))
                product = admin_pb2.Product(PID=f"{id}", data=f"name: {nome}, price: {preco}, quantity: {qtd}")
                response = stub.CreateProduct(product)
            elif op2 == 2:
                id = input("Identificador do produto a ser atualizado: ")
                nome = input("Nome do produto: ")
                preco = float(input("Valor do produto: R$ "))
                qtd = int(input("Quantidade desse produto no estoque: "))
                product = admin_pb2.Product(PID=f"{id}", data=f"name: {nome}, price: {preco}, quantity: {qtd}")
                response = stub.UpdateProduct(product)
            elif op2 == 3:
                id = input("Id do produto que deseja recuperar: ")
                response = stub.RetrieveProduct(admin_pb2.ID(ID=f"{id}"))
                print(response)
                input("press Enter")
            elif op2 == 4:
                id = input("Id do produto que será apagado: ")
                response = stub.DeleteProduct(admin_pb2.ID(ID=f"{id}"))
                input("Produto deletado\npress Enter")


def menu():
    os.system("clear")
    print("==Admin Portal==")
    print("1 - Client Manage")
    print("2 - Product Manage")
    print("0 - Sair")


def menu_menage(opc: str):
    os.system("clear")
    print("==Admin", opc, "==")
    print("1 - Create", opc)
    print("2 - Update", opc)
    print("3 - Retrieve", opc)
    print("4 - Delete", opc)


if __name__ == '__main__':
    run()
