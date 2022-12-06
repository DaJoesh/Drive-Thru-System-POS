from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from selectingItems import Ui_selectingItems
from finishOrderAttached import finishOrderAttatched

class selectingItemsAttatched(Ui_selectingItems, QMainWindow):

    def __init__(self, mass, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.mass = mass
        self.cancelbtn.clicked.connect(self.closeWindow)
        self.orderFrame1.hide()
        self.orderFrame2.hide()
        self.orderFrame3.hide()
        self.orderFrame4.hide()
        self.orderFrame5.hide()
        self.orderFrame6.hide()
        self.orderFrame7.hide()
        self.orderFrame8.hide()

        self.chickSanBtn.clicked.connect(self.showCSFrm)
        self.chickSanPicBtn.clicked.connect(self.showCSFrm)
        self.waltersNuggiesBtn.clicked.connect(self.showWNFrm)
        self.waltersNuggiesPicBtn.clicked.connect(self.showWNFrm)
        self.wanBangBtn.clicked.connect(self.showWBFrm)
        self.wanBangPicBtn.clicked.connect(self.showWBFrm)
        self.lastFFriesBtn.clicked.connect(self.showLFFFrm)
        self.lastFFriesPicBtn.clicked.connect(self.showLFFFrm)
        self.holyBreadBtn.clicked.connect(self.showHBFrm)
        self.holyBreadPicBtn.clicked.connect(self.showHBFrm)
        self.mackBtn.clicked.connect(self.showMFrm)
        self.mackPicBtn.clicked.connect(self.showMFrm)
        self.seaWtrBtn.clicked.connect(self.showSWFrm)
        self.seaWtrPicBtn.clicked.connect(self.showSWFrm)
        self.diMoxBtn.clicked.connect(self.showDMFrm)
        self.diMoxPicBtn.clicked.connect(self.showDMFrm)

        self.order1CancelBtn.clicked.connect(self.hideCSFrm)
        self.order2CancelBtn.clicked.connect(self.hideWNFrm)
        self.order3CancelBtn.clicked.connect(self.hideWBFrm)
        self.order4CancelBtn.clicked.connect(self.hideLFFFrm)
        self.order5CancelBtn.clicked.connect(self.hideHBFrm)
        self.order6CancelBtn.clicked.connect(self.hideMFrm)
        self.order7CancelBtn.clicked.connect(self.hideSWFrm)
        self.order8CancelBtn.clicked.connect(self.hideDMFrm)

        self.finishbtn.clicked.connect(self.switchToFinishOrder)

        self.itemsName = [None]*8
        self.itemsQty = [None]*8
        self.itemsNotes = [None]*8

        self.finishOrderWindow = QMainWindow()
        self.finishOrderUI = finishOrderAttatched(self.mass, self.finishOrderWindow)

        if(len(self.mass.orders) == 0):
            self.orderNumLabel.setText(str(1))
        else:
            self.orderNumLabel.setText(str(self.mass.orders[-1].queue_num+1))

    
    def switchToFinishOrder(self):
        self.finishOrderUI.submitOrderBtn.clicked.connect(self.hide)
        qty1 = self.order1Qty.value()
        qty2 = self.order2Qty.value()
        qty3 = self.order3Qty.value()
        qty4 = self.order4Qty.value()
        qty5 = self.order5Qty.value()
        qty6 = self.order6Qty.value()
        qty7 = self.order7Qty.value()
        qty8 = self.order8Qty.value()

        nums = 0

        if(qty1 != 0):
            self.itemsQty[0] = qty1
            nums += 1
        if(qty2 != 0):
            self.itemsQty[1] = qty2
            nums += 1
        if(qty3 != 0):
            self.itemsQty[2] = qty3
            nums += 1
        if(qty4 != 0):
            self.itemsQty[3] = qty4
            nums += 1
        if(qty5 != 0):
            self.itemsQty[4] = qty5
            nums += 1
        if(qty6 != 0):
            self.itemsQty[5] = qty6
            nums += 1
        if(qty7 != 0):
            self.itemsQty[6] = qty7
            nums += 1
        if(qty8 != 0):
            self.itemsQty[7] = qty8
            nums += 1

        notes1 = self.order1Notes.text()
        notes2 = self.order2Notes.text()
        notes3 = self.order3Notes.text()
        notes4 = self.order4Notes.text()
        notes5 = self.order5Notes.text()
        notes6 = self.order6Notes.text()
        notes7 = self.order7Notes.text()
        notes8 = self.order8Notes.text()

        if(notes1 != ""):
            self.itemsNotes[0] = notes1
        if(notes2 != ""):
            self.itemsNotes[1] = notes2
        if(notes3 != ""):
            self.itemsNotes[2] = notes3
        if(notes4 != ""):
            self.itemsNotes[3] = notes4
        if(notes5 != ""):
            self.itemsNotes[4] = notes5
        if(notes6 != ""):
            self.itemsNotes[5] = notes6
        if(notes7 != ""):
            self.itemsNotes[6] = notes7
        if(notes8 != ""):
            self.itemsNotes[7] = notes8

        row = 0
        totalPrice = 0
        for i in range(8):
            if(self.itemsName[i] != None):
                self.finishOrderUI.orderTableWidget.insertRow(row)
                self.finishOrderUI.orderTableWidget.setItem(row,0, QTableWidgetItem(self.itemsName[i]))
                self.finishOrderUI.orderTableWidget.setItem(row,1, QTableWidgetItem(str(self.itemsQty[i])))
                self.finishOrderUI.orderTableWidget.setItem(row,2, QTableWidgetItem(self.itemsNotes[i]))
                print(self.itemsName[i])
                totalItemPrice = next(x.price for x in self.mass.menu_items if x.item_name == self.itemsName[i])*self.itemsQty[i]
                self.finishOrderUI.orderTableWidget.setItem(row,3, QTableWidgetItem("$ %.2f" % totalItemPrice))
                totalPrice += totalItemPrice
                row += 1

        self.finishOrderUI.displayTotal.setText("$ %.2f" % totalPrice)
        self.finishOrderUI.show()

    def closeWindow(self):
        self.hide()

    def showCSFrm(self):
        self.orderFrame1.show()
        self.chickSanWid.setStyleSheet("border-style: outset;\n"
        "border-width: 5px;\n"
        "border-color: rgb(0, 255, 0);")
        self.order1Qty.setValue(1)
        name = self.order1Label.text()
        if(name in self.itemsName):
            pass
        else:
            self.itemsName[0] = name
    
    def showWNFrm(self):
        self.orderFrame2.show()
        self.waltersNuggiesWid.setStyleSheet("border-style: outset;\n"
        "border-width: 5px;\n"
        "border-color: rgb(0, 255, 0);")
        self.order2Qty.setValue(1)
        name = self.order2Label.text()
        if(name in self.itemsName):
            pass
        else:
            self.itemsName[1] = name
    
    def showWBFrm(self):
        self.orderFrame3.show()
        self.wangBangWid.setStyleSheet("border-style: outset;\n"
        "border-width: 5px;\n"
        "border-color: rgb(0, 255, 0);")
        self.order3Qty.setValue(1)
        name = self.order3Label.text()
        if(name in self.itemsName):
            pass
        else:
            self.itemsName[2] = name
    
    def showLFFFrm(self):
        self.orderFrame4.show()
        self.lastFFriesWid.setStyleSheet("border-style: outset;\n"
        "border-width: 5px;\n"
        "border-color: rgb(0, 255, 0);")
        self.order4Qty.setValue(1)
        name = self.order4Label.text()
        if(name in self.itemsName):
            pass
        else:
            self.itemsName[3] = name
    
    def showHBFrm(self):
        self.orderFrame5.show()
        self.holyBreadWid.setStyleSheet("border-style: outset;\n"
        "border-width: 5px;\n"
        "border-color: rgb(0, 255, 0);")
        self.order5Qty.setValue(1)
        name = self.order5Label.text()
        if(name in self.itemsName):
            pass
        else:
            self.itemsName[4] = name
    
    def showMFrm(self):
        self.orderFrame6.show()
        self.mackWid.setStyleSheet("border-style: outset;\n"
        "border-width: 5px;\n"
        "border-color: rgb(0, 255, 0);")
        self.order6Qty.setValue(1)
        name = self.order6Label.text()
        if(name in self.itemsName):
            pass
        else:
            self.itemsName[5] = name
    
    def showSWFrm(self):
        self.orderFrame7.show()
        self.seaWtrWid.setStyleSheet("border-style: outset;\n"
        "border-width: 5px;\n"
        "border-color: rgb(0, 255, 0);")
        self.order7Qty.setValue(1)
        name = self.order7Label.text()
        if(name in self.itemsName):
            pass
        else:
            self.itemsName[6] = name
    
    def showDMFrm(self):
        self.orderFrame8.show()
        self.diMoxWid.setStyleSheet("border-style: outset;\n"
        "border-width: 5px;\n"
        "border-color: rgb(0, 255, 0);")
        self.order8Qty.setValue(1)
        name = self.order8Label.text()
        if(name in self.itemsName):
            pass
        else:
            self.itemsName[7] = name

    def hideCSFrm(self):
        self.orderFrame1.hide()
        self.chickSanWid.setStyleSheet("")
        self.itemsName[0] = None
        self.order1Notes.setText("")
        self.order1Qty.setValue(0)
    
    def hideWNFrm(self):
        self.orderFrame2.hide()
        self.waltersNuggiesWid.setStyleSheet("")
        self.itemsName[1] = None
        self.order2Notes.setText("")
        self.order2Qty.setValue(0)

    def hideWBFrm(self):
        self.orderFrame3.hide()
        self.wangBangWid.setStyleSheet("")
        self.itemsName[2] = None
        self.order3Notes.setText("")
        self.order3Qty.setValue(0)
    
    def hideLFFFrm(self):
        self.orderFrame4.hide()
        self.lastFFriesWid.setStyleSheet("")
        self.itemsName[3] = None
        self.order4Notes.setText("")
        self.order4Qty.setValue(0)
    
    def hideHBFrm(self):
        self.orderFrame5.hide()
        self.holyBreadWid.setStyleSheet("")
        self.itemsName[4] = None
        self.order5Notes.setText("")
        self.order5Qty.setValue(0)
    
    def hideMFrm(self):
        self.orderFrame6.hide()
        self.mackWid.setStyleSheet("")
        self.itemsName[5] = None
        self.order6Notes.setText("")
        self.order6Qty.setValue(0)
    
    def hideSWFrm(self):
        self.orderFrame7.hide()
        self.seaWtrWid.setStyleSheet("")
        self.itemsName[6] = None
        self.order7Notes.setText("")
        self.order7Qty.setValue(0)
    
    def hideDMFrm(self):
        self.orderFrame8.hide()
        self.diMoxWid.setStyleSheet("")
        self.itemsName[7] = None
        self.order8Notes.setText("")
        self.order8Qty.setValue(0)
