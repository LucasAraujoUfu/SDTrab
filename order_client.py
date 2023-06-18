import grpc
import os
import json
import admin_pb2
import admin_pb2_grpc
import random


def run():
    channel = grpc.insecure_channel('localhost:50052')
    stub = admin_pb2_grpc.OrderPortalStub(channel)

    products = {
        1: "Cadeira: 3.5",
        2: "Mesa: 6. ",
        3: "Cama: 4.75",
    }

    CID = input("Digite seu nome de usuario: ")

    while True:
        menu()
        op = input("Opção: ")

        if op == '0':
            break

        elif op == '1':
            OID = (random.randint(0, 1000)+random.randint(0, 1000))
            list_compra = []
            print("Número da sua compra:", OID)
            input("[OK]")

            while True:
                menuCompra(products)
                opc = int(input("Opção: "))
                if opc == 0:
                    break
                else:
                    qtd = input("Quantidade: ")
                    list_compra.append({'PID': str(opc), 'price': qtd, 'quantity': qtd})

            response = stub.CreateOrder(admin_pb2.Order(OID=str(OID), CID=CID, data=json.dumps(list_compra)))

        elif op == '2':
            OID = input("Número da compra: ")
            response = stub.RetrieveOrder(admin_pb2.ID(ID=f"{OID}"))
            print(response)
            input("Press Enter")

        elif op == '3':
            OID = input("Número da compra: ")
            response = stub.DeleteOrder(admin_pb2.ID(ID=f"{OID}"))
            print("Compra cancelada")
            input("Press Enter")

        elif op == '4':
            OID = input("Número da compra a ser editada: ")
            list_compra = []

            while True:
                menuCompra(products)
                opc = int(input("Opção: "))
                if opc == 0:
                    break
                else:
                    qtd = input("Quantidade: ")
                    list_compra.append({'PID': str(opc), 'price': qtd, 'quantity': qtd})

            response = stub.UpdateOrder(admin_pb2.Order(OID=str(OID), CID=CID, data=json.dumps(list_compra)))

        elif op == '5':
            pass


def menuCompra(prods: dict):
    os.system("clear")
    print("O que deseja comprar?")
    for j, i in zip(prods.keys(), prods.values()):
        print(j, i)
    print("0 - Sair")


def menu():
    os.system("clear")
    print("1 - Comprar")
    print("2 - Vizualiar uma compra")
    print("3 - Cancelar uma compra")
    print("4 - Editar uma compra")
    print("5 - Ver todas suas comprar")
    print("0 - Sair")


if __name__ == '__main__':
    run()
