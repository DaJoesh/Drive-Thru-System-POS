from manageOrder import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
import manageOrderListAttached



class manageOrderAttached(Ui_MainWindow, QMainWindow):
    def __init__(self, mass, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.mass = mass
        self.setupDisplay(mass.orders)
        self.setupButtons()
        self.show()
        self.manageOrderItems_win = QMainWindow()
        self.josh = manageOrderListAttached.manageOrderListAttached(self.mass, self.manageOrderItems_win)
        
        #button clickability


    def setupDisplay(self, orders):
        self.ordersList.addItems([x.customer_name for x in orders])
    def setupButtons(self):
        self.backButton.clicked.connect(self.clickBack)
        self.manageButton.clicked.connect(self.clickManage)
    def clickBack(self):
        self.hide()
    def clickManage(self):
        #list & menuItem intilization
        nameList = []
        quantList = []
        notesList = []
        orderName = self.ordersList.currentItem().text()
        menuItems = self.mass.menu_items
        
        #current orderID set
        orderID = next(i.order_id for i in self.mass.orders if i.customer_name == orderName)
        self.josh.currentOrderID = orderID
        orderItems = self.mass.log[self.josh.currentOrderID]
        
        #current custName sent to josh.custName_LineEdit
        self.josh.custName_var = orderName
        self.josh.custName_LineEdit.setText(self.josh.custName_var + "'s Order:")
        
        # for each item in given order, it puts each attribute into it's respective list
        for item in orderItems:
            name = next(i.item_name for i in menuItems if i.item_id == item.item_id)
            nameList.append(name)
            quantity = item.quantity
            quantList.append(quantity)
            notes = item.notes
            notesList.append(notes)
            
        #initialize row count
        self.josh.orderList_TableWidget.setRowCount(len(nameList))
        
        #taking the previously populated lists and putting them into the table
        for num in range(len(nameList)):
            self.josh.orderList_TableWidget.setItem(num, 0, QTableWidgetItem(nameList[num]))
            self.josh.orderList_TableWidget.setItem(num, 1, QTableWidgetItem(str(quantList[num])))
            self.josh.orderList_TableWidget.setItem(num, 2, QTableWidgetItem(notesList[num]))

        self.josh.show()
        
        

        