from manageOrderList import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
import OrderItem

class manageOrderListAttached(Ui_MainWindow, QMainWindow):
    #constructor
    def __init__(self, mass, parent = None):  
        self.currentOrderID = ""
        self.custName_var = ""
        super().__init__(parent)
        self.setupUi(self)
        self.mass = mass
        #initializing variables
        self.globalRow = 0
        self.globalCol = 0
        # self.orderList_TableWidget
        self.orderList_TableWidget.setColumnWidth(0,100)
        self.orderList_TableWidget.setColumnWidth(1,75)
        self.orderList_TableWidget.setColumnWidth(2,200)
        #calls clickEdit function
        self.accept_but.clicked.connect(self.clickAccept)
        #calls clickVoid function
        self.void_but.clicked.connect(self.clickVoid)
        #calls clickBack function
        self.back_but.clicked.connect(self.clickBack)
        #calls spinSelected if increment box changes
        self.increment_spinBox.valueChanged.connect(self.spinSelected)
        #gets position of current cell clicked
        self.orderList_TableWidget.cellClicked.connect(self.cellClickPosition)
        
    #allows the editing of order    
    def clickAccept(self):
        self.hide()
        nameList_Complete = []
        quantList_Complete = []
        notesList_Complete = []
        menuIDList_Complete = []
        numRows = self.orderList_TableWidget.rowCount()
        
        #pulls customer name from custName_LineEdit (cuts off suffix)
        custName_Complete = self.custName_LineEdit.text()[:-9]
        
        #adds all the edited attributes to respective lists
        for row in range(numRows):
            nameList_Complete.append(self.orderList_TableWidget.item(row, 0).text())
            quantList_Complete.append(self.orderList_TableWidget.item(row, 1).text())
            notesList_Complete.append(self.orderList_TableWidget.item(row, 2).text())
            
        #changes nameList into menuID's in menuIDList_Complete
        for item in nameList_Complete:
            menuID = next(i.item_id for i in self.mass.menu_items if i.item_name == item)
            menuIDList_Complete.append(menuID)
        
        for i in range(numRows):
            #creates OrderItem object
            orderItemObject = OrderItem.OrderItem(self.currentOrderID, menuIDList_Complete[i], quantList_Complete[i], notesList_Complete[i])
            #adds OrderItem object to database
            self.mass.update_order_item(orderItemObject)
        
    #deletes order from db
    def clickVoid(self):
        delItemID = next(item.item_id for item in self.mass.menu_items if item.item_name == self.orderList_TableWidget.item(self.globalRow, 0).text())
        self.mass.remove_order_item(next(item for item in self.mass.log[self.currentOrderID] if item.item_id == delItemID))
        self.orderList_TableWidget.removeRow(self.globalRow)
    
    #goes back to manageOrder    
    def clickBack(self):
        self.hide()
    
    #edits quantity of clicked cell
    def cellClickPosition(self, row, col):
        self.globalRow, self.globalCol = row, col
        
    
    #increments the quantity
    def spinSelected(self):
        if self.globalCol == 1:
            self.orderList_TableWidget.setItem(self.globalRow, self.globalCol, QTableWidgetItem(str(self.increment_spinBox.value())))
