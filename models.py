import pyrebase
import datetime
import time
import threading

config={
   "apiKey": "AIzaSyBMjuS7yAjgHWUY-VxX7y6TSYDzu6C2E3c",
  "authDomain": "sigin-a0a4b.firebaseapp.com",
  "databaseURL": "https://sigin-a0a4b-default-rtdb.firebaseio.com",
  "projectId": "sigin-a0a4b",
  "storageBucket": "sigin-a0a4b.appspot.com",
  "messagingSenderId": "139412624194",
  "appId": "1:139412624194:web:39fb80ba1b0dc4cef2aedb"
}


firebase = pyrebase.initialize_app(config)

db = firebase.database()

auth=firebase.auth()

storage = firebase.storage()

def initialize_machine(email, password):
    try:
        machine = auth.sign_in_with_email_and_password(email, password)
        return VendingMachine(machine)
    except Exception as e:

        print("Error logging in ")
        # Catch the exception and return the error message
        return None

class VendingMachine:
    def __init__(self,machine_info):
        self.machine_id=machine_info['localId']
        self.id_token=machine_info['idToken'] 
        self.machine=None 
        try:
            self.machine=Machine(self.machine_id)
        except:
            raise ValueError("Error intializing machine") 
        self.order=Order(machine_id=self.machine_id)
        self._process_order=None
         

    def get_products(self):
        
       return self.machine.get_products()

    
    def get_product_by_slot(self,slot):
        for product in self.machine.get_products():
            if product.position==slot:
                return product 
        return None  
#order logic
    def add_item_to_cart(self, product, quantity=1):
        self.order.add_item(product,quantity)
    def view_cart(self):
       return self.order.view_order()  
    
    def clear_cart(self):
        self.order.clear_cart()

    def save_order(self):
        if self.order.items:
            self.order.save_order() 
#process order                 
    def initialize_process_order(self):
        if self.order.items:
            self._process_order=ProcessOrder(self.order)
        else:
            print("cart is empty")    
    def listen_to_order_status(self):
        if self._process_order:
            self._process_order.listen_to_order_status()  
    
    def get_order_qrinfo(self):
        if self.order.order_id:
            return f"{self.order.machine_id}/{self.order.order_id}"
        
    def get_order_status(self):
        if self.order.status==10:
            print("order scanned")
        elif self.order.status==20:
            print("Succeses")
            print("dispensing items.....")
            #hardware function here.......
            #self._process_order.update_stock()
            self._process_order.close_timer()
            self._process_order.close_stream()
        elif self.order.status==30:
            print("Unsucceses")
            self._process_order.close_timer()
            self._process_order.close_stream()
        elif self.order.status==100:
            print("Connection timed out") 
        return self.order.status
    def update_stock(self):
        self._process_order.update_stock()
    def clear_cart(self):
        self.order.clear_cart()   
    def clear_process_order(self):
        self._process_order=None     






    

    



    
    #returns a list of all products information
    #show products


class Machine:
    def __init__(self,machine_id):
        self.machine_id=machine_id
        self._machine_info=self.get_machine_data()
        self.products=None
        if self._machine_info!=None:
            self.name=self._machine_info["name"] 
            self.slots=self._machine_info["slots"]
        else:
            raise ValueError("Error retrieving machine")   
        
        self._products=self.get_products()    
        if self._products!=None:
            self.products=self._products    
        else:
            raise ValueError("Error retrieving products")                       
    #state function
    def set_available(self):
        if len(self.products) == 0:
            print("Erro:Machine doesn't have products")
        try:
            db.child("machines").child(self.machine_id).child("state").set(1)
            self.state = 1
            return True
        except:
            print("Error setting machine state")    
             
            
    def set_unavailable(self):
        try:
            db.child("machines").child(self.machine_id).child("state").set(0)    
            self.state = 0
            return True
        except:
            print("Error setting machine state")
   
    def get_state(self):
        try:
            self.state = db.child("machines").child(self.machine_id).child("state").get().val()
            return self.state
        except:
            print("Error getting machine state")
            return None  

    def get_machine_data(self):
        try:
            machine_info=db.child("machines").child(self.machine_id).get().val() 
            return machine_info 
        except:
            print("Error retriveing data")    
            return None
    def get_products(self):
            products=[]
            try:
                productref=db.child('machine-products').child(self.machine_id).get().each()
            except:
                print("Error getting products")
                return None
            
            for product in productref:
                products.append(Product(self.machine_id,product.key()))
                
            products.sort(key=lambda p: p.position)  
            return products    
     
