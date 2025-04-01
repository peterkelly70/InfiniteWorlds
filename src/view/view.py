from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
                             QListWidget, QPushButton, QMessageBox, QListWidgetItem)
from PyQt6.QtCore import Qt
import sys

class View(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        """Initialize the user interface."""
        # Create main layout
        main_layout = QVBoxLayout()
        
        # Create input fields
        input_layout = QVBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter name")
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Enter description")
        input_layout.addWidget(self.name_input)
        input_layout.addWidget(self.description_input)
        
        # Create buttons
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add")
        self.update_button = QPushButton("Update")
        self.delete_button = QPushButton("Delete")
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)
        
        # Create list widget
        self.item_list = QListWidget()
        
        # Add all layouts and widgets to main layout
        main_layout.addLayout(input_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.item_list)
        
        # Set the main layout
        self.setLayout(main_layout)
        
        # Set window properties
        self.setWindowTitle("Item Manager")
        self.setGeometry(100, 100, 400, 500)

    def populate_list(self, items):
        """Populate the list widget with items."""
        self.item_list.clear()
        for item in items:
            list_item = QListWidgetItem(item.name)
            list_item.setData(0, item.id)  # Store item ID in data role 0
            self.item_list.addItem(list_item)

    def get_selected_item_id(self):
        """Get the ID of the currently selected item."""
        current_item = self.item_list.currentItem()
        if current_item:
            return current_item.data(0)  # Get item ID from data role 0
        return None

    def set_input_fields(self, name, description):
        """Set the values of input fields."""
        self.name_input.setText(name)
        self.description_input.setText(description)

    def clear_inputs(self):
        """Clear all input fields."""
        self.name_input.clear()
        self.description_input.clear()

    def show_message(self, title, message):
        """Show a message box with the given title and message."""
        QMessageBox.information(self, title, message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = View()
    view.show()
    sys.exit(app.exec())
