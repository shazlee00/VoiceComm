from models import *
# Initialize the recognizer
import speech_recognition as sr
import pyttsx3

# Initialize the recognizer
r = sr.Recognizer()

# Function to convert text to
# speech
def SpeakText(command):
	
	# Initialize the engine
	engine = pyttsx3.init()
	engine.say(command)
	engine.runAndWait()
	
# Set up the stream on the order status path


machine=initialize_machine("machine@gmail.com","123456789")
while True:
    #show items and take user input
    products=machine.get_products()
    for product in products:
        print(vars(product))
    picked_item=input("item: ")
    item_amount=input("amount: ")
    #make a cart
    machine.add_item_to_cart(products[int(picked_item)] , int(item_amount))
    print(machine.order.items)
    print(machine.view_cart())
    machine.save_order()
    #proces payment
    machine.get_order_qrinfo()
    machine.initialize_process_order()
    machine.listen_to_order_status()
    i=True
    while i==True:
        status=machine.get_order_status()
        time.sleep(0.1)
        if status == 20:
            machine.update_stock()
            machine.clear_cart()
            machine.clear_process_order()
            time.sleep(3)
            i=False
        elif status in [30,100]:
            machine.clear_cart()
            machine.clear_process_order()
            time.sleep(3)
            i=False













#tests

# # Print the name and number of slots of machine_1
# print(machine_1.name)
# print(machine_1.slots)

# # Set the state of machine_1 to available and print the state
# machine_1.set_available()
# print(machine_1.get_state())

# # Set the state of machine_1 to unavailable and print the state
# machine_1.set_unavailable()
# print(machine_1.get_state())

# # Get the list of products of machine_1 and print their names and positions
# products = machine_1.get_products()
# for product in products:
#     print(vars(product))

# # Get the product at slot 1 of machine_1 and print its name
# product_1 = machine_1.get_product_by_slot(1)
# product_1.set_product_price(10)
# product_1.set_product_amount(7)
# print(vars(product_1))





