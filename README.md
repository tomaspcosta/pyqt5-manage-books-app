#   PyQt5 Manage Books App

##   Table of Contents

1.  [Project Description](#project-description)
2.  [Technologies Used](#technologies-used)
3.  [Project Structure](#project-structure)
4.  [Features](#features)

##   1. Project Description

This project is a book management application developed with PyQt5. The application allows adding, editing, searching, and deleting books, as well as storing information in a JSON file and managing book images.

This application provides a user interface for managing a collection of books, including features to add new books, modify existing book information, search for books, and remove books from the collection. It also handles the storage of book data in a JSON file and the management of associated book images.

##   2. Technologies Used

* Python 3.x
* PyQt5

##   3. Project Structure

The repository contains the following files and directories:

* `project.py`: The main source code of the application.
* `library.json`: JSON file used to store book data.
* `book_images/`: Directory where uploaded book images are stored.

##   4. Features

* **Add Book:** Fill in fields for title, author, genre, stand, and notes, with the option to add an image. The image is saved in the `book_images/` folder.
* **Edit Book:** Modify book information and update the associated image.
* **Search Book:** Filter books based on title or author.
* **Delete Book:** Remove a book from the list.
* **Manage Stands:** Adjust the number of available stands for books.
