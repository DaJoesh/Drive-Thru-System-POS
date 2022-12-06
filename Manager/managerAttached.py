from PyQt5.QtWidgets import QMainWindow
from managerGUI import Ui_ManagerOrder_MainWindow
from editDialog import Ui_editDialog_MainWindow
import MenuItem

class managerAttached(Ui_ManagerOrder_MainWindow, QMainWindow):
    def __init__(self, mass, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.mass = mass
        self.edit_dlg = editDialog(mass, self)
        self.connectSignalsSlots()
        self.load()
        self.show()

    def load(self):
        self.menuItems_listWidget.clear()
        self.menuItems_listWidget.addItems([x.item_name for x in self.mass.menu_items])


    def connectSignalsSlots(self):
        self.addItem_pushButton.clicked.connect(self.addMenuItem_GUI)
        self.editItem_pushButton.clicked.connect(self.editMenuItem_GUI)
        self.removeItem_pushButton.clicked.connect(self.removeMenuItem_GUI)

    def addMenuItem_GUI(self):
        self.edit_dlg.function = "add"
        self.edit_dlg.itemName_plainTextEdit.clear()
        self.edit_dlg.description_plainTextEdit.clear()
        self.edit_dlg.price_plainTextEdit.clear()
        self.edit_dlg.show()



    def removeMenuItem_GUI(self):
        index = next((i for i, item in enumerate(self.mass.menu_items) if item.item_name == self.menuItems_listWidget.currentItem().text()), -1)
        current_item = self.mass.menu_items[index]
        self.mass.remove_menu_item(current_item)
        self.load()


    def editMenuItem_GUI(self):
        try:
            index = next((i for i, item in enumerate(self.mass.menu_items) if item.item_name == self.menuItems_listWidget.currentItem().text()), -1)
            current_item = self.mass.menu_items[index]
            self.edit_dlg.function = "edit"
            self.edit_dlg.current_item = current_item
            self.edit_dlg.itemName_plainTextEdit.setPlainText(current_item.item_name)
            self.edit_dlg.description_plainTextEdit.setPlainText(current_item.item_description)
            self.edit_dlg.price_plainTextEdit.setPlainText(str(current_item.price))
            self.edit_dlg.show()
        except Exception as e:
            print(e)


class editDialog(Ui_editDialog_MainWindow, QMainWindow):
    """edit a menu item"""
    def __init__(self, mass, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.current_item = None
        self.mass = mass
        self.function = None
        # Create an instance of the GUI
        # Run the .setupUi() method to show the GUI
        self.connectSignalsSlots()

    def connectSignalsSlots(self):
        self.cancel_pushButton.clicked.connect(self.hide)
        self.ok_pushButton.clicked.connect(self.save)
    
    def save(self):
        self.hide()
        if self.function == "edit":
            self.current_item.item_name = self.itemName_plainTextEdit.toPlainText()
            self.current_item.item_description = self.description_plainTextEdit.toPlainText()
            self.current_item.price = float(self.price_plainTextEdit.toPlainText())
            self.mass.update_menu_item(self.current_item)
        elif self.function == "add":
            newItem = MenuItem.MenuItem(self.itemName_plainTextEdit.toPlainText(), self.mass.menu_items[-1].item_id + 1, float(self.price_plainTextEdit.toPlainText()), self.description_plainTextEdit.toPlainText(), None)
            self.mass.add_menu_item(newItem)
        

        
        