import sys
from PyQt6 import QtWidgets, uic


class Main(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self._donors = {
            "Bellevue": {},
            "Seattle": {},
            "Portland": {}
        }
        self._num_branches = {
            "Bellevue": 10,
            "Seattle": 10,
            "Portland": 10
        }

        uic.loadUi("mainwindow.ui", self)
        self.add.clicked.connect(self.open_donorinfo)
        self.findbranch.clicked.connect(self.find_branch)

    def get_donors(self):
        return self._donors

    def find_branch(self):
        # will be microservice
        open_branch = "2"
        self.branch.setText(open_branch)

    def create_donor(self, last, first, dob, num, donations, center, branch):
        """creates donor from user input and adds to donors"""

        donor = Donor(last, first, dob, num, donations, center, branch)

        for i in self._donors:
            if i == center:
                self._donors[i][num] = donor
        print(self._donors)

    def val(self, last, first, dob, num, donations, center, branch):
        if self.validate_full(last, first, dob, num, donations, center, branch) is False:
            self.validate.setText("Please fill out all fields.")
            return False
        if self.validate_donor(num) is False:
            self.validate.setText("Donor already in system.")
            return False
        if self.validate_branch(branch, center) is False:
            self.validate.setText("Invalid branch. Please enter another or click 'Find Branch' "
                                  "to find an open spot.")
            return False
        if self.validate_dob(dob) is False:
            self.validate.setText("Please enter DOB in MM-DD-YYYY format.")
            return False
        if self.validate_num(num) is False:
            self.validate.setText("Donor number may only contain digits 0-9.")
            return False

    def validate_full(self, last, first, dob, num, donations, center, branch):

        if last == "" or first == "" or dob == "" or num == "" or branch == "" \
                or center == "Choose Location" or donations == "Choose Number":
            return False

    def validate_donor(self,num):
        for i in self._donors:
            for j in self._donors[i]:
                if num == j:
                    return False

    def validate_branch(self, branch, center):
        for i in self._num_branches:
            if i == center and int(branch) > self._num_branches[i]:
                return False

    def validate_dob(self, dob):
        if len(dob) != 10:
            return False
        for i in range(len(dob)):
            if i == 2 or i == 5:
                if dob[i] != "-":
                    return False
            elif not dob[i].isdigit():
                return False

    def validate_num(self,num):
        if not num.isdigit():
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
        last = self.last.text()
        first = self.first.text()
        dob = self.dob.text()
        num = self.num.text()
        donations = self.donations.currentText()
        center = self.center.currentText()
        branch = self.branch.text()

        if self.val(last, first, dob, num, donations, center, branch) is False:
            return
        self.create_donor(last, first, dob, num, donations, center, branch)
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

        donor = Donor(last, first, dob, num, donations, center, branch)
        donors = window.get_donors()
        for i in donors:
            if i == center:
                dict = donors[i]
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
