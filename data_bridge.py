import mysql.connector
import json
import pandas as pd
import Order
import MenuItem
import OrderItem


class bridge:
    """This class will be used to control data movement between the runtime application
    and the azure cloud database used for this project"""
    def __init__(self, json_file_str: str):
        f = open(json_file_str, 'r')
        info = json.load(f)
        print("Connecting to server \""
              + info["host"] + "\"...")
        print("Using database \""
              + info["database"] + "\"...")
        self.mydb = mysql.connector.connect(**info)
        f.close()
       #################################CLASS ATTRIBUTES#################################

        # Rebuild all currently active orders
        self.orders = []
        for index, order in self.db_get_active_orders().sort_values(by=["queue_num"]).iterrows():
            self.orders.append(Order.Order(**order))

        # Rebuild all items attatched to the active orders
        self.log = {}
        for order in self.orders:
            self.log[order.order_id] = []
            for index, item in self.db_get_order_items(order).iterrows():
                self.log[order.order_id].append(OrderItem.OrderItem(**item))
        # Rebuild all menu items
        print(self.log.keys())
        self.menu_items = []
        for index, item in self.db_get_menu_items().iterrows():
            self.menu_items.append(MenuItem.MenuItem(**item))

    def add_order(self, order: Order.Order):
        """Add a new order to the database and runtime"""
        self.orders.append(order)
        self.log[order.order_id] = []
        self.db_add_order(order)
    
    def cancel_order(self, order: Order.Order):
        """Remove a single order from the database and runtime"""
        order.cancel()
        self.orders.remove(order)
        del self.log[order.order_id]
        self.db_update_order(order)

    def complete_order(self, order: Order.Order):
        """Update the  of an order to completed"""
        order.complete()
        self.orders.remove(order)
        del self.log[order.order_id]
        self.db_update_order(order)

    def edit_order(self, order: Order.Order, attr: str, value):
        """Edit a single order atribute in the database and runtime"""
        self.orders[self.orders.index(order)].__dict__[attr] = value
        self.db_edit_order(order, attr, value)

    def update_order(self, order: Order.Order):
        """Update an order in the runtime"""
        for attr in order.__dict__:
            self.edit_order(order, attr, order.__dict__[attr])
    
    def add_order_item(self, orderItem: OrderItem.OrderItem):
        """Add a single order item to the database and runtime"""
        self.log[orderItem.order_id].append(orderItem)
        self.db_add_order_item(orderItem)

    def remove_order_item(self, orderItem: OrderItem.OrderItem):
        """Remove a single order item from the database and runtime"""
        self.log[orderItem.order_id].remove(orderItem)
        self.db_remove_order_item(orderItem)
    
    def update_order_item(self, orderItem: OrderItem.OrderItem):
        """Update an order item in the database"""
        index = next((i for i, item in enumerate(self.log[orderItem.order_id]) if item.item_id == orderItem.item_id), -1)
        self.log[orderItem.order_id][index] = orderItem
        for attr in orderItem.__dict__:
            self.db_edit_order_item(orderItem, attr, orderItem.__dict__[attr])
    
    def add_menu_item(self, menuItem: MenuItem.MenuItem):
        """Add a single MenuItem into the runtime"""
        self.menu_items.append(menuItem)
        self.db_add_menu_item(menuItem)

    def remove_menu_item(self, menuItem: MenuItem.MenuItem):
        """Remove a single MenuItem from the runtime"""
        self.menu_items.remove(menuItem)
        self.db_remove_menu_item(menuItem)

    def edit_menu_item(self, menuItem: MenuItem.MenuItem, attr: str, value):
        """Edit a single MenuItem atribute in the database and runtime"""
        self.menu_items[self.menu_items.index(menuItem)].__dict__[attr] = value
        self.db_edit_menu_item(menuItem, attr, value)
    
    def update_menu_item(self, menuItem: MenuItem.MenuItem):
        """Update a single MenuItem in the database"""
        for attr in menuItem.__dict__:
            self.edit_menu_item(menuItem, attr, menuItem.__dict__[attr])


    #################################DATABASE EDITING METHODS#################################
    ################# Getter Operations #################

    def db_get_active_orders(self) -> pd.DataFrame:
        """Will return all of the orders in the database that are not completed and not canceled"""
        return pd.read_sql("select * from orders where order_status != 'c' and order_status != 'x'", self.mydb)

    def db_get_order_items(self, Order: Order) -> pd.DataFrame:
        """Given an Order object this method will scan the database for all of the order items that
        are associated with the given order"""
        return pd.read_sql("select * from order_items where order_id = \"" + Order.order_id + "\"", self.mydb)

    def db_get_menu_items(self) -> pd.DataFrame:
        """This will return all of the items that will be on the menu"""
        return pd.read_sql("select * from menu_items", self.mydb)

    ################# MenuItem Operations #################

    def db_add_menu_item(self, menuItem: MenuItem.MenuItem):
        """Add a single MenuItem into the database"""
        with self.mydb.cursor() as cursor:
            cursor.execute("insert into menu_items (item_id, item_name, item_description, price, image) values ("
                           + str(menuItem.item_id) + ", "
                           + "\"" + menuItem.item_name + "\", "
                           + "\"" + menuItem.item_description + "\", "
                           + str(menuItem.price) + ", "
                           + "%s)", [menuItem.image])
        self.mydb.commit()

    def db_remove_menu_item(self, MenuItem: MenuItem.MenuItem):
        """Remove a single MenuItem from the database"""
        with self.mydb.cursor() as cursor:
            cursor.execute("delete from menu_items where item_id = "
                           + str(MenuItem.item_id))
        self.mydb.commit()

    def db_edit_menu_item(self, menuItem: MenuItem.MenuItem, attribute: str, value):
        """Edit an attribute of a MenuItem in the database"""
        if attribute == "price":
            with self.mydb.cursor() as cursor:
                cursor.execute("update menu_items set "
                               + attribute + " = "
                               + str(value) + " where item_id = "
                               + str(menuItem.item_id))
            self.mydb.commit()
        elif attribute == "item_name" or attribute == "item_description":
            with self.mydb.cursor() as cursor:
                cursor.execute("update menu_items set "
                               + attribute + " = "
                               + "\"" + value + "\" where item_id = "
                               + str(menuItem.item_id))
            self.mydb.commit()
    ################# Order Operations #################

    def db_add_order(self, order: Order.Order):
        """Add a single order into the database"""
        with self.mydb.cursor() as cursor:
            cursor.execute("insert into orders (order_id, queue_num, customer_name, order_status) values ("
                           + "\"" + order.order_id + "\", "
                           + str(order.queue_num) + ", "
                           + "\"" + order.customer_name + "\", "
                           + "\'" + order.order_status + "\')")
        self.mydb.commit()

    def db_remove_order(self, Order: Order):
        """Remove a single order from the database"""
        with self.mydb.cursor() as cursor:
            for index, item in self.get_order_items(Order).iterrows():
                cursor.execute("delete from order_items where order_id = \""
                               + item["order_id"] + "\" and item_id = "
                               + str(item["item_id"]))
            cursor.execute("delete from orders where order_id = \""
                           + Order.order_id + "\"")
        self.mydb.commit()

    def db_edit_order(self, Order: Order, attribute: str, value):
        """Edit an attribute of a single order in the database"""
        if attribute == "queue_num":
            with self.mydb.cursor() as cursor:
                cursor.execute("update orders set "
                               + attribute + " = "
                               + str(value) + " where order_id = \""
                               + Order.order_id + "\"")
            self.mydb.commit()
        elif attribute == "customer_name" or attribute == "order_status":
            with self.mydb.cursor() as cursor:
                cursor.execute("update orders set "
                               + attribute + " = "
                               + "\"" + value + "\" where order_id = \""
                               + Order.order_id + "\"")
            self.mydb.commit()
    
    def db_update_order(self, Order: Order):
        """Update an every attribute of a single order in the database"""
        for attr in Order.__dict__:
            self.db_edit_order(Order, attr, Order.__dict__[attr])

    ################# OrderItem Operations #################

    def db_add_order_item(self, orderItem: OrderItem.OrderItem):
        """Add a single OrderItem into the database"""
        with self.mydb.cursor() as cursor:
            cursor.execute("insert into order_items (order_id, item_id, quantity, notes) values ("
                           + "\"" + orderItem.order_id + "\", "
                           + str(orderItem.item_id) + ", "
                           + str(orderItem.quantity) + ", "
                           + "\"" + str(orderItem.notes) + "\")")
        self.mydb.commit()

    def db_remove_order_item(self, OrderItem: OrderItem.OrderItem):
        """Remove a single OrderItem from the database"""
        with self.mydb.cursor() as cursor:
            cursor.execute("delete from order_items where order_id = \""
                           + OrderItem.order_id + "\" and item_id = \""
                           + str(OrderItem.item_id) + "\"")
        self.mydb.commit()

    def db_edit_order_item(self, OrderItem: OrderItem, attribute: str, value):
        """Edit an attribute of a single OrderItem in the database"""
        if attribute == "quantity":
            with self.mydb.cursor() as cursor:
                cursor.execute("update order_items set "
                               + attribute + " = "
                               + str(value) + " where order_id = \""
                               + OrderItem.order_id + "\" and item_id = "
                               + str(OrderItem.item_id))
            self.mydb.commit()
        elif attribute == "notes":
            with self.mydb.cursor() as cursor:
                cursor.execute("update order_items set "
                               + attribute + " = "
                               + "\"" + str(value) + "\" where order_id = \""
                               + OrderItem.order_id + "\" and item_id = "
                               + str(OrderItem.item_id))
            self.mydb.commit()