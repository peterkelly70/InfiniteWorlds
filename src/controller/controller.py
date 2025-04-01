import sys
from PyQt6.QtWidgets import QApplication

# Adjust import paths based on project structure
sys.path.append('/home/peter/Projects/infiniteWorlds/src')
from src.model.model import Model
from src.view.view import View

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self._connect_signals()
        self._update_view()

    def _connect_signals(self):
        self.view.add_button.clicked.connect(self.add_item)
        self.view.delete_button.clicked.connect(self.delete_item)
        self.view.update_button.clicked.connect(self.update_item)
        self.view.item_list.currentItemChanged.connect(self.on_item_selected)

    def _update_view(self):
        items = self.model.get_all_items()
        self.view.populate_list(items)

    def add_item(self):
        name = self.view.name_input.text()
        description = self.view.description_input.text()

        if name and description:
            try:
                self.model.create_item(name, description)
                self.view.clear_inputs()
                self._update_view()
                self.view.show_message("Success", "Item added successfully!")
            except Exception as e:
                self.view.show_message("Error", f"Failed to add item: {e}")
        else:
            self.view.show_message("Warning", "Please enter both name and description.")

    def delete_item(self):
        item_id = self.view.get_selected_item_id()
        
        if item_id is None:
            self.view.show_message("Warning", "Please select an item to delete.")
            return
            
        try:
            if self.model.delete_item(item_id):
                self._update_view()
                self.view.show_message("Success", "Item deleted successfully!")
            else:
                self.view.show_message("Error", "Item not found.")
        except Exception as e:
            self.view.show_message("Error", f"Failed to delete item: {e}")

    def update_item(self):
        item_id = self.view.get_selected_item_id()
        
        if item_id is None:
            self.view.show_message("Warning", "Please select an item to update.")
            return
            
        name = self.view.name_input.text()
        description = self.view.description_input.text()
        
        if not name or not description:
            self.view.show_message("Warning", "Please enter both name and description.")
            return
            
        try:
            updated_item = self.model.update_item(item_id, name=name, description=description)
            if updated_item:
                self.view.clear_inputs()
                self._update_view()
                self.view.show_message("Success", "Item updated successfully!")
            else:
                self.view.show_message("Error", "Item not found.")
        except Exception as e:
            self.view.show_message("Error", f"Failed to update item: {e}")

    def on_item_selected(self):
        """Handle item selection in the list."""
        item_id = self.view.get_selected_item_id()
        
        if item_id is None:
            self.view.clear_inputs()
            return
            
        try:
            item = self.model.get_item(item_id)
            if item:
                self.view.set_input_fields(item.name, item.description)
            else:
                self.view.clear_inputs()
                self.view.show_message("Error", "Selected item not found.")
        except Exception as e:
            self.view.clear_inputs()
            self.view.show_message("Error", f"Failed to get item: {e}")

# Main execution block (optional, for testing the controller)
if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Initialize Model and View
    db_path = '/home/peter/Projects/infiniteWorlds/data.db' # Or use in-memory: ':memory:'
    model = Model(db_path)
    view = View()

    # Initialize Controller
    controller = Controller(model, view)

    # Show the View
    view.show()

    sys.exit(app.exec())
