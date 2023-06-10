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
                id = input("Nome de usuario que será apagado: ")
                response = stub.DeleteClient(admin_pb2.ID(ID=f"{id}"))
            elif op2 == 3:
                id = input("Nome de usuario: ")
                response = stub.RetrieveClient(admin_pb2.ID(ID=f"{id}"))
                print(response)
                input("press ENTER")
            elif op2 == 4:
                id = input("Qual id quer recuperar? ")
                response = stub.DeleteClient(admin_pb2.ID(ID=f"{id}"))
                input("Cliente deletado\nPress Enter")
        else:
            if op2 == 1:
                id = input("qual o identificador do produto? ")
                nome = input("Qual o nome do produto? ")
                preco = float(input("Qual o valor do produto? R$ "))
                qtd = int(input("Qual a quantidade desse produto no estoque? "))
                product = admin_pb2.Product(PID='1', data=f"name: {nome}, price: {preco}, quantity: {qtd}")
                response = stub.CreateProduct(product)
            elif op2 == 2:
                pass
            elif op2 == 3:
                id = input("qual o id do produto que deseja recuperar? ")
                response = stub.RetrieveProduct(admin_pb2.ID(ID=f"{id}"))
                print(response)
                input("press Enter")
            elif op2 == 4:
                pass


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
