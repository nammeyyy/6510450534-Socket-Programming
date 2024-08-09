import socket
import threading
import json
from datetime import datetime

flowers = {
    "fresh": ["Roses", "Lilies", "Tulips"],
    "dried": ["Lavender", "Sunflower", "Cotton"]
}

wraps = ["Bouquet", "Vase", "Basket"]
delivery_options = ["Pick-Up", "Messenger"]
payment_options = {
    "Pick-Up": ["Cash", "QR Payment"],
    "Messenger": ["QR Payment"]
}

orders = []

def validate_date(date_string):
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_time(time_string):
    try:
        datetime.strptime(time_string, '%H:%M')
        return True
    except ValueError:
        return False

def handle_client(client_socket):
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break

            print("Received order data from client:")
            print(data)

            order = json.loads(data)

            if "flowers" in order:
                num_flowers = len(order["flowers"])
                if not (1 <= num_flowers <= 10):
                    response = {
                        "status_code": 203,
                        "status_message": "Invalid number of flowers. Must be between 1 and 10."
                    }
                    client_socket.send(json.dumps(response).encode('utf-8'))
                    continue

            delivery_date = order.get("delivery_date")
            delivery_time = order.get("delivery_time")

            if not validate_date(delivery_date):
                response = {
                    "status_code": 403,
                    "status_message": "Forbidden",
                    "error": "Invalid delivery date format. Use YYYY-MM-DD."
                }
                client_socket.send(json.dumps(response).encode('utf-8'))
                continue

            if not validate_time(delivery_time):
                response = {
                    "status_code": 403,
                    "status_message": "Forbidden",
                    "error": "Invalid delivery time format. Use HH:MM."
                }
                client_socket.send(json.dumps(response).encode('utf-8'))
                continue

            orders.append(order)

            order_status = "Processing"  # Replace with actual status
            response = {
                "status_code": 200,
                "status_message": "OK",
                "order_status": order_status,
                "delivery_date": delivery_date,
                "delivery_time": delivery_time
            }

            client_socket.send(json.dumps(response).encode('utf-8'))
        except Exception as e:
            response = {
                "status_code": 500,
                "status_message": "Internal Server Error",
                "error": str(e)
            }
            client_socket.send(json.dumps(response).encode('utf-8'))
            break

    client_socket.close()

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket successfully created")

    port = 12345
    s.bind(('', port))
    print(f"Socket binded to {port}")

    s.listen(5)
    print("Socket is listening")

    while True:
        c, addr = s.accept()
        print(f"Got connection from {addr}")

        client_handler = threading.Thread(target=handle_client, args=(c,))
        client_handler.start()

if __name__ == "__main__":
    main()
