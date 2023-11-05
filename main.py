import sys
from PyQt6 import QtWidgets, uic

# class Donors():
#     def __init__(self):
#         self.donors = []

class Invalid(Exception):
    pass
class Main(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self._donors = {
            "Bellevue": {},
            "Seattle": {},
            "Portland": {}
        }

        uic.loadUi("mainwindow.ui", self)
        self.add.clicked.connect(self.open_donorinfo)
        self.findbranch.clicked.connect(self.find_branch)

    def get_donors(self):
        return self._donors

    def find_branch(self):
        #will be microservice
        open_branch = "2"
        self.branch.setText(open_branch)

    def create_donor(self):
        """creates donor from user input and adds to donors"""

        last = self.last.text()
        first = self.first.text()
        dob = self.dob.text()
        num = self.num.text()
        donations = self.donations.currentText()
        center=  self.center.currentText()
        branch =  self.branch.text()

        donor = Donor(last,first,dob,num,donations,center,branch)

        for i in self._donors:
            if i == center:
                self._donors[i][num] = donor
        print(self._donors)


    def validate_new(self):
        last = self.last.text()
        first = self.first.text()
        dob = self.dob.text()
        num = self.num.text()
        donations = self.donations.currentText()
        center = self.center.currentText()
        branch = self.branch.text()

        if last == "" or first == "" or dob == "" or num == "" or branch == "" \
            or center =="Choose Location" or donations == "Choose Number":
            return False

    def display_new_donor(self):
        """modifies labels to display donor information when add donor is clicked"""
        last = self.last.text()
        self.window.last.setText(last)

        first = self.first.text()
        self.window.first.setText(first)

        dob = self.dob.text()
        self.window.dob.setText(dob)

        num = self.num.text()
        self.window.num.setText(num)

        donations = self.donations.currentIndex()
        self.window.donations.setCurrentIndex(donations)

        center = self.center.currentIndex()
        self.window.center.setCurrentIndex(center)

        branch = self.branch.text()
        self.window.branch.setText(branch)

    def clear_info(self):

        self.last.setText("")
        self.first.setText("")
        self.dob.setText("")
        self.num.setText("")
        self.donations.setCurrentIndex(0)
        self.center.setCurrentIndex(0)
        self.branch.setText("")
        self.validate.setText("")

    def open_donorinfo(self):
        """Opens window with donor information added"""
        if self.validate_new() is False:
            self.validate.setText("Please fill out all fields.")
            return
        self.create_donor()
        self.window = DonorInfo()
        self.window.show()
        self.display_new_donor()
        self.clear_info()

class DonorInfo(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("donorinfo1.ui", self)
        self.save.clicked.connect(self.save_info)
        self.ok.clicked.connect(self.hide_wind)

    def save_info(self):
        last = self.last.text()
        first = self.first.text()
        dob = self.dob.text()
        num = self.num.text()
        donations = self.donations.currentText()
        center = self.center.currentText()
        branch = self.branch.text()

        donor =Donor(last,first,dob,num,donations,center,branch)
        donors = window.get_donors()
        for i in donors:
            if i == center:
                dict= donors[i]
                for i in dict:
                    if i == num:
                        dict[i] = donor
        self.label_4.setText("Donor information updated.")

    def hide_wind(self):
        self.hide()

class Donor:
    def __init__(self, last, first, dob, num, donations, center, branch):
        self._last = last
        self._first = first
        self._dob = dob
        self._num = num
        self._donations = donations
        self._center = center
        self._branch = branch


app = QtWidgets.QApplication(sys.argv)
window = Main()
window.show()
app.exec()