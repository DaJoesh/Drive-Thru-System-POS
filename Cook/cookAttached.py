from cookGUI import *
from PyQt5 import *
from PyQt5.QtWidgets import QMainWindow


class cookAttached(Ui_cookGUI, QMainWindow):
    #making constructor
    def __init__(self, mass, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self.mass = mass
        self.submittedOrders = [i for i in self.mass.orders if i.order_status == 's']
        self.updateOrderSlots()
        self.show()
        self.doneButton1.clicked.connect(self.prepareOrderSlot1)     #update slot 1
        self.doneButton2.clicked.connect(self.prepareOrderSlot2)     #update slot 2
        self.doneButton3.clicked.connect(self.prepareOrderSlot3)     #update slot 3
        self.doneButton4.clicked.connect(self.prepareOrderSlot4)     #update slot 4

        
    #edit slot 1
    def updateOrderSlots(self):
        try:
            self.orderNum1.clear()
            self.listWidget.clear()
            self.orderNum1.setText(str(self.submittedOrders[3].queue_num))
            for item in self.mass.log[self.submittedOrders[3].order_id]:
                self.listWidget.addItem("x" + str(item.quantity)\
                 + "  " + next(i.item_name for i in self.mass.menu_items if i.item_id == item.item_id) + "\n" +item.notes + "\n")
        except:
            pass

        try:
            self.orderNum2.clear()
            self.listWidget_2.clear()
            self.orderNum2.setText(str(self.submittedOrders[2].queue_num))
            for item in self.mass.log[self.submittedOrders[2].order_id]:
                self.listWidget_2.addItem("x" + str(item.quantity)\
                 + "  " + next(i.item_name for i in self.mass.menu_items if i.item_id == item.item_id) + "\n" +item.notes + "\n")
        except:
            pass

        try:
            self.orderNum3.clear()
            self.listWidget_3.clear()
            self.orderNum3.setText(str(self.submittedOrders[1].queue_num))
            for item in self.mass.log[self.submittedOrders[1].order_id]:
                self.listWidget_3.addItem("x" + str(item.quantity)\
                 + "  " + next(i.item_name for i in self.mass.menu_items if i.item_id == item.item_id) + "\n" +item.notes + "\n")
        except:
            pass

        try:
            self.orderNum4.clear()
            self.listWidget_4.clear()
            self.orderNum4.setText(str(self.submittedOrders[0].queue_num))
            for item in self.mass.log[self.submittedOrders[0].order_id]:
                self.listWidget_4.addItem("x" + str(item.quantity)\
                 + "  " + next(i.item_name for i in self.mass.menu_items if i.item_id == item.item_id) + "\n" +item.notes + "\n")
        except:
            pass

    def prepareOrderSlot1(self, order):
        self.submittedOrders = [i for i in self.mass.orders if i.order_status == 's']
        try:
            self.mass.complete_order(self.submittedOrders[3])
            self.submittedOrders.pop(3)
        except:
            pass
        try:
            self.updateOrderSlots()
        except:
            print("no actice orders: cook GUI closed")

    def prepareOrderSlot2(self, order):
        self.submittedOrders = [i for i in self.mass.orders if i.order_status == 's']
        try:
            self.mass.complete_order(self.submittedOrders[2])
            self.submittedOrders.pop(2)
        except:
            pass
        try:
            self.updateOrderSlots()
        except:
            print("no actice orders: cook GUI closed")

    def prepareOrderSlot3(self, order):
        self.submittedOrders = [i for i in self.mass.orders if i.order_status == 's']
        try:
            self.mass.complete_order(self.submittedOrders[1])
            self.submittedOrders.pop(1)
        except:
            pass
        try:
            self.updateOrderSlots()
        except:
            print("no actice orders: cook GUI closed")

    def prepareOrderSlot4(self, order):
        self.submittedOrders = [i for i in self.mass.orders if i.order_status == 's']
        try:
            self.mass.complete_order(self.submittedOrders[0])
            self.submittedOrders.pop(0)
        except:
            pass
        try:
            self.updateOrderSlots()
        except:
            print("no actice orders: cook GUI closed")
