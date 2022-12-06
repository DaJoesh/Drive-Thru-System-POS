# Association Class
class OrderItem:
    def __init__(self, order_id: int, item_id: int, quantity: int, notes: str):
        self.order_id = order_id
        self.item_id = item_id
        self.quantity = quantity
        self.notes = notes
