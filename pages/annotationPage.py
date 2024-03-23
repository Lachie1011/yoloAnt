"""
    annotationPage.py
"""

import sys
from enum import Enum

from PyQt6 import QtCore
from PyQt6.QtGui import QCursor, QIcon, QColor
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QLabel, QVBoxLayout, QPushButton, QFrame, QGraphicsDropShadowEffect, QSpacerItem, QSizePolicy

from yoloAnt_ui import Ui_MainWindow
from image import Image
from events.hoverEvent import HoverEvent
# from events.resizeEvent import ResizeEvent
from events.resizeEvent import ResizeEvent
from customWidgets.customQObjects import CustomClassQListWidget, UserInputQLineEdit
from customWidgets.annotationClassSelectionWidget import AnnotationClassSelectionWidget


class NavigationModes(Enum):
    """ 
        Enum to represent different canvas navigation modes 
    """
    next=0
    previous=1
    nextUnannotated=2
    previousUnannotated=3


class Tools(Enum):
    """ 
        Enum to represent the annotation tools within the page
    """
    mouseTool=0
    annotationTool=1


class AnnotationPage():
    """
        Class to set up the functionality for the annotation page
    """
    def __init__(self, app) -> None:
        # TODO: fix up app type to yoloant app involes add future annotations and some if typing
        self.app = app
        self.ui = app.ui
        self.__setupStyleSheet()
        self.__setupPagePalette()

        # Page attributes:
        self.currentIndex = 0
        self.pageInitialised = False
        
        # Dict to hold the unannotatedImages TODO: probs could be made into some kind of Kd tree to make searching faster
        self.unannotatedImages = {}
        # Connecting signals and slots for the page
        self.__connectIconHover()
        self.__connectAnnotationToolButtons()
        self.__connectImageNavigationButtons()

    def loadPage(self):
        """ Loads all information and functionality """ 
        if len(self.app.project.annotationDataset) < 0:
            self.app.notificationManager.raiseNotification("Dataset contains no images")
            return

        if not self.pageInitialised:
            # Creating metadata for inital image
            self.app.project.annotationDataset[self.currentIndex].createMetadata()
            self.app.ui.annotationCanvasWidget.updateImage(self.app.project.annotationDataset[self.currentIndex])
            self.pageInitialised = True

    def __connectImageNavigationButtons(self):
        """ Connects the buttons used to navigate throughout the canvas"""
        self.app.ui.nextImageBtn.clicked.connect(lambda: self.__navigateCanvasWidget(NavigationModes.next))
        self.app.ui.prevImageBtn.clicked.connect(lambda: self.__navigateCanvasWidget(NavigationModes.previous))
        self.app.ui.nextUnannoImageBtn.clicked.connect(lambda: self.__navigateCanvasWidget(NavigationModes.nextUnannotated))
        self.app.ui.prevUnannoImageBtn.clicked.connect(lambda: self.__navigateCanvasWidget(NavigationModes.previousUnannotated))
    
    def __navigateCanvasWidget(self, navigationType):
        """ Logic for page navigation """
        # TODO: this logic assumes that a new image will be found only when moving next not previously
        self.__checkImageState(self.app.project.annotationDataset[self.currentIndex])
        if navigationType is NavigationModes.next:
            if (self.currentIndex + 1) < len(self.app.project.dataset):
                # Setup the next image
                nextImage = self.app.project.annotationDataset[self.currentIndex + 1]
                nextImage.createMetadata()
                if nextImage.isValid:
                    # go to next image
                    self.app.ui.annotationCanvasWidget.updateImage(nextImage)
                    self.currentIndex = self.currentIndex + 1
                else:
                    # TODO: If the image is not valid show blank image / skip ahead to the next valid image??
                    self.app.notificationManager.raiseNotification(f"Image: {0} is not valid", nextImage.path)
        if navigationType is NavigationModes.previous:
            if (self.currentIndex - 1) >= 0:
                self.app.ui.annotationCanvasWidget.updateImage(self.app.project.annotationDataset[self.currentIndex - 1])
                self.currentIndex = self.currentIndex - 1
        if navigationType is NavigationModes.nextUnannotated:
            closestIndex = None
            # Check cache first
            if self.unannotatedImages:
                for _, index in self.unannotatedImages.items():
                    if index > self.currentIndex:
                        if closestIndex is None:
                            closestIndex = index
                        if (index < closestIndex) and index != self.currentIndex:
                            closestIndex = index
                            
            # If we couldnt find anything in the cache, check annotation dataset 
            if closestIndex is None:
                for i in range(self.currentIndex + 1, len(self.app.project.annotationDataset) - 1):
                    if not self.app.project.annotationDataset[i].annotated:
                        closestIndex = i
                        break
            if closestIndex is not None:
                self.app.ui.annotationCanvasWidget.updateImage(self.app.project.annotationDataset[closestIndex])
                self.currentIndex = closestIndex 
        if navigationType is NavigationModes.previousUnannotated:
            closestIndex = None
            # check the cache first
            if self.unannotatedImages:
                for _, index in self.unannotatedImages.items():
                    if index < self.currentIndex:
                        if closestIndex is None:
                            closestIndex = index
                        if (index > closestIndex) and index != self.currentIndex:
                            closestIndex = index
            # if we couldnt find anything in the cache, check annotation dataset
            if closestIndex is None:
                for i in range(self.currentIndex - 1, len(self.app.project.annotationDataset), -1):
                    if not self.app.project.annotationDataset[i].annotated:
                        closestIndex = i
                        break
            if closestIndex is not None:
                self.app.ui.annotationCanvasWidget.updateImage(self.app.project.annotationDataset[closestIndex])
                self.currentIndex = closestIndex
        
    def __checkImageState(self, image) -> None:
        """ Checks the current images state and updates related properties """
        if image.annotated and (image in self.unannotatedImages):
            self.unannotatedImages.pop(image)
        if not image.annotated:
            self.unannotatedImages.update({self.app.project.annotationDataset[self.currentIndex]:self.currentIndex})

    def __setupPagePalette(self) -> None:
        """ Sets the colour palette for the page widgets """  
        self.ui.imageFrame.setStyleSheet(self.ui.imageFrame.styleSheet() +
                                         f"background: {self.app.theme.colours['app.sunken']};")   

        dropshadowEffect1 = QGraphicsDropShadowEffect()
        dropshadowEffect1.setBlurRadius(10)
        color = QColor(self.app.theme.colours['app.dropshadow'])
        dropshadowEffect1.setColor(color)
        dropshadowEffect1.setOffset(0,2)
        self.ui.classSelectionFrame.setGraphicsEffect(dropshadowEffect1)
        self.ui.classSelectionFrame.setStyleSheet(self.ui.classSelectionFrame.styleSheet() + 
                                             f"background: {self.app.theme.colours['panel.background']};")   

        dropshadowEffect2 = QGraphicsDropShadowEffect()
        dropshadowEffect2.setBlurRadius(10)
        color = QColor(self.app.theme.colours['app.dropshadow'])
        dropshadowEffect2.setColor(color)
        dropshadowEffect2.setOffset(0,2) 
        self.ui.imageInfoFrame.setGraphicsEffect(dropshadowEffect2)
        self.ui.imageInfoFrame.setStyleSheet(self.ui.imageInfoFrame.styleSheet() +
                                             f"background: {self.app.theme.colours['panel.background']};") 
        
        dropshadowEffect3 = QGraphicsDropShadowEffect()
        dropshadowEffect3.setBlurRadius(10)
        color = QColor(self.app.theme.colours['app.dropshadow'])
        dropshadowEffect3.setColor(color)
        dropshadowEffect3.setOffset(0,2)  
        self.ui.annotationToolsFrame.setGraphicsEffect(dropshadowEffect3)
        self.ui.annotationToolsFrame.setStyleSheet(self.ui.annotationToolsFrame.styleSheet() + 
                                                   f"background: {self.app.theme.colours['panel.background']};")
        # self.ui.classSelectAnnoPageFrame.setStyleSheet(self.ui.classSelectAnnoPageFrame.styleSheet() +
        #                                                f"background: {self.app.theme.colours['panel.sunken']};")    
    def __setupStyleSheet(self) -> None:
        """ Sets the style sheet for the page """
        # Setup annotation class selection frame
        self.annotationClassSelectionWidget = AnnotationClassSelectionWidget(self.ui, self.app.theme.colours, self.app.fontTypeRegular, self.app.fontTypeTitle)

        # Status combobox style
        self.ui.statusComboBox.setStyleSheet("QComboBox{"
                                             f"font: 75 12pt {self.app.fontTypeRegular};"
                                             f"background-color: {self.app.theme.colours['panel.sunken']};}}"
                                             "QComboBox::drop-down:button{"
                                             f"background-color: {self.app.theme.colours['panel.sunken']};"
                                             "border-radius: 5px}"
                                             "QComboBox::drop-down{"
                                             f"color: {self.app.theme.colours['panel.sunken']};}}"
                                             "QComboBox::down-arrow{"
                                             "image: url(icons/icons8-drop-down-arrow-10.png)}")

    def __connectIconHover(self) -> None:
        """ 
            Installs the hover event filter onto the image navigation buttons
            and the annotation tool buttons.
        """
        
        # Applying hover events and cursor change to Navigation Buttons
        self.ui.prevUnannoImageBtn.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.prevUnannoBtnHoverEvent = HoverEvent(self.ui.prevUnannoImageBtn, "icons/icons8-chevron-prev-30.png", "icons/icons8-chevron-prev-30-selected.png")
        self.ui.prevUnannoImageBtn.installEventFilter(self.prevUnannoBtnHoverEvent)

        self.ui.prevImageBtn.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.prevBtnHoverEvent = HoverEvent(self.ui.prevImageBtn, "icons/icons8-chevron-left-30.png", "icons/icons8-chevron-left-30-selected.png")
        self.ui.prevImageBtn.installEventFilter(self.prevBtnHoverEvent)

        self.ui.nextImageBtn.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.nextBtnHoverEvent = HoverEvent(self.ui.nextImageBtn, "icons/icons8-chevron-right-30.png", "icons/icons8-chevron-right-30-selected.png")
        self.ui.nextImageBtn.installEventFilter(self.nextBtnHoverEvent)

        self.ui.nextUnannoImageBtn.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.nextUnannoBtnHoverEvent = HoverEvent(self.ui.nextUnannoImageBtn, "icons/icons8-chevron-next-30.png", "icons/icons8-chevron--next-30-selected.png")
        self.ui.nextUnannoImageBtn.installEventFilter(self.nextUnannoBtnHoverEvent)
      
        # Applying hover events and cursor change to Tool Selection Buttons 
        self.ui.mouseToolBtn.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.mouseBtnHoverEvent = HoverEvent(self.ui.mouseToolBtn, "icons/cursor-inactive.png", "icons/cursor-active.png")
        self.ui.mouseToolBtn.installEventFilter(self.mouseBtnHoverEvent)

        self.ui.annotateToolBtn.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.annotateBtnHoverEvent = HoverEvent(self.ui.annotateToolBtn, "icons/bounding-inactive.png", "icons/bounding-active.png")
        self.ui.annotateToolBtn.installEventFilter(self.annotateBtnHoverEvent)
    
    def __connectAnnotationToolButtons(self) -> None:
        """ Connects the annotation buttons to update the mouse icon as well as checked state """
        self.ui.mouseToolBtn.clicked.connect(lambda: self.__connectAnnotationToolSelected(Tools.mouseTool))
        self.ui.annotateToolBtn.clicked.connect(lambda: self.__connectAnnotationToolSelected(Tools.annotationTool))

    def __connectAnnotationToolSelected(self, tool: Tools) -> None:
        """ Updates the mouse icon based on selected tool """
        if tool is Tools.mouseTool:
            # updating checked state
            self.ui.annotateToolBtn.setChecked(False)
            self.ui.annotateToolBtn.setIcon(QIcon("icons/bounding-inactive.png"))
            # update mouse icon
            QApplication.restoreOverrideCursor()

            # Updating annotationCanvasWidget mode
            self.ui.annotationCanvasWidget.mode = Tools.mouseTool

        if tool is Tools.annotationTool:
            # updating checked state
            self.ui.mouseToolBtn.setChecked(False)
            self.ui.mouseToolBtn.setIcon(QIcon("icons/cursor-inactive.png"))
            # update mouse icon
            QApplication.setOverrideCursor(QtCore.Qt.CursorShape.CrossCursor)

            # Updating annotationCanvasWidget mode
            self.ui.annotationCanvasWidget.mode = Tools.annotationTool
