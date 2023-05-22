# @author: Sanjay Ram RR
# ---------------------

import os
import re
import sys
import random
import requests
import webcolors
from bs4 import BeautifulSoup
from PyQt6.QtCore import Qt, QPoint, QUrl
from PyQt6.QtGui import QImage, QPainter, QColor, QFont, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QStatusBar

# ----------------------------------------------
# Class for Canvas
# ----------------

class Canvas(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.images = []
        self.selected_image = None
        self.offset = QPoint()
        self.setStyleSheet("background-color: #F0F0F0; border: 1px solid #CCCCCC;")

# ----------------------------------------------
# paintEvent
# ----------

    def paintEvent(self, event):
        painter = QPainter(self)
        for image, position in self.images:
            painter.drawImage(position, image)

# ----------------------------------------------
# addImage
# ---------

    def addImage(self, image):
        position = QPoint(
            random.randint(0, self.width() - image.width()),
            random.randint(0, self.height() - image.height())
        )
        self.images.append((image, position))
        self.update()

# ----------------------------------------------
# mousePressEvent
# ----------------

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            position = event.position().toPoint()
            for image, img_position in self.images:
                if image.rect().translated(img_position).contains(position):
                    self.selected_image = image
                    self.offset = position - img_position
                    break

# ----------------------------------------------
# mouseMoveEvent
# ---------------

    def mouseMoveEvent(self, event):
        if self.selected_image:
            new_position = event.position().toPoint() - self.offset
            for i, (image, img_position) in enumerate(self.images):
                if image == self.selected_image:
                    self.images[i] = (image, new_position)
                    self.update()
                    break

# ----------------------------------------------
# Main Function
# --------------

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.selected_image = None

# ----------------------------------------------
# Trigger Canvas reszie whe resizeEvent
# -------------------------------------

    def resizeEvent(self, event):
        self.updateCanvasSize()

# ----------------------------------------------
# Resize the canvas as the window resizes
# ----------------------------------------

    def updateCanvasSize(self):
        for i, (image, position) in enumerate(self.images):
            new_position = QPoint(
                random.randint(0, self.width() - image.width()),
                random.randint(0, self.height() - image.height())
            )
            self.images[i] = (image, new_position)

# ----------------------------------------------
# Window Class
# --------------

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.canvas = Canvas(self)
        self.setCentralWidget(self.canvas)

        self.image_info_label = QLabel(self)
        self.image_info_label.setGeometry(10, 50, 300, 30)
        self.image_info_label.setStyleSheet("font-weight: bold;")

        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)

        download_button = QPushButton("Render Image", self)
        download_button.clicked.connect(self.downloadAndRender)
        download_button.setGeometry(10, 10, 120, 30)
        download_button.setStyleSheet(
            "QPushButton { background-color: #4CAF50; color: white; border: none; font-weight: bold; padding: 8px 16px; }"
            "QPushButton:hover { background-color: #45a049; }"
        )

        group_button = QPushButton("Group Images", self)
        group_button.clicked.connect(self.groupImages)
        group_button.setGeometry(140, 10, 120, 30)
        group_button.setStyleSheet(
            "QPushButton { background-color: #007BFF; color: white; border: none; font-weight: bold; padding: 8px 16px; }"
            "QPushButton:hover { background-color: #0069D9; }"
        )

        # Basic Webscraping for Image Links
        
        url = "https://github.com/hfg-gmuend/openmoji/tree/master/src/symbols/geometric"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        file_links = soup.find_all('a', class_='js-navigation-open')

        self.image_links = []
        for link in file_links:
            href = link.get('href')

            if href.endswith('.svg'):
                image_link = "https://raw.githubusercontent.com/hfg-gmuend/openmoji/44c02495e040c52fbea0bfb1cba89aa24754f9a8/src/symbols/geometric/" + href.replace("/hfg-gmuend/openmoji/blob/master/src/symbols/geometric/", "")
                self.image_links.append(image_link)

# ----------------------------------------------
# Choosing a random image
# -----------------------

    def downloadAndRender(self):
        url = random.choice(self.image_links)
        image = self.downloadImage(url)
        if image:
            self.canvas.addImage(image)
            self.displayImageInfo(image)

# ----------------------------------------------
# Download the image from the source
# ----------------------------------

    def downloadImage(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            image = QImage.fromData(response.content)
            return image
        return None

# ----------------------------------------------
# Group all images in the pos of 1st image
# ----------------------------------------

    def groupImages(self):
        if len(self.canvas.images) > 1:
            # Get the position of the first image
            first_image_position = self.canvas.images[0][1]

            # Set the same position for all the images
            for i, (image, position) in enumerate(self.canvas.images):
                self.canvas.images[i] = (image, first_image_position)

            self.canvas.update()

# ----------------------------------------------
# Displaying the Image Size and Colour
# -------------------------------------

    def displayImageInfo(self, image):
        image_size = f"Size: {image.width()}x{image.height()} pixels"
        image_color = self.getImageDominantColor(image)
        self.image_info_label.setText(f"{image_size} | Color: {image_color.name()}")
        self.statusBar.showMessage("Image information updated.")

# ----------------------------------------------
# Getting the Dominat Colour of that image
# ----------------------------------------

    def getImageDominantColor(self, image):
        image = image.convertToFormat(QImage.Format.Format_RGB888)
        pixels = image.width() * image.height()
        color_count = {}
        for y in range(image.height()):
            for x in range(image.width()):
                color = QColor.fromRgb(image.pixel(x, y))
                if color.isValid():
                    rgb = (color.red(), color.green(), color.blue())
                    if rgb not in color_count:
                        color_count[rgb] = 0
                    color_count[rgb] += 1

        dominant_color_rgb = max(color_count, key=color_count.get)
        dominant_color = QColor.fromRgb(*dominant_color_rgb)
        return dominant_color

# ----------------------------------------------
# Main Function
# --------------

if __name__ == '__main__':

    app = QApplication(sys.argv)
    # Apply global style to the application
    app.setStyleSheet(
        "QMainWindow { background-color: #FFFFFF; }"
        "QLabel { color: #333333; font-size: 14px; }"
    )

    window = Window()
    window.setGeometry(100, 100, 1080, 720)
    window.setWindowTitle("Geometric Images !")
    window.show()

    sys.exit(app.exec())

# -----------------------------------------------
# TODO:
# 1. Print Colour Name instead of Colour Code
# 2. Make improvements to the UI
# 3. Group Only the Selected Images
# -----------------------------------------------