from PySide6 import QtCore, QtWidgets, QtGui, QtMultimedia
import sys
import os
import time
import random as rd
import subprocess   

class Menu(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Menu")
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        self.setFixedSize(300, 300)
        self.pets = ["Alvarez(WIP)", "Bernardo(WIP)", "De Bruyne", "Ederson(WIP)", "Foden(WIP)", "Grealish(WIP)", "Haaland" , "Rodri(WIP)", "Ruben(WIP)", "Walker(WIP)"]
        self.initPets()
    
    def initPets(self):
        for pet in self.pets:
            button = QtWidgets.QPushButton(pet)
            button.clicked.connect(lambda _, pet=pet: self.runPlayerApp(pet))
            self.layout.addWidget(button)
    
    def runPlayerApp(self, petName):
        if petName == "De Bruyne":
            petName = petName.replace(" ", "")
        bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
        pet_script_path = os.path.join(bundle_dir, 'pet.py')
        subprocess.Popen(["python", pet_script_path, petName.casefold()], shell=True)
        
        

menuApp = QtWidgets.QApplication(sys.argv)
menu = Menu()
menu.show()
sys.exit(menuApp.exec_())