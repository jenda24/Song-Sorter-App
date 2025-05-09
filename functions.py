import csv
import os
from PyQt6 import QtCore

"""
This file contains the functions that are used to bring this Song
Sorter to life.

1. The save_song function is simply used to save songs
2. The remove_song function is used to remove songs
3. The setup_connections function is used to connect the buttons
   to their respective functions.
"""

def save_song(ui) -> bool:
    """
    This function saves song information to songs.csv.
    It also validates required fields and updates user feedback
    if necessary.

    :param ui: This is the ui instance containing input feilds
    :return: True if song was saved successfully, False otherwise
    """

    # first, get data from input fields
    artist = ui.add_artist_input.toPlainText().strip()
    title = ui.add_title_input.toPlainText().strip()
    rating = ui.rating.currentText()
    description = ui.user_description.toPlainText().strip()

    # make sure all of the information is filled out!
    if not artist or not title:
        ui.add_song_label.setText("ADD A SONG: Missing information!")
        ui.add_song_label.setStyleSheet("color: red;")
        return False

    # reset label if validation passes
    ui.add_song_label.setText("ADD A SONG:")
    ui.add_song_label.setStyleSheet("")

    # set default description if empty
    if not description:
        description = "N/A"

    # create CSV file with headers if it doesn't exist
    file_exists = os.path.isfile('songs.csv')

    with open('songs.csv', 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["Artist Name", "Song Title", "Rating", "Description"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # write headers if file is new
        if not file_exists:
            writer.writeheader()

        # write song data
        writer.writerow({
            "Artist Name": artist,
            "Song Title": title,
            "Rating": rating,
            "Description": description
        })

    # clear input fields after successful save
    ui.add_artist_input.clear()
    ui.add_title_input.clear()
    ui.user_description.clear()
    ui.rating.setCurrentIndex(0)  # Reset to first rating option

    # Display success message
    ui.message_to_user.setText("Song added successfully!")
    QtCore.QTimer.singleShot(3000, lambda: ui.message_to_user.setText(""))

    return True


def remove_song(ui) -> bool:
    """
    THis function removes a song from the CSV file based on artist
    and title. Both are needed to prevent multiple songs from being removed.

    If the user doesn't provide both, the song will NOT be removed and
    error messgaes will be sent using the remove_song_label.

    When a song is removed, the entire spngs.csv file is quickly rewritten,
    without the song that has just been removed.

    :param ui: The ui instance containing input fields
    :return: True if song was removed successfully, False otherwise
    """

    # get removal criteria
    artist = ui.remove_artist_input.toPlainText().strip()
    title = ui.remove_title_input.toPlainText().strip()

    # validate removal criteria
    if not artist or not title:
        ui.remove_song_label.setText("REMOVE A SONG: Missing information!")
        ui.remove_song_label.setStyleSheet("color: red;")
        return False

    # reset label if validation passes
    ui.remove_song_label.setText("REMOVE A SONG:")
    ui.remove_song_label.setStyleSheet("")

    # check if file exists
    if not os.path.isfile('songs.csv'):
        ui.message_to_user.setText("No songs to remove!")
        QtCore.QTimer.singleShot(3000, lambda: ui.message_to_user.setText(""))
        return False

    # read existing songs
    songs = []
    found = False

    with open('songs.csv', 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # skip the song to be removed
            if row["Artist Name"].lower() == artist.lower() and row["Song Title"].lower() == title.lower():
                found = True
                continue
            songs.append(row)

    if not found:
        ui.message_to_user.setText("Song not found!")
        QtCore.QTimer.singleShot(3000, lambda: ui.message_to_user.setText(""))
        return False

    # write back all songs except the removed one
    with open('songs.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["Artist Name", "Song Title", "Rating", "Description"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for song in songs:
            writer.writerow(song)

    # clear remove input fields after successful removal
    ui.remove_artist_input.clear()
    ui.remove_title_input.clear()

    # display success message
    ui.message_to_user.setText("Song removed successfully!")
    QtCore.QTimer.singleShot(3000, lambda: ui.message_to_user.setText(""))

    return True


def setup_connections(ui, main_window) -> None:
    """
    Connect the save and remove buttons to their  functions.

    :param ui: The UI instance containing buttons
    :param main_window: The main window instance
    :return: None
    """
    ui.save_button.clicked.connect(lambda: save_song(ui))
    ui.remove_button.clicked.connect(lambda: remove_song(ui))