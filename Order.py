import uuid
from itertools import cycle
import OrderItem


class Order:
    queue = cycle(range(1, 200))

    def __init__(self, customer_name: str, *, order_id="null", order_status='s', queue_num=-1):

        self.customer_name = customer_name
        self.order_id = order_id
        self.queue_num = next(self.queue)
        if order_id == "null":
            self.order_id = uuid.uuid1().hex
        else:
            self.order_id = order_id
        self.order_status = order_status

    def prepare(self):
        self.order_status = 'p'
        return self

    def complete(self):
        self.order_status = "c"
        self.queue_num = 0

    def cancel(self):
        self.order_status = 'x'
        self.queue_num = 0

    def createOrderItem(self, item_id, *, quantity=1, notes=None):
        return OrderItem.OrderItem(self.order_id, item_id, quantity=quantity, notes=notes)
        
        
