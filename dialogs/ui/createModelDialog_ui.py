# Form implementation generated from reading ui file 'ui/createModelDialog.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_createModelDialog(object):
    def setupUi(self, createModelDialog):
        createModelDialog.setObjectName("createModelDialog")
        createModelDialog.resize(400, 160)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(createModelDialog.sizePolicy().hasHeightForWidth())
        createModelDialog.setSizePolicy(sizePolicy)
        createModelDialog.setMinimumSize(QtCore.QSize(400, 160))
        createModelDialog.setMaximumSize(QtCore.QSize(400, 160))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        createModelDialog.setFont(font)
        createModelDialog.setStyleSheet("")
        self.verticalLayout = QtWidgets.QVBoxLayout(createModelDialog)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.mainFrame = QtWidgets.QFrame(parent=createModelDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainFrame.sizePolicy().hasHeightForWidth())
        self.mainFrame.setSizePolicy(sizePolicy)
        self.mainFrame.setStyleSheet("background-color: #454545;")
        self.mainFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.mainFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.mainFrame.setObjectName("mainFrame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.mainFrame)
        self.verticalLayout_2.setContentsMargins(-1, -1, -1, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.modelFrame = QtWidgets.QFrame(parent=self.mainFrame)
        self.modelFrame.setMinimumSize(QtCore.QSize(0, 50))
        self.modelFrame.setMaximumSize(QtCore.QSize(16777215, 50))
        self.modelFrame.setStyleSheet("border: 5px solid;\n"
"border-color: #454545;")
        self.modelFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.modelFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.modelFrame.setObjectName("modelFrame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.modelFrame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.modelNameLbl = QtWidgets.QLabel(parent=self.modelFrame)
        self.modelNameLbl.setMinimumSize(QtCore.QSize(120, 30))
        self.modelNameLbl.setMaximumSize(QtCore.QSize(120, 30))
        self.modelNameLbl.setStyleSheet("font: 75 bold 12pt \"Gotham Rounded\";\n"
"color: rgb(136, 138, 133);")
        self.modelNameLbl.setObjectName("modelNameLbl")
        self.horizontalLayout.addWidget(self.modelNameLbl)
        self.modelLineEdit = QtWidgets.QLineEdit(parent=self.modelFrame)
        self.modelLineEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.modelLineEdit.setMaximumSize(QtCore.QSize(16777215, 30))
        self.modelLineEdit.setStyleSheet("font: 75 bold 12pt \"Gotham Rounded\";\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(85, 87, 83);\n"
"border: 5px solid;\n"
"border-radius: 5px;\n"
"border-color:  rgb(85, 87, 83);")
        self.modelLineEdit.setObjectName("modelLineEdit")
        self.horizontalLayout.addWidget(self.modelLineEdit)
        self.verticalLayout_2.addWidget(self.modelFrame)
        self.createFrame = QtWidgets.QFrame(parent=self.mainFrame)
        self.createFrame.setMinimumSize(QtCore.QSize(0, 50))
        self.createFrame.setMaximumSize(QtCore.QSize(16777215, 50))
        self.createFrame.setStyleSheet("border: 5px solid;\n"
"border-color: #454545;")
        self.createFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.createFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.createFrame.setObjectName("createFrame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.createFrame)
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.createModelBtn = QtWidgets.QPushButton(parent=self.createFrame)
        self.createModelBtn.setMinimumSize(QtCore.QSize(140, 30))
        self.createModelBtn.setMaximumSize(QtCore.QSize(140, 30))
        self.createModelBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.createModelBtn.setStyleSheet("background-color: rgb(65, 66, 64);\n"
"border : 1px solid;\n"
"border-radius: 10px;\n"
"border-color:  rgb(85, 87, 83);\n"
"font: 75 bold 12pt \"Gotham Rounded\";\n"
"color: rgb(255, 255, 255);")
        self.createModelBtn.setObjectName("createModelBtn")
        self.horizontalLayout_3.addWidget(self.createModelBtn)
        self.importModelBtn = QtWidgets.QPushButton(parent=self.createFrame)
        self.importModelBtn.setMinimumSize(QtCore.QSize(140, 30))
        self.importModelBtn.setMaximumSize(QtCore.QSize(140, 30))
        self.importModelBtn.setStyleSheet("background-color: rgb(65, 66, 64);\n"
"border : 1px solid;\n"
"border-radius: 10px;\n"
"border-color:  rgb(85, 87, 83);\n"
"font: 75 bold 12pt \"Gotham Rounded\";\n"
"color: rgb(255, 255, 255);")
        self.importModelBtn.setObjectName("importModelBtn")
        self.horizontalLayout_3.addWidget(self.importModelBtn)
        self.verticalLayout_2.addWidget(self.createFrame)
        self.verticalLayout.addWidget(self.mainFrame)

        self.retranslateUi(createModelDialog)
        QtCore.QMetaObject.connectSlotsByName(createModelDialog)

    def retranslateUi(self, createModelDialog):
        _translate = QtCore.QCoreApplication.translate
        createModelDialog.setWindowTitle(_translate("createModelDialog", "Create Model"))
        self.modelNameLbl.setText(_translate("createModelDialog", "Model Name"))
        self.createModelBtn.setText(_translate("createModelDialog", "Create New"))
        self.importModelBtn.setText(_translate("createModelDialog", "Import Existing"))