import data_bridge
import sys
from PyQt5 import QtWidgets 
sys.path.append("Manager")
sys.path.append("Cook")
sys.path.append("Cashier")
import managerAttached
import welcomeScreenAttatched
import cookAttached



####### Initial setup of running environment
mass = data_bridge.bridge("sql.json")

app = QtWidgets.QApplication(sys.argv)

welcome_win = QtWidgets.QMainWindow()
welcomeUI = welcomeScreenAttatched.welcomeScreenAttatched(mass, welcome_win)
cookGUIWindow = QtWidgets.QMainWindow()
CookWindowUI = cookAttached.cookAttached(mass, cookGUIWindow)
manager_win = QtWidgets.QMainWindow()
manager_ui = managerAttached.managerAttached(mass, manager_win)
app.exec_()
