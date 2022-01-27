from typing import Container
from pytube import YouTube, Playlist
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout
from PyQt6.QtCore import *
from PyQt6.QtGui import *

# Only needed for access to command line arguments
import sys

# Subclass QMainWindow to customize your application's main window
class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Youtube Downloader")
        self.setFixedSize(QSize(350, 250))

        layout = QVBoxLayout()

        #Title
        self.label = QLabel("Youtube Downloader")
        LabelFont = self.label.font()
        LabelFont.setPointSize(25)
        self.label.setFont(LabelFont)
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.label)

        #Logo Image
        self.logo = QLabel()
        self.pixmap = QPixmap("logo.png")
        self.logoResized = self.pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio)
        self.logo.setPixmap(self.logoResized)
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.logo)

        #Status Label
        self.status = QLabel("Status: Stopped")
        LabelFont = self.status.font()
        LabelFont.setPointSize(10)
        self.status.setFont(LabelFont)
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status)

        #Input
        self.input = QLineEdit(self)
        layout.addWidget(self.input)
        self.input.setPlaceholderText("Paste here URL of the video")

        #Downlaod Button
        self.button = QPushButton("Download Video")
        self.button.setCheckable(True)
        self.button.clicked.connect(self.download_Button_Was_Clicked)
        layout.addWidget(self.button)

        #Playlist Button
        self.PlaylistButton = QPushButton("Download Playlist")
        self.PlaylistButton.setCheckable(True)
        self.PlaylistButton.clicked.connect(self.playlist_Button_Was_Clicked)
        layout.addWidget(self.PlaylistButton)

        #Exit Button
        self.ExitButton = QPushButton("Exit")
        self.ExitButton.setCheckable(True)
        self.ExitButton.clicked.connect(self.exit_Button_Was_Clicked)
        layout.addWidget(self.ExitButton)

        #Container
        container = QWidget()
        container.setLayout(layout)

        # Set the central widget of the Window.
        self.setCentralWidget(container)

    def exit_Button_Was_Clicked(self):
        sys.exit()

    def playlist_Button_Was_Clicked(self):
        if self.input.text():
            p = Playlist(self.input.text())
            for video in p.videos:
                video.streams.first().download()
                self.input.clear()
                self.button.toggle()
                self.status.setText("Status: Downloaded")
        else:
            self.status.setText("Invalid link")
            self.input.clear()
            self.button.toggle()


    def download_Button_Was_Clicked(self):
        if self.input.text():
            yt = YouTube(self.input.text())
            video = yt.streams.get_highest_resolution()
            video.download()    
            self.input.clear()
            self.button.toggle()
            self.status.setText("Status: Downloaded")
        else:
            self.status.setText("Invalid link")
            self.input.clear()
            self.button.toggle()

# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication(sys.argv)

# Create a Qt widget, which will be our window.
window = mainWindow()
window.show()

app.exec()