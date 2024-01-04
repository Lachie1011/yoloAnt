"""
    yoloAnt.py
"""

import sys
import signal
from enum import Enum

from PyQt6 import QtCore
from PyQt6.QtCore import QEvent
from PyQt6.QtGui import QCursor, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow

from yoloAnt_ui import Ui_MainWindow

from pages.startPage import StartPage
from pages.projectPage import ProjectPage
from pages.annotationPage import AnnotationPage
from pages.machineLearningPage import MachineLearningPage

from dialogs.infoDialog import InfoDialog

from notificationManager import NotificationManager

from events.hoverEvent import HoverEvent

app = None

class Pages(Enum):
    """ Enum to represent the pages within the application"""
    StartPage=0
    AnnotationPage=1
    ProjectPage=2
    MachineLearningPage=3


class YoloAnt(QMainWindow):
    """
        Class that creates the yoloant application
    """
    def __init__(self) -> None:
        """ init """
        super().__init__()

        self.ui = Ui_MainWindow()
        
        self.ui.setupUi(self)
        
        # Setting up some member variables
        self.currentPage = Pages.StartPage
        self.project = None
        self.infoDialog = None
        
        # Starting the notification manager
        self.notificationManager = NotificationManager(self)

        # Connecting signals and slots for the application
        self.__connectNavigationButtons()
        self.__connectIconHover()
        self.__connectInformationButton()
        self.__connectNotificationButton()

        self.startPage = StartPage(self)
        self.projectPage = ProjectPage(self)
        self.annotationPage = AnnotationPage(self)
        
        # self.installEventFilter(self)

        self.show()
    
    def eventFilter(self, object, event):
        """ Application level event filter """
        if event.type() == QEvent.Type.Resize:
            # resize notifications
            self.notificationManager.resizeNotifications()
            return False
        return False

    def closeEvent(self, event) -> None:
        """ Overrides the close event on the main window """
        # Ensure all notifications are closed
        self.notificationManager.closeNotifications()
        # For now manually close info dialog TODO: have this close nicer
        if self.infoDialog:
            self.infoDialog.close()
        event.accept()

    def __connectNavigationButtons(self) -> None:
        """ Connects the navigation buttons to update the current page of the stacked widget and updates checked state """
        # Connects the currentChanged signal for the stacked widget
        self.ui.stackedWidget.currentChanged.connect(self.__onPageChange)

        # Updates stacked widget index
        self.ui.annotTabBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))    
        self.ui.projectsTabBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))    
        self.ui.mlTabBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(3))

        # Updates the state of the navigation buttons
        self.ui.annotTabBtn.clicked.connect(lambda: self.__updateStateOfNavigationButtons(Pages.AnnotationPage))
        self.ui.projectsTabBtn.clicked.connect(lambda: self.__updateStateOfNavigationButtons(Pages.ProjectPage))
        self.ui.mlTabBtn.clicked.connect(lambda: self.__updateStateOfNavigationButtons(Pages.MachineLearningPage))

    def __updateStateOfNavigationButtons(self, page: Pages) -> None:
        """ Updates the state of the navigation buttons """
        if(page is Pages.AnnotationPage):
            self.currentPage = Pages.AnnotationPage
            # Because of hover event, update check and also icon TODO: explore a cleaner alternative to checking / unchecking
            self.ui.annotTabBtn.setChecked(True)
            self.ui.projectsTabBtn.setChecked(False)
            self.ui.projectsTabBtn.setIcon(QIcon("icons/icons8-project-50.png"))
            self.ui.mlTabBtn.setChecked(False)
            self.ui.mlTabBtn.setIcon(QIcon("icons/icons8-ant-head-50.png"))
            self.ui.infoBtn.setChecked(False)
            self.ui.infoBtn.setIcon(QIcon("icons/icons8-information-50.png"))
        elif(page is Pages.ProjectPage):
            self.currentPage = Pages.ProjectPage
            self.ui.projectsTabBtn.setChecked(True)
            self.ui.annotTabBtn.setChecked(False)
            self.ui.annotTabBtn.setIcon(QIcon("icons/icons8-pencil-50.png"))
            self.ui.mlTabBtn.setChecked(False)
            self.ui.mlTabBtn.setIcon(QIcon("icons/icons8-ant-head-50.png"))
            self.ui.infoBtn.setChecked(False)
            self.ui.infoBtn.setIcon(QIcon("icons/icons8-information-50.png"))
        elif(page is Pages.MachineLearningPage):
            self.currentPage = Pages.MachineLearningPage
            self.ui.mlTabBtn.setChecked(True)
            self.ui.annotTabBtn.setChecked(False)
            self.ui.annotTabBtn.setIcon(QIcon("icons/icons8-pencil-50.png"))
            self.ui.projectsTabBtn.setChecked(False)
            self.ui.projectsTabBtn.setIcon(QIcon("icons/icons8-project-50.png"))
            self.ui.infoBtn.setChecked(False)
            self.ui.infoBtn.setIcon(QIcon("icons/icons8-information-50.png"))

    def __onPageChange(self) -> None: 
        """ Resets some application attributes on a page change """
        # Reset cursor icon
        QApplication.restoreOverrideCursor()

    def __connectInformationButton(self) -> None:
        """ Connects the info button """
        self.ui.infoBtn.clicked.connect(lambda: self.__openInfoDialog(True))

    def __openInfoDialog(self, displayInfoDialog: bool) -> None:
        """ Handles the display of the info dialog box"""
        self.infoDialog = InfoDialog()
        self.notificationManager.raiseNotification("test")
        
        if(displayInfoDialog and not self.infoDialog.isVisible()):
            self.infoDialog.exec()    

    def __connectNotificationButton(self) -> None: 
        """ Connects the notification button """
        self.ui.notificationBtn.clicked.connect(lambda: self.__openNotificationViewer)
    
    def __openNotificationViewer(self) -> None:
        """ Opens the notification viewer """
        self.notificationManager.openNotificationViewer()

    def __connectIconHover(self) -> None:
        """ 
            Installs the hover event filter onto the application navigation buttons
            and updates the cursor icon on hover.
        """
        # Applying hover event and cursor change to annotTabBtn
        self.ui.annotTabBtn.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.annotTabHoverEvent = HoverEvent(self.ui.annotTabBtn, "icons/icons8-pencil-50.png", "icons/icons8-pencil-50-selected.png")
        self.ui.annotTabBtn.installEventFilter(self.annotTabHoverEvent)

        # Applying hover event and cursor change to projectsTabBtn
        self.ui.projectsTabBtn.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.projectsTabHoverEvent = HoverEvent(self.ui.projectsTabBtn, "icons/icons8-project-50.png", "icons/icons8-project-50-selected.png")
        self.ui.projectsTabBtn.installEventFilter(self.projectsTabHoverEvent)

        # Applying hover event and cursor change to mlTabBtn
        self.ui.mlTabBtn.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.mlTabHoverEvent = HoverEvent(self.ui.mlTabBtn, "icons/icons8-ant-head-50.png", "icons/icons8-ant-head-50-selected.png")
        self.ui.mlTabBtn.installEventFilter(self.mlTabHoverEvent)

        # Applying hover event and cursor change to infoBtn
        self.ui.infoBtn.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.infoBtnEvent = HoverEvent(self.ui.infoBtn, "icons/icons8-information-50.png", "icons/icons8-information-50-selected.png")
        self.ui.infoBtn.installEventFilter(self.infoBtnEvent)

        # Applying hover event and cursor change to notificationBtn
        self.ui.notificationBtn.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.notificationBtnEvent = HoverEvent(self.ui.notificationBtn, "icons/icons8-notification-bell-30-inactive.png", "icons/icons8-notification-bell-30-active.png")
        self.ui.notificationBtn.installEventFilter(self.notificationBtnEvent)


def signal_handler(sig, frame) -> None:
    """ Handles unix signals """
    # At the moment we are just worried about sigint and sigterm and both signals are handled the same
    global app
    app.exit(-1)  # Any non-typical exit is an error -1 


def main() -> None:
    """
        main entry point
    """ 
    
    # Handling application signals that are not handled by QT
    signal.signal(signal.SIGINT, signal_handler)  # SIGINT
    signal.signal(signal.SIGTERM, signal_handler)  # SIGTERM

    # Starting application
    global app  # Using a global reference for the signal handling - might be something better here
    app = QApplication(sys.argv)

    YoloAnt()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()