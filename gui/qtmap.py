# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'map.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
import cons.cst


class Ui_MainWindow(object):
    # Attributes
    positions = {}
    last_seen = {}
    markers = {}
    marker_labels = {}
    marker_texts = {}

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1366, 768)
        MainWindow.setMinimumSize(QtCore.QSize(1366, 768))
        MainWindow.setMaximumSize(QtCore.QSize(1366, 768))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.map = QtWidgets.QLabel(self.centralwidget)
        self.map.setGeometry(QtCore.QRect(10, 20, 1366, 768))
        self.map.setMinimumSize(QtCore.QSize(1366, 768))
        self.map.setMaximumSize(QtCore.QSize(1366, 768))
        self.map.setText("")
        self.map.setPixmap(QtGui.QPixmap(r"../gui/img/theskeld.png"))
        self.map.setScaledContents(True)
        self.map.setObjectName("map")

        '''
        self.marker = QtWidgets.QLabel(self.centralwidget)
        self.marker.setGeometry(QtCore.QRect(710, 170, 50, 42))
        self.marker.setMinimumSize(QtCore.QSize(50, 42))
        self.marker.setMaximumSize(QtCore.QSize(50, 42))
        self.marker.setText("")
        self.marker.setPixmap(QtGui.QPixmap("../gui/img/marker_red.png"))
        self.marker.setScaledContents(True)
        self.marker.setObjectName("marker")
        self.marker_time = QtWidgets.QLabel(self.centralwidget)
        self.marker_time.setGeometry(QtCore.QRect(710, 220, 47, 13))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.marker_time.setFont(font)
        self.marker_time.setAlignment(QtCore.Qt.AlignCenter)
        self.marker_time.setObjectName("marker_time")
        self.marker_time.setText("7s")
        '''
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        MainWindow.setWindowTitle("CrewHelp")
        MainWindow.setWindowIcon(QIcon('../gui/img/icon.png'))

        # self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("CrewHelp", "CrewHelp"))
        MainWindow.setWindowIcon(QIcon('../gui/img/icon.png'))
        self.marker_time.setText(_translate("MainWindow", "7s"))

    def set_attributes(self, player_positions, player_last_seen):
        self.positions = player_positions
        self.last_seen = player_last_seen

    # Set markers at corresponding positions
    def set_markers(self):
        for color in cons.cst.colors:
            if self.positions[color]:
                # get position of room
                room = self.positions[color]
                # get marker at this position
                self.markers.update({color: cons.cst.marker_positions[room]})
            else:
                self.markers.update({color: None})

    # Display markers
    def display_markers(self, time=True):
        y_shift = 13
        x_shift = 55
        tmp = {}  # Temporary dict used to shift text down when multiple colors are in the same room
        for color in cons.cst.colors:
            # Display icon
            if self.markers[color]:

                # If it's the first time looping on this room then create a key for it
                if self.markers[color] not in tmp:
                    tmp.update({self.markers[color]: 1})

                # Otherwise increment the count for this room
                else:
                    tmp[self.markers[color]] = tmp[self.markers[color]] + 1

                # display marker at position
                self.marker_labels[color] = QtWidgets.QLabel(self.centralwidget)
                self.marker_labels[color].setGeometry(QtCore.QRect(self.markers[color][0] + x_shift * tmp[
                                                                       self.markers[color]],
                                                                   self.markers[color][1],
                                                                   50, 42))
                self.marker_labels[color].setPixmap(QtGui.QPixmap(r'../gui/img/marker_' + color + '.png'))
                self.marker_labels[color].setScaledContents(True)

                # Display timings
                if time:
                    # Display text
                    self.marker_texts[color] = QtWidgets.QLabel(self.centralwidget)
                    self.marker_texts[color].setGeometry(QtCore.QRect(self.markers[color][0] + x_shift * tmp[
                                                                       self.markers[color]],
                                                                      self.markers[color][1] + 42,
                                                                      47, 13))
                    font = QtGui.QFont()
                    font.setFamily("Arial")
                    font.setPointSize(11)
                    font.setBold(True)
                    font.setWeight(75)
                    font.setKerning(True)
                    self.marker_texts[color].setFont(font)
                    self.marker_texts[color].setAlignment(QtCore.Qt.AlignCenter)
                    self.marker_texts[color].setText(str(int(self.last_seen[color])))

                    '''
                    cv.putText(self.map, color + ' : ' + str(int(self.last_seen[color])) + 's',
                               (
                                   self.markers[color][0], self.markers[color][1] + y_shift * tmp[self.markers[color]]),
                               cv.FONT_HERSHEY_PLAIN, 1.1, cons.cst.bgr_colors[color], 1, cv.LINE_AA)
                    '''


# Display window
def display(player_positions, player_last_seen):
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(main_window)
    ui.set_attributes(player_positions, player_last_seen)
    ui.set_markers()
    ui.display_markers()
    main_window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    # ui.set_attributes()
    MainWindow.show()

    sys.exit(app.exec_())
