import socket
import json

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

def select_number_of_flowers():
    while True:
        try:
            num_flowers = int(input("Enter the number of flowers (1-10): "))
            if 1 <= num_flowers <= 10:
                return num_flowers
            else:
                print("Number of flowers must be between 1 and 10.")
                return None  
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def select_flower():
    flower_type = input("Select flower type (fresh/dried): ")
    if flower_type in flowers:
        print(f"Available {flower_type} flowers: {', '.join(flowers[flower_type])}")
        flower = input("Select a flower: ")
        if flower in flowers[flower_type]:
            return flower_type, flower
    print("Invalid input. Please try again.")
    return select_flower()

def select_wrap():
    print(f"Available wraps: {', '.join(wraps)}")
    wrap = input("Select a wrap (Bouquet/Vase/Basket): ")
    if wrap in wraps:
        return wrap
    print("Invalid input. Please try again.")
    return select_wrap()

def select_delivery():
    print(f"Available delivery options: {', '.join(delivery_options)}")
    delivery = input("Select delivery option (Pick-Up/Messenger): ")
    if delivery in delivery_options:
        return delivery
    print("Invalid input. Please try again.")
    return select_delivery()

def select_payment(delivery_option):
    print(f"Available payment options for {delivery_option}: {', '.join(payment_options[delivery_option])}")
    payment = input(f"Select payment method ({'/'.join(payment_options[delivery_option])}): ")
    if payment in payment_options[delivery_option]:
        return payment
    print("Invalid input. Please try again.")
    return select_payment(delivery_option)

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 12345))  

    num_flowers = select_number_of_flowers()
    if num_flowers is None:
    
        response = {
            "status_code": 203,
            "status_message": "Invalid number of flowers. Must be between 1 and 10."
        }
        client.send(json.dumps(response).encode('utf-8'))
        client.close()
        return

    orders = []

    for _ in range(num_flowers):
        flower_type, flower = select_flower()
        orders.append({"flower_type": flower_type, "flower": flower})

    wrap = select_wrap()
    delivery = select_delivery()
    payment = select_payment(delivery)

    delivery_date = input("Enter delivery date (YYYY-MM-DD): ")
    delivery_time = input("Enter delivery time (HH:MM): ")

    order = {
        "flowers": orders,  
        "wrap": wrap,
        "delivery": delivery,
        "payment": payment,
        "delivery_date": delivery_date,
        "delivery_time": delivery_time
    }

    client.send(json.dumps(order).encode('utf-8'))

    response = client.recv(1024).decode('utf-8')
    response_data = json.loads(response)

    if response_data["status_code"] == 200:
        print("Order placed successfully!")
        print(f"Order status: {response_data['order_status']}")
        print(f"Delivery date: {response_data['delivery_date']}")
        print(f"Delivery time: {response_data['delivery_time']}")
    else:
        print("Error:", response_data["status_message"], response_data.get("error", ""))

    client.close()

if __name__ == "__main__":
    main()
