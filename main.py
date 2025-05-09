import sys
from PyQt6 import QtWidgets
from gui import Ui_MainWindow
import functions


"""
Welcome ot the Song Sorter App Application!
This file is basically used to run the Song Sorter App Application

This program will help you sort out your favorite songs. The user will
enter the name of an artist, a song, and a ranking out of 10! They can 
also include an optional description of the song, like their favoirte lyrics
or something about it that they particularly like. Then the song will be 
added to the file song.csv where users can access all of their favorite 
songs!

Along with that, they can remove a song by typing in the artists name and
the song title to successfully remove a song.

Multi-file structure basically separates the logic to keep things organized. 
"""

def main() -> None:
    """
    Application entry point :p

    :return: None
    """

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    # set up button connections
    functions.setup_connections(ui, MainWindow)

    MainWindow.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()