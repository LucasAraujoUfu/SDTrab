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
        "Cadeira": 3.5,
        "Mesa": 6.,
        "Cama": 4.75,
    }

    CID = input("Digite seu nome de usuario: ")

    OID = (random.randint(0, 10000)+random.randint(0, 10000))

    list_compra = []

    while True:
        menu(products)
        op = int(input("opção: "))

        if op == 0:
            break

        qtd = int(input("quantidade: "))
        pName = list(products.keys())[op-1]
        od = {
            "PID": op-1,
            "price": products[pName],
            "quantity": qtd,
        }
        list_compra.append(json.dumps(od))

    print(list_compra)
    order = admin_pb2.Order(OID=f"{OID}", CID=CID, data=json.dumps(list_compra))
    response = stub.CreateOrder(order)
    print(order)
    choice = input("Confirmar o pedido (S/N)? ")
    if choice == 'N':
        response = stub.DeleteOrder(admin_pb2.ID(ID=f"{OID}"))
    else:
        choice = input("Deseja Editar o pedido (S/N)? ")
        if choice == 'S':
            for i in list_compra:
                it = json.loads(i)
                print(it)
        response = stub.RetrieveOrder(admin_pb2.ID(ID=f"{OID}"))
        print(response)


def menu(prods: dict):
    os.system("clear")
    print("O que deseja comprar?")
    for j, i in enumerate(prods):
        print(j+1, '-', i+':', prods[i])
    print("0 - Sair")


if __name__ == '__main__':
    run()
