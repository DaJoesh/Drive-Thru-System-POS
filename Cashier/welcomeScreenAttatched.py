from PyQt5.QtWidgets import QMainWindow
from welcomeScreen import Ui_welcomeScreen
from selectingItemsAttached import selectingItemsAttatched
from manageOrderAttached import manageOrderAttached

class welcomeScreenAttatched(Ui_welcomeScreen, QMainWindow):

    def __init__(self, mass, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.mass = mass
        self.createOrderBtn.clicked.connect(self.switchToSelectingItems)
        self.show()
        self.manageOrderBtn.clicked.connect(self.switchToManagerOrder)

    def switchToSelectingItems(self):
        self.selectingItemsWindow = QMainWindow()
        self.selectingItemsUi = selectingItemsAttatched(self.mass, self.selectingItemsWindow)
        self.selectingItemsUi.show()
    
    def switchToManagerOrder(self):
        self.manageOrderWindow = QMainWindow()
        self.manageOrderUi = manageOrderAttached(self.mass, self.manageOrderWindow)
        self.manageOrderUi.show()