#move to machine class
   
         
       


class Product:
    def __init__(self,machine_id,product_id):
        self.machine_id=machine_id
        self.product_id=product_id
        product=self.get_product_data()
        self.name=product['name']
        self.imgUrl=product['image']
        self.price=product['price']
        self.amount=product['amount'] 
        self.position=product['position'] 
    def get_product_data(self):
        product=db.child('machine-products').child(self.machine_id).child(self.product_id).get().val()
        return product
    def set_product_amount(self,newAmount):
        if newAmount not in range(1,30):
           print("incorrect amount")
           return None
        try:
            db.child('machine-products').child(self.machine_id).child(self.product_id).child("amount").set(newAmount)
            self.amount = db.child('machine-products').child(self.machine_id).child(self.product_id).child("amount").get().val()
            return True
        except:
            return None 
    
    def set_product_price(self,new_price):
        try:
            new_price = float(new_price)
            if new_price <= 0:
                print("Invalid price amount: {}".format(new_price))
                return None
        except ValueError:
            print("Invalid price input: {}".format(new_price))
            return None  
        # Set the instance variable
        self.price = new_price

        try:
            db.child('machine-products').child(self.machine_id).child(self.product_id).child("price").set(new_price)
            return True
        except:
            print("Error updating database")   
            return None 
  
      
        
    
#order class
class Order:
    def __init__(self,machine_id):
        self.items = []  # List to store the items in the order
        self.total=0
        self.status=0
        self.machine_id=machine_id
        self.order_id=None

    def add_item(self, product, quantity=1):
        if product.amount<quantity:
            raise ValueError("Not enough inventory")
        
        self.items.append({
            'product': product,
            'quantity': quantity,
            'subtotal':product.price*quantity
        })
        self.total+=product.price*quantity

        print(f"{quantity} {product.name}(s) added to the order.")
    def view_order(self):
        if self.items:
            print("Items in the order:")
            order=[]
            for item in self.items:
                
                order.append(f"{item['product'].name}: {item['quantity']} x ${item['product'].price} = ${item['subtotal']}")
            print(f"Total: ${self.total}")
            return order    
        else:
            None

    def save_order(self):
        items=[]
        for item in self.items:
            product=item['product']
            quantity=item['quantity']
            subtotal=item['subtotal']
            items={
               product.product_id:{'name':product.name,'price':product.price,'quantity':quantity,'subtotal':subtotal }
            }
        machine_order={
            'order':items,
            'status':0,
            'total':self.total,
            'timestamp':datetime.datetime.now().timestamp()
        }
        self.order_id=db.generate_key()
        db.child('machine-orders').child(self.machine_id).child(self.order_id).set(machine_order)        
   
    def clear_cart(self):
        self.items = []  # List to store the items in the order
        self.total=0
        self.status=0
        self.order_id=None



#Payment
class ProcessOrder:
    def __init__(self,order):
        self.order=order
        self.order_status_stream = None
        self.timer=None
   
    def order_status_stream_handler(self,message):
        if message["event"] == "put":
            order_status = message["data"]
            self.order.status=order_status            
            print("Order status updated:", order_status,self.order.status)

    def _connection_time_out(self):
        if self.order.status==0 or self.order.status==10:
            db.child('machine-orders').child(self.order.machine_id).child(self.order.order_id).child('status').set(100)
            self.order.status=100
            self.close_stream()
    

    def listen_to_order_status(self):
        self.order_status_stream = db.child("machine-orders").child(self.order.machine_id).child(self.order.order_id).child("status").stream(self.order_status_stream_handler)
        self.timer=threading.Timer(30,self._connection_time_out)
        self.timer.start()
                            
    def close_stream(self):
        if self.order_status_stream:
            self.order_status_stream.close()
    def close_timer(self):
        if self.timer:
            self.timer.cancel()        
    
    def update_stock(self):
        if self.order.status==20:
            for item in self.order.items:
                product=item['product']
                quantity=item['quantity'] 
                product.set_product_amount(product.amount-quantity)        

            


