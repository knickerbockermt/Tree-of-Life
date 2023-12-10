import sys
from PyQt6 import QtWidgets, uic
import time


class Main(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self._donors = [{
            "last": "Smith",
            "first": "John",
            "dob": "01-19-1960",
            "num": "123",
            "donations": "100",
            "donation index": 1,
            "center": "Seattle",
            "center index": 2,
            "branch": "0",
        }]
        self._current_donor = None

        # load ui for main window
        uic.loadUi("mainwindow.ui", self)

        # connect clicked button on main window to function
        self.add.clicked.connect(self.open_donorinfo)
        self.findbranch.clicked.connect(self.find_branch)
        self.info.clicked.connect(self.branch_popup)
        self.search.clicked.connect(self.search_for_donor)
        self.close_2.clicked.connect(self.hide_banner)

    def get_donors(self):
        return self._donors

    def get_current_donor(self):
        return self._current_donor

    def set_current_donor(self, donor):
        self._current_donor = donor

    def hide_banner(self):
        self.banner.hide()
        self.close_2.hide()

    def search_for_donor(self):
        """
        Takes user input and searches for matching donor
        :return: None
        """
        self.search_validate.setText("")

        # get user input
        last = self.search_last.text().lower()
        first = self.search_first.text().lower()
        num = self.search_num.text()

        # validate input
        if self.validate_search(last, first, num) is False:
            return

        # find matching donor
        donor = self.search_donors(last, first, num)

        # no matching donor found
        if donor is None:
            self.search_popup = SearchPopup()
            self.search_popup.show()

        # matching donor found
        else:
            self.display_search_results(donor)

    def validate_search(self, last, first, num):
        """
        Validates that user input for search is entered correctly
        :return: None
        """
        # check that all fields are filled out
        if self.validate_search_full(last, first, num) is False:
            self.search_validate.setText("Please enter donor's first and last name or donor number.")
            return

        # check that donor number is only digits
        if self.validate_search_num(num) is False:
            self.search_validate.setText("Donor number may only contain digits 0-9.")
            return

    def validate_search_full(self, last, first, num):
        """
        Checks that user has entered either full name or donor number
        :return: False if full name or donor number is missing
        """
        if last == "" and first == "" and num == "":
            return False
        if last != "" and first == "" and num == "":
            return False
        if last == "" and first != "" and num == "":
            return False

    def validate_search_num(self, num):
        """
        Checks that donor number is only digits
        :return: False if not only digits
        """
        if not num.isdigit() and num != "":
            return False

    def search_donors(self, last, first, num):
        """
        Searches list of donors for match to user input
        :return: matching donor
        """
        if last != "" and first != "":
            donor = self.search_by_name(last, first)

        elif num != "":
            donor = self.search_by_num(num)

        return donor

    def search_by_name(self, last, first):
        """
        Searches donor list by donor name
        :return: donor if found, None if no matching donor
        """
        for donor in self._donors:
            if donor["last"] == last and donor["first"] == first:
                return donor
        return None

    def search_by_num(self, num):
        """
        Searches list of donors by donor number
        :return: donor if found, None if no matching donor
        """
        for donor in self._donors:
            if donor["num"] == num:
                return donor
        return None

    def display_search_results(self, donor):
        """
        Displays window with donor information from search
        :return: None
        """
        self._current_donor = donor

        # create donor info window
        self.donor_window = DonorInfo()
        self.donor_window.show()
        self.donor_window.banner.hide()

        # display donor's information in donor info window
        self.display_new_donor()
        self.clear_info()

    def find_branch(self):
        """
        Finds an open branch for leaf at center location given by user
        :return: number of branch in branch text box on main window
        """
        self.clear_branch()

        # validate that center has been chosen
        if self.validate_center() is False:
            self.validate.setText("Please choose a center location.")
            return

        # write center to branch-booking.txt
        self.write_center()

        # read and validate branch number from branch-booking.txt
        open_branch = self.read_branch()
        if open_branch == "invalid":
            self.validate.setText("Location invalid. Please choose a valid center.")
            return

        # set text in branch text box
        self.branch.setText(open_branch)

    def clear_branch(self):
        """
        Clears value from branch text box and validation text if "find branch"
        is clicked
        :return: None
        """
        if self.branch.text() != "":
            self.branch.setText("")
        if self.validate.text != "":
            self.validate.setText("")

    def write_center(self):
        """
        Writes center location to "branch-booking.txt"
        :return: None
        """
        location = self.center.currentText()
        file = open("branch-booking.txt", "w")
        file.write(location)
        file.close()

    def read_branch(self):
        """
        Reads branch number from branch-booking.txt
        :return: branch number or "invalid"
        """
        while True:
            time.sleep(1)
            file = open("branch-booking.txt", "r")
            open_branch = file.read()
            file.close()

            # if open_branch has been written to file by database service
            if open_branch.isdigit() or open_branch == "invalid":
                return open_branch

    def validate_center(self):
        """
        Returns false if center location is not chosen by user
        :return: None or False
        """
        if self.center.currentIndex() == 0:
            return False

    def branch_popup(self):
        """
        Displays dialogue explaining how to select a branch
        :return: None
        """
        self.popup_win = BranchPopup()
        self.popup_win.show()

    def open_donorinfo(self):
        """Opens window with donor information added
        :return: None
        """
        # get donor info
        self.validate.setText("")
        donor = self.create_dict()

        # validate donor
        if self.validate_add(donor) is False:
            return

        # add donor to system

        self.create_donor(donor)

        # display donor info window with current donor info
        self.donor_window = DonorInfo()
        self.donor_window.show()

        self.display_new_donor()
        self.clear_info()

    def create_dict(self):
        """
        Creates dictionary containing current values in add donor fields
        :return: donor_info dictionary
        """
        donor_info = {
            "last": self.last.text(),
            "first": self.first.text(),
            "dob": self.dob.text(),
            "num": self.num.text(),
            "donations": self.donations.currentText(),
            "donation index": self.donations.currentIndex(),
            "center": self.center.currentText(),
            "center index": self.center.currentIndex(),
            "branch": self.branch.text(),
        }

        return donor_info

    def validate_add(self, donor):
        """
        Validates fields in add donor section
        :return: False if any input entered incorrectly
        """
        if self.validate_add_full(donor) is False:
            self.validate.setText("Please fill out all fields.")
            return False

        if self.validate_donor(donor) is False:
            self.validate.setText("Donor already in system.")
            return False

        if self.validate_dob(donor) is False:
            self.validate.setText("Please enter date of birth as MM-DD-YYYY.")
            return False

        if self.validate_num(donor) is False:
            self.validate.setText("Donor number may only contain digits 0-9.")
            return False

        if self.validate_branch(donor) is False:
            self.validate.setText("Branch invalid or full. Please enter another or click 'Find Branch'.")
            return False

    def validate_add_full(self, donor):
        """
        Validates that all fields in add donor section have been filled out by user
        :return: False if field is empty
        """
        for key in donor:
            if donor[key] == "" or donor[key] == "Choose Location" or donor[key] == "Choose Number":
                return False

    def validate_donor(self, donor):
        """
        Validates that donor is not already in system
        :return: False if donor already in system
        """
        for i in self._donors:
            if donor["num"] == i["num"]:
                return False

    def validate_branch(self, donor):
        """
        Validates that there is an empty spot at given branch and location
        :return: False if branch is invalid
        """
        self.write_center_branch(donor)

        valid_branch = self.read_center_branch()
        if valid_branch == "invalid":
            return False

    def write_center_branch(self, donor):
        """Writes given branch and center to branch-booking.txt
        :return: None
        """
        branch = donor["branch"]
        center = donor["center"]

        inp = f"{center},{branch}"

        file = open("branch-booking.txt", "w")
        file.write(inp)
        file.close()

    def read_center_branch(self):
        """
        Reads branch-booking.txt to see if given branch and center are valid
        :return: "valid" or "invalid"
        """
        while True:
            time.sleep(1)
            file = open("branch-booking.txt", "r")
            open_branch = file.read()
            file.close()

            # if open_branch has been written to file by database service
            if open_branch == "valid" or open_branch == "invalid":
                return open_branch

    def validate_dob(self, donor):
        """
        Validates that DOB is in correct format
        :return: False if DOB not in correct format
        """
        dob = donor["dob"]
        length = len(dob)

        if length != 10:
            return False

        for i in range(length):
            # check that dashes are used
            if i == 2 or i == 5:
                if dob[i] != "-":
                    return False

            # check that digits are used
            elif not dob[i].isdigit():
                return False

    def validate_num(self, donor):
        """
        Validates that donor number is in correct format
        :return: False if donor number not in correct format
        """
        if not donor["num"].isdigit():
            return False

    def create_donor(self, donor_info):
        """
        Creates donor object from self._current_info and adds object to self._donors
        :return: None
        """
        self._donors.append(donor_info)
        self._current_donor = donor_info
        print(self._donors)

    def display_new_donor(self):
        """
        Displays current donor info on Donor Info dialogue
        :return: None
        """
        donor = self._current_donor

        self.donor_window.last.setText(donor["last"])
        self.donor_window.first.setText(donor["first"])
        self.donor_window.dob.setText(donor["dob"])
        self.donor_window.num.setText(donor["num"])
        self.donor_window.donations.setCurrentIndex(donor["donation index"])
        self.donor_window.center.setCurrentIndex(donor["center index"])
        self.donor_window.branch.setText(donor["branch"])

    def clear_info(self):
        """
        Clears all inputs from fields in add donor section
        :return: None
        """
        self.last.setText("")
        self.first.setText("")
        self.dob.setText("")
        self.num.setText("")
        self.donations.setCurrentIndex(0)
        self.center.setCurrentIndex(0)
        self.branch.setText("")
        self.validate.setText("")
        self.search_last.setText("")
        self.search_first.setText("")
        self.search_num.setText("")
        self.search_validate.setText("")



class DonorInfo(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # load ui for main window
        self.ui = uic.loadUi("donorinfo1.ui", self)

        # connect clicked button on donor info dialogue to function
        self.save.clicked.connect(self.save_info)
        self.ok.clicked.connect(self.hide_wind)
        self.remove.clicked.connect(self.remove_donor)
        self.close_1.clicked.connect(self.hide_banner)


    def hide_banner(self):
        """Hides green status banner
        :return: None
        """
        self.banner.hide()
        self.close_1.hide()

    def save_info(self):
        """
        Updates donor's information in system
        :return: None
        """
        self.hide_banner()
        self.validate.setText("")

        # extract new information
        new_info = self.get_info()
        current_info = window.get_current_donor()

        # check if information has changed
        same = self.compare_info(current_info, new_info)

        # if information has changed
        if same is False:
            # save new information to correct donor
            if self.validate_save(new_info) is False:
                return

            donors = window.get_donors()
            self.update_info(donors, new_info)

    def get_info(self):
        """
        Gets donor information from donor information window
        :return: dictionary of donor information
        """
        donor_info = {
            "last": self.last.text(),
            "first": self.first.text(),
            "dob": self.dob.text(),
            "num": self.num.text(),
            "donations": self.donations.currentText(),
            "donation index": self.donations.currentIndex(),
            "center": self.center.currentText(),
            "center index": self.center.currentIndex(),
            "branch": self.branch.text(),
        }
        return donor_info

    def compare_info(self, current, new):
        """
        Compares information from donor information screen to current donor's information
        :return: True if information matches, false if not
        """
        for key in new:
            # information doesn't match
            if current[key] != new[key]:
                return False

        # information matches
        return True

    def validate_save(self, new_info):
        """
        Validates updated donor information
        :return: False if input is invalid
        """
        if window.validate_add_full(new_info) is False:
            self.validate.setText("Please fill out all fields.")
            return False

        if window.validate_dob(new_info) is False:
            self.validate.setText("Please enter date of birth as MM-DD-YYYY.")
            return False

        if window.validate_num(new_info) is False:
            self.validate.setText("Donor number may only contain digits 0-9.")
            return False

        current_donor = window.get_current_donor()
        if new_info["branch"] != current_donor["branch"]:
            if window.validate_branch(new_info) is False:
                self.validate.setText("Branch invalid or full. Please enter another or click 'Find Branch'.")
                return False
            increase = self.increase_branch(current_donor)
            return increase

    def increase_branch(self, donor):
        """
        Increases number of open spots at given branch
        :return: "removed
        """
        center = donor["center"]
        branch = donor["branch"]

        # write given branch and center to text file
        self.write_increase(center, branch)

        # read text file to see if number of spots was increased
        removed = self.read_increase()

        return removed

    def write_increase(self, center, branch):
        """
        Writes branch and center to branch-booking.txt
        :return: None
        """
        # 1 signals to increase number of spots by one
        inp = f"{center},{branch},1"

        file = open("branch-booking.txt", "w")
        file.write(inp)
        file.close()

    def read_increase(self):
        """
        Reads branch-booking.txt to see if donor was successfully removed
        :return: True when removed
        """
        while True:
            time.sleep(1)
            file = open("branch-booking.txt", "r")
            open_branch = file.read()
            file.close()

            # if number of spots has been increased
            if open_branch == "removed":
                return True

    def update_info(self, donors, new_info):
        """
        Updates any changed fields in corresponding donor
        :return: None
        """
        for i in range(len(donors)):
            # find matching donor in list of donors
            if donors[i]["num"] == new_info["num"]:
                # update information
                donors[i] = new_info
                window.set_current_donor(new_info)

                self.banner.setText("Donor information updated.")
                self.banner.show()
                self.close_1.show()
                print(window.get_donors())
                return

    def hide_wind(self):
        """
        Closes donor information window
        :return: None
        """
        # check if changes have been made to donor's information
        donor = window.get_current_donor()
        new_info = self.get_info()
        same = self.compare_info(donor,new_info)

        # no changes made
        if same is True:
            self.hide()

        # changes made
        else:
            self.save_win = SavePopup()
            self.save_win.show()

    def remove_donor(self):
        """
        Displays remove donor popup
        :return: none
        """
        self.remove_win = RemovePopup()
        self.remove_win.show()


class SearchPopup(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("search_popup.ui", self)
        self.back.clicked.connect(self.close_wind)

    def close_wind(self):
        self.close()

class BranchPopup(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("popup.ui", self)
        self.back.clicked.connect(self.close_wind)

    def close_wind(self):
        self.close()


class SavePopup(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("savepopup.ui", self)
        self.save.clicked.connect(self.save_info)
        self.discard.clicked.connect(self.discard_changes)
        self.cancel.clicked.connect(self.cancel_close)

    def save_info(self):
        """
        Saves changes made to donor information before closing donor info window
        :return: none
        """
        # save changes made to donor information
        window.donor_window.save_info()

        # go back to home screen
        self.close()
        window.donor_window.hide()

    def discard_changes(self):
        """
        Closes donor info window without saving changes
        :return: None
        """
        self.close()
        window.donor_window.hide()

    def cancel_close(self):
        """
        Closes save information popup
        :return: none
        """
        self.close()


class RemovePopup(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self._removed = False

        self.ui = uic.loadUi("removepopup.ui", self)

        self.removebutton.clicked.connect(self.remove)

    def get_removed(self):
        return self._removed

    def remove(self):
        """
        Removes donor from list of donors
        :return: None
        """
        donor = window.get_current_donor()
        donors = window.get_donors()

        # increase number of spots at branch at which donor is located
        increase = self.increase_branch(donor)

        # remove donor from dictionary
        removed = self.remove_from_donors(donors, donor)

        if increase is True and removed is True:
            self.hide()
            window.donor_window.hide()
            window.banner.show()
            window.close_2.show()

    def increase_branch(self, donor):
        """
        Increases number of open spots at given branch
        :return: "removed
        """
        center = donor["center"]
        branch = donor["branch"]

        # write given branch and center to text file
        self.write_increase(center, branch)

        # read text file to see if number of spots was increased
        removed = self.read_increase()

        return removed

    def write_increase(self, center, branch):
        """
        Writes branch and center to branch-booking.txt
        :return: None
        """
        # 1 signals to increase number of spots by one
        inp = f"{center},{branch},1"

        file = open("branch-booking.txt", "w")
        file.write(inp)
        file.close()

    def read_increase(self):
        """
        Reads branch-booking.txt to see if donor was successfully removed
        :return: True when removed
        """
        while True:
            time.sleep(1)
            file = open("branch-booking.txt", "r")
            open_branch = file.read()
            file.close()

            # if number of spots has been increased
            if open_branch == "removed":
                return True

    def remove_from_donors(self, donors, donor):
        """
        Removes donor from list of donors
        :return: True if removed successfully
        """
        num = donor["num"]

        for i in donors:
            if i["num"] == num:
                donors.remove(i)
                print(donors)
                return True


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    window.banner.hide()
    window.close_2.hide()
    app.exec()
