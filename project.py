import os, json, sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QMessageBox, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QGroupBox, QDialog, QFormLayout, QDialogButtonBox, QComboBox, QFileDialog, QScrollArea, QGridLayout, QSizePolicy, QSpinBox, QTextEdit,
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, pyqtSignal, QSize

def get_stylesheet():
    return """
        QWidget {
            background-color: #2E2E2E;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        QPushButton {
            background-color: #3A3A3A;
            border: 1px solid #555;
            color: white;
            padding: 10px 20px;
            font-size: 14px;
            border-radius: 5px;
            margin: 5px 0;
        }

        QPushButton:hover {
            background-color: #555;
        }

        QLineEdit, QTextBrowser, QTextEdit {
            background-color: #3A3A3A;
            color: white;
            border: 1px solid #555;
            border-radius: 5px;
            padding: 10px;
            font-size: 14px;
        }

        QGroupBox {
            background-color: #3A3A3A;
            border: 1px solid #555;
            border-radius: 5px;
            padding: 10px;
            margin-top: 10px;
            color: white;
        }

        /* Styling for QGroupBox title */
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top center;
            padding: 5px;
            font-weight: bold; /* Ensure the title text is bold */
        }

        QLabel {
            color: #FFFFFF;
            font-size: 16px;
            margin-bottom: 5px;
        }

        QFrame {
            background-color: #3A3A3A;
            border: 1px solid #555;
            border-radius: 5px;
        }

        QPushButton#stand_button {
            background-color: #555;
        }

        QPushButton#stand_button:hover {
            background-color: #777;
        }

        QPushButton#stand_button:selected {
            background-color: #FF4500;
        }
    """

class HomeLibraryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.books = []
        self.stands = ["No stand yet"] + [f"Stand {i}" for i in range(1, 21)]
        self.initUI()

    def initUI(self):
        self.setWindowTitle("OOP Project [Home Library]")
        self.setMinimumSize(800, 600)

        self.setStyleSheet(get_stylesheet())

        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        left_layout = QVBoxLayout()
        main_layout.addLayout(left_layout)

        self.book_group = QGroupBox("BOOK MANAGEMENT")
        self.book_layout = QVBoxLayout()
        self.book_group.setLayout(self.book_layout)
        left_layout.addWidget(self.book_group)

        self.add_book_button = QPushButton("➕ Add Book")
        self.add_book_button.clicked.connect(self.add_book)
        self.book_layout.addWidget(self.add_book_button)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search")
        self.search_input.textChanged.connect(self.search_books)
        self.book_layout.addWidget(self.search_input)

        self.edit_library_button = QPushButton("Edit Library")
        self.edit_library_button.clicked.connect(self.edit_library)
        left_layout.addWidget(self.edit_library_button)

        self.book_group.setMinimumWidth(240)
        self.book_group.setMaximumWidth(240)
        self.book_group.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        left_layout.addStretch(1)

        right_layout = QVBoxLayout()
        main_layout.addLayout(right_layout)

        self.book_list_label = QLabel("📚 My Books List:")
        right_layout.addWidget(self.book_list_label)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        right_layout.addWidget(self.scroll_area)

        self.book_list_widget = QWidget()
        self.book_grid_layout = QGridLayout()
        self.book_grid_layout.setAlignment(Qt.AlignTop)
        self.book_list_widget.setLayout(self.book_grid_layout)
        self.scroll_area.setWidget(self.book_list_widget)

        self.load_books_from_json()

    def edit_library(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Library")
        dialog_layout = QVBoxLayout(dialog)

        current_stands = (
            len(self.stands) - 1
        )  # Subtract 1 for the "No stand yet" option

        stands_label = QLabel("Number of Stands")
        stands_label.setAlignment(Qt.AlignCenter)
        dialog_layout.addWidget(stands_label)

        stands_spinbox = QSpinBox()
        stands_spinbox.setStyleSheet("background-color: white;")
        stands_spinbox.setValue(current_stands)
        dialog_layout.addWidget(stands_spinbox)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        dialog_layout.addWidget(button_box)

        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        if dialog.exec_() == QDialog.Accepted:
            new_stands = stands_spinbox.value()
            if new_stands > current_stands:
                self.stands += [
                    f"Stand {i}" for i in range(current_stands + 1, new_stands + 1)
                ]
            elif new_stands < current_stands:
                self.stands = self.stands[: new_stands + 1]

    def delete_book(self, index):
        confirm = QMessageBox.question(
            self,
            "Delete Book",
            "Are you sure you want to delete this book?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirm == QMessageBox.Yes:
            del self.books[index]
            self.update_book_list()
            self.save_books_to_json()
            self.sender().parent().parent().close()

    def add_book(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Book")
        dialog_layout = QFormLayout(dialog)

        # Create the input fields
        title_edit = QLineEdit()
        author_edit = QLineEdit()
        genre_edit = QLineEdit()
        stand_edit = QComboBox()
        stand_edit.addItems(self.stands)
        notes_edit = QTextEdit()

        # Create the labels with a fixed width and center-aligned text
        label_width = 100
        title_label = QLabel("Title:")
        title_label.setFixedWidth(label_width)
        title_label.setAlignment(Qt.AlignCenter)
        
        author_label = QLabel("Author:")
        author_label.setFixedWidth(label_width)
        author_label.setAlignment(Qt.AlignCenter)
        
        genre_label = QLabel("Genre:")
        genre_label.setFixedWidth(label_width)
        genre_label.setAlignment(Qt.AlignCenter)
        
        stand_label = QLabel("Stand:")
        stand_label.setFixedWidth(label_width)
        stand_label.setAlignment(Qt.AlignCenter)
        
        notes_label = QLabel("Notes:")
        notes_label.setFixedWidth(label_width)
        notes_label.setAlignment(Qt.AlignCenter)

        # Add the labels and input fields to the form layout
        dialog_layout.addRow(title_label, title_edit)
        dialog_layout.addRow(author_label, author_edit)
        dialog_layout.addRow(genre_label, genre_edit)
        dialog_layout.addRow(stand_label, stand_edit)
        dialog_layout.addRow(notes_label, notes_edit)

        image_edit_button = QPushButton("Add Image 📤")
        dialog_layout.addRow(image_edit_button)

        def select_image():
            image_path, _ = QFileDialog.getOpenFileName(
                self, "Select Book Image", "", "Images (*.png *.jpg *.jpeg)"
            )
            if image_path:
                image_edit_button.setText(
                    f"Image Selected: {os.path.basename(image_path)}"
                )
                image_edit_button.image_path = image_path

        image_edit_button.clicked.connect(select_image)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        dialog_layout.addWidget(button_box)

        def validate_and_accept():
            title = title_edit.text().strip()
            author = author_edit.text().strip()
            genre = genre_edit.text().strip()
            
            missing_fields = []
            if not title:
                missing_fields.append(("Title", title_edit))
            if not author:
                missing_fields.append(("Author", author_edit))
            if not genre:
                missing_fields.append(("Genre", genre_edit))

            if missing_fields:
                QMessageBox.warning(dialog, "Validation Error", f"You need to fill {', '.join(field[0] for field in missing_fields)}.")
                missing_fields[0][1].setFocus()
                return
            
            stand = stand_edit.currentText()
            notes = notes_edit.toPlainText()

            if hasattr(image_edit_button, "image_path"):
                image_path = image_edit_button.image_path
            else:
                image_path = ""

            book = {
                "title": title,
                "author": author,
                "genre": genre,
                "stand": stand,
                "notes": notes,
                "image_path": image_path,
            }
            self.books.append(book)
            self.update_book_list()
            self.save_books_to_json()
            dialog.accept()

        button_box.accepted.connect(validate_and_accept)
        button_box.rejected.connect(dialog.reject)

        dialog.exec_()


    def search_books(self):
        search_text = self.search_input.text().lower()
        search_results = [
            book
            for book in self.books
            if search_text in book["title"].lower()
            or search_text in book["author"].lower()
        ]
        self.update_book_list(search_results)

    def update_book_list(self, books=None):
        if books is None:
            books = self.books

        # Clear the current book grid layout
        for i in reversed(range(self.book_grid_layout.count())):
            widget_to_remove = self.book_grid_layout.itemAt(i).widget()
            self.book_grid_layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

        # Calculate the number of columns based on available width and preferred width of each tile
        available_width = self.scroll_area.viewport().width()
        tile_width = 160
        min_columns = 1
        max_columns = max(1, available_width // tile_width)
        columns = min(max_columns, len(books))

        # Set a fixed size for each book tile
        tile_size = QSize(tile_width, 250)

        row = 0
        col = 0
        for index, book in enumerate(books):
            if col == columns:
                col = 0
                row += 1

            book_widget = QWidget()
            book_layout = QVBoxLayout()
            book_widget.setLayout(book_layout)

            if "image_path" in book and os.path.exists(book["image_path"]):
                pixmap = QPixmap(book["image_path"])
                book_image_label = ClickableLabel()
                book_image_label.setPixmap(pixmap.scaled(tile_size, Qt.KeepAspectRatio))
                book_image_label.setAlignment(Qt.AlignCenter)
                book_image_label.index = index
                book_image_label.clicked.connect(self.show_book_details)
                book_layout.addWidget(book_image_label)
            else:
                book_title_label = ClickableLabel()
                book_title_label.setText(book["title"])
                book_title_label.setAlignment(Qt.AlignCenter)
                book_title_label.setWordWrap(True)
                book_title_label.index = index
                book_title_label.clicked.connect(self.show_book_details)
                book_layout.addWidget(book_title_label)

            book_widget.setLayout(book_layout)
            self.book_grid_layout.addWidget(book_widget, row, col)

            col += 1

        # Set fixed size for each book tile
        for i in range(self.book_grid_layout.count()):
            widget = self.book_grid_layout.itemAt(i).widget()
            widget.setFixedSize(tile_size)

        self.book_list_widget.adjustSize()

    def show_book_details(self):
        clicked_label = self.sender()
        index = clicked_label.index
        book = self.books[index]
        dialog = QDialog(self)
        dialog.setWindowTitle("Book Details")
        dialog_layout = QFormLayout()
        dialog.setLayout(dialog_layout)

        # Create the labels with a fixed width and center-aligned text
        label_width = 100
        title_label = QLabel("Title:")
        title_label.setFixedWidth(label_width)
        title_label.setAlignment(Qt.AlignCenter)
        
        author_label = QLabel("Author:")
        author_label.setFixedWidth(label_width)
        author_label.setAlignment(Qt.AlignCenter)
        
        genre_label = QLabel("Genre:")
        genre_label.setFixedWidth(label_width)
        genre_label.setAlignment(Qt.AlignCenter)
        
        stand_label = QLabel("Stand:")
        stand_label.setFixedWidth(label_width)
        stand_label.setAlignment(Qt.AlignCenter)
        
        notes_label = QLabel("Notes:")
        notes_label.setFixedWidth(label_width)
        notes_label.setAlignment(Qt.AlignCenter)

        # Add the book details with centered and uniform width labels
        dialog_layout.addRow(title_label, QLabel(book["title"]))
        dialog_layout.addRow(author_label, QLabel(book["author"]))
        dialog_layout.addRow(genre_label, QLabel(book["genre"]))
        dialog_layout.addRow(stand_label, QLabel(book["stand"]))
        dialog_layout.addRow(notes_label, QLabel(book.get("notes", "No notes")))

        if "image_path" in book and os.path.exists(book["image_path"]):
            pixmap = QPixmap(book["image_path"])
            image_label = QLabel()
            image_label.setPixmap(pixmap.scaled(300, 450, Qt.KeepAspectRatio))
            dialog_layout.addRow(QLabel("Image:"), image_label)
        else:
            dialog_layout.addRow(QLabel("Image:"), QLabel("No Image"))

        edit_button = QPushButton("Edit")
        delete_button = QPushButton("Delete")
        ok_button = QPushButton("OK")

        delete_button.setStyleSheet("background-color: red; color: white;")

        button_box = QDialogButtonBox(Qt.Horizontal)
        button_box.addButton(edit_button, QDialogButtonBox.ActionRole)
        button_box.addButton(delete_button, QDialogButtonBox.ActionRole)
        button_box.addButton(ok_button, QDialogButtonBox.AcceptRole)

        dialog_layout.addWidget(button_box)

        edit_button.clicked.connect(lambda: self.edit_book(index))
        delete_button.clicked.connect(lambda: self.delete_book(index))

        def close_dialog():
            dialog.accept()

        ok_button.clicked.connect(close_dialog)

        dialog.exec_()

    
    def edit_book(self, index):
        book = self.books[index]
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Book")
        dialog_layout = QFormLayout()
        dialog.setLayout(dialog_layout)

        # Create the input fields pre-filled with the book data
        title_edit = QLineEdit(book["title"])
        author_edit = QLineEdit(book["author"])
        genre_edit = QLineEdit(book["genre"])
        stand_edit = QComboBox()
        stand_edit.addItems(self.stands)
        stand_edit.setCurrentText(book.get("stand", ""))
        notes_edit = QTextEdit(book.get("notes", ""))
        image_edit_button = QPushButton("Change Image")

        # Create the labels with a fixed width and center-aligned text
        label_width = 100
        title_label = QLabel("Title:")
        title_label.setFixedWidth(label_width)
        title_label.setAlignment(Qt.AlignCenter)
        
        author_label = QLabel("Author:")
        author_label.setFixedWidth(label_width)
        author_label.setAlignment(Qt.AlignCenter)
        
        genre_label = QLabel("Genre:")
        genre_label.setFixedWidth(label_width)
        genre_label.setAlignment(Qt.AlignCenter)
        
        stand_label = QLabel("Stand:")
        stand_label.setFixedWidth(label_width)
        stand_label.setAlignment(Qt.AlignCenter)
        
        notes_label = QLabel("Notes:")
        notes_label.setFixedWidth(label_width)
        notes_label.setAlignment(Qt.AlignCenter)

        # Add the labels and input fields to the form layout
        dialog_layout.addRow(title_label, title_edit)
        dialog_layout.addRow(author_label, author_edit)
        dialog_layout.addRow(genre_label, genre_edit)
        dialog_layout.addRow(stand_label, stand_edit)
        dialog_layout.addRow(notes_label, notes_edit)
        dialog_layout.addRow(image_edit_button)

        def select_image():
            image_path, _ = QFileDialog.getOpenFileName(
                self, "Select Book Image", "", "Images (*.png *.jpg *.jpeg)"
            )
            if image_path:
                book["image_path"] = image_path

        image_edit_button.clicked.connect(select_image)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        dialog_layout.addWidget(button_box)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        if dialog.exec_() == QDialog.Accepted:
            book["title"] = title_edit.text()
            book["author"] = author_edit.text()
            book["genre"] = genre_edit.text()
            if stand_edit.currentText():
                book["stand"] = stand_edit.currentText()
            book["notes"] = notes_edit.toPlainText()
            self.update_book_list()
            self.save_books_to_json()

    
    def save_books_to_json(self):
        with open("library.json", "w") as f:
            json.dump(self.books, f, indent=4)

    def load_books_from_json(self):
        if os.path.exists("library.json"):
            with open("library.json", "r") as f:
                self.books = json.load(f)
            for book in self.books:
                if "image_path" not in book:
                    book["image_path"] = ""
            self.update_book_list()


class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HomeLibraryApp()
    window.show()
    sys.exit(app.exec_())
