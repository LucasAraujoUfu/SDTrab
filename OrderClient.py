import grpc
import admin_pb2
import admin_pb2_grpc

def create_order():
    channel = grpc.insecure_channel('localhost:50051')
    stub = admin_pb2_grpc.OrderPortalStub(channel)

    order_id = input("Enter Order ID: ")
    client_id = input("Enter Client ID: ")
    data = input("Enter Order data (in JSON format): ")

    order = admin_pb2.Order(OID=order_id, CID=client_id, data=data)
    reply = stub.CreateOrder(order)

    print(reply)

def retrieve_order():
    channel = grpc.insecure_channel('localhost:50051')
    stub = admin_pb2_grpc.OrderPortalStub(channel)

    order_id = input("Enter Order ID: ")

    order_id_message = admin_pb2.ID(ID=order_id)
    order = stub.RetrieveOrder(order_id_message)

    print(order)

def update_order():
    channel = grpc.insecure_channel('localhost:50051')
    stub = admin_pb2_grpc.OrderPortalStub(channel)

    order_id = input("Enter Order ID: ")
    data = input("Enter new Order data (in JSON format): ")

    order = admin_pb2.Order(OID=order_id, data=data)
    reply = stub.UpdateOrder(order)

    print(reply)

def delete_order():
    channel = grpc.insecure_channel('localhost:50051')
    stub = admin_pb2_grpc.OrderPortalStub(channel)

    order_id = input("Enter Order ID: ")

    order_id_message = admin_pb2.ID(ID=order_id)
    reply = stub.DeleteOrder(order_id_message)

    print(reply)

def retrieve_client_orders():
    channel = grpc.insecure_channel('localhost:50051')
    stub = admin_pb2_grpc.OrderPortalStub(channel)

    client_id = input("Enter Client ID: ")

    client_id_message = admin_pb2.ID(ID=client_id)
    orders = stub.RetrieveClientOrders(client_id_message)

    for order in orders:
        print(order)

if __name__ == '__main__':
    while True:
        print("1. Create Order")
        print("2. Retrieve Order")
        print("3. Update Order")
        print("4. Delete Order")
        print("5. Retrieve Client Orders")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            create_order()
        elif choice == '2':
            retrieve_order()
        elif choice == '3':
            update_order()
        elif choice == '4':
            delete_order()
        elif choice == '5':
            retrieve_client_orders()
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")
