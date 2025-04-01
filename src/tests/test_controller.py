import pytest
from unittest.mock import Mock, patch
import sys
import os

# Mock PyQt6 before importing any modules that use it
mock_qt = Mock()
sys.modules['PyQt6'] = mock_qt
sys.modules['PyQt6.QtWidgets'] = Mock()
sys.modules['PyQt6.QtCore'] = Mock()

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.controller.controller import Controller
from src.model.model import Model, Item
from src.view.view import View

@pytest.fixture
def mock_model():
    """Create a mock model with all required methods."""
    model = Mock()
    model.get_all_items.return_value = []
    return model

@pytest.fixture
def mock_view():
    """Create a mock view with all required widgets and methods."""
    view = Mock()
    view.add_button = Mock()
    view.add_button.clicked = Mock()
    view.delete_button = Mock()
    view.delete_button.clicked = Mock()
    view.update_button = Mock()
    view.update_button.clicked = Mock()
    view.item_list = Mock()
    view.item_list.currentItemChanged = Mock()
    view.name_input = Mock()
    view.description_input = Mock()
    view.populate_list = Mock()
    view.clear_inputs = Mock()
    view.show_message = Mock()
    view.get_selected_item_id = Mock()
    view.set_input_fields = Mock()
    return view

@pytest.fixture
def sample_item():
    """Create a sample item for testing."""
    return Item(name="Original Name", description="Original Description")

def test_controller_initialization(mock_model, mock_view):
    """Test that controller initializes correctly and connects signals."""
    controller = Controller(mock_model, mock_view)
    
    # Test that the controller has the correct attributes
    assert controller.model == mock_model
    assert controller.view == mock_view
    
    # Test that signals are connected
    assert mock_view.add_button.clicked.connect.called
    assert mock_view.delete_button.clicked.connect.called
    assert mock_view.update_button.clicked.connect.called
    assert mock_view.item_list.currentItemChanged.connect.called
    
    # Test that initial view update is performed
    assert mock_model.get_all_items.called
    assert mock_view.populate_list.called

def test_add_item_success(mock_model, mock_view):
    """Test adding an item successfully."""
    # Setup
    mock_view.name_input.text.return_value = "Test Item"
    mock_view.description_input.text.return_value = "Test Description"
    mock_model.create_item.return_value = Item(name="Test Item", description="Test Description")
    
    controller = Controller(mock_model, mock_view)
    
    # Execute
    controller.add_item()
    
    # Assert
    mock_model.create_item.assert_called_once_with("Test Item", "Test Description")
    mock_view.clear_inputs.assert_called_once()
    mock_view.show_message.assert_called_once_with("Success", "Item added successfully!")
    assert mock_view.populate_list.call_count == 2  # Once during init, once after adding

def test_add_item_empty_fields(mock_model, mock_view):
    """Test adding an item with empty fields."""
    # Setup
    mock_view.name_input.text.return_value = ""
    mock_view.description_input.text.return_value = ""
    
    controller = Controller(mock_model, mock_view)
    
    # Execute
    controller.add_item()
    
    # Assert
    mock_model.create_item.assert_not_called()
    mock_view.show_message.assert_called_once_with("Warning", "Please enter both name and description.")
    assert mock_view.populate_list.call_count == 1  # Only during init

def test_add_item_model_error(mock_model, mock_view):
    """Test adding an item when model raises an error."""
    # Setup
    mock_view.name_input.text.return_value = "Test Item"
    mock_view.description_input.text.return_value = "Test Description"
    mock_model.create_item.side_effect = Exception("Database error")
    
    controller = Controller(mock_model, mock_view)
    
    # Execute
    controller.add_item()
    
    # Assert
    mock_model.create_item.assert_called_once_with("Test Item", "Test Description")
    mock_view.show_message.assert_called_once_with("Error", "Failed to add item: Database error")
    assert mock_view.populate_list.call_count == 1  # Only during init

def test_delete_item_success(mock_model, mock_view):
    """Test deleting an item successfully."""
    # Setup
    mock_view.get_selected_item_id.return_value = 1
    mock_model.delete_item.return_value = True
    
    controller = Controller(mock_model, mock_view)
    
    # Execute
    controller.delete_item()
    
    # Assert
    mock_model.delete_item.assert_called_once_with(1)
    mock_view.show_message.assert_called_once_with("Success", "Item deleted successfully!")
    assert mock_view.populate_list.call_count == 2  # Once during init, once after deletion

def test_delete_item_no_selection(mock_model, mock_view):
    """Test deleting when no item is selected."""
    # Setup
    mock_view.get_selected_item_id.return_value = None
    
    controller = Controller(mock_model, mock_view)
    
    # Execute
    controller.delete_item()
    
    # Assert
    mock_model.delete_item.assert_not_called()
    mock_view.show_message.assert_called_once_with("Warning", "Please select an item to delete.")
    assert mock_view.populate_list.call_count == 1  # Only during init

def test_delete_item_model_error(mock_model, mock_view):
    """Test deleting an item when model raises an error."""
    # Setup
    mock_view.get_selected_item_id.return_value = 1
    mock_model.delete_item.side_effect = Exception("Database error")
    
    controller = Controller(mock_model, mock_view)
    
    # Execute
    controller.delete_item()
    
    # Assert
    mock_model.delete_item.assert_called_once_with(1)
    mock_view.show_message.assert_called_once_with("Error", "Failed to delete item: Database error")
    assert mock_view.populate_list.call_count == 1  # Only during init

def test_update_item_success(mock_model, mock_view, sample_item):
    """Test updating an item successfully."""
    # Setup
    mock_view.get_selected_item_id.return_value = 1
    mock_view.name_input.text.return_value = "Updated Name"
    mock_view.description_input.text.return_value = "Updated Description"
    mock_model.get_item.return_value = sample_item
    mock_model.update_item.return_value = Item(name="Updated Name", description="Updated Description")
    
    controller = Controller(mock_model, mock_view)
    
    # Execute
    controller.update_item()
    
    # Assert
    mock_model.update_item.assert_called_once_with(1, name="Updated Name", description="Updated Description")
    mock_view.clear_inputs.assert_called_once()
    mock_view.show_message.assert_called_once_with("Success", "Item updated successfully!")
    assert mock_view.populate_list.call_count == 2  # Once during init, once after update

def test_update_item_no_selection(mock_model, mock_view):
    """Test updating when no item is selected."""
    # Setup
    mock_view.get_selected_item_id.return_value = None
    
    controller = Controller(mock_model, mock_view)
    
    # Execute
    controller.update_item()
    
    # Assert
    mock_model.update_item.assert_not_called()
    mock_view.show_message.assert_called_once_with("Warning", "Please select an item to update.")
    assert mock_view.populate_list.call_count == 1  # Only during init

def test_update_item_empty_fields(mock_model, mock_view):
    """Test updating an item with empty fields."""
    # Setup
    mock_view.get_selected_item_id.return_value = 1
    mock_view.name_input.text.return_value = ""
    mock_view.description_input.text.return_value = ""
    
    controller = Controller(mock_model, mock_view)
    
    # Execute
    controller.update_item()
    
    # Assert
    mock_model.update_item.assert_not_called()
    mock_view.show_message.assert_called_once_with("Warning", "Please enter both name and description.")
    assert mock_view.populate_list.call_count == 1  # Only during init

def test_update_item_model_error(mock_model, mock_view):
    """Test updating an item when model raises an error."""
    # Setup
    mock_view.get_selected_item_id.return_value = 1
    mock_view.name_input.text.return_value = "Updated Name"
    mock_view.description_input.text.return_value = "Updated Description"
    mock_model.update_item.side_effect = Exception("Database error")
    
    controller = Controller(mock_model, mock_view)
    
    # Execute
    controller.update_item()
    
    # Assert
    mock_model.update_item.assert_called_once_with(1, name="Updated Name", description="Updated Description")
    mock_view.show_message.assert_called_once_with("Error", "Failed to update item: Database error")
    assert mock_view.populate_list.call_count == 1  # Only during init

def test_item_selection_success(mock_model, mock_view, sample_item):
    """Test selecting an item populates input fields."""
    # Setup
    mock_view.get_selected_item_id.return_value = 1
    mock_model.get_item.return_value = sample_item
    
    controller = Controller(mock_model, mock_view)
    
    # Execute
    controller.on_item_selected()
    
    # Assert
    mock_model.get_item.assert_called_once_with(1)
    mock_view.set_input_fields.assert_called_once_with(sample_item.name, sample_item.description)

def test_item_selection_none(mock_model, mock_view):
    """Test selecting nothing clears input fields."""
    # Setup
    mock_view.get_selected_item_id.return_value = None
    
    controller = Controller(mock_model, mock_view)
    
    # Execute
    controller.on_item_selected()
    
    # Assert
    mock_model.get_item.assert_not_called()
    mock_view.clear_inputs.assert_called_once()

def test_item_selection_not_found(mock_model, mock_view):
    """Test selecting a non-existent item."""
    # Setup
    mock_view.get_selected_item_id.return_value = 999
    mock_model.get_item.return_value = None
    
    controller = Controller(mock_model, mock_view)
    
    # Execute
    controller.on_item_selected()
    
    # Assert
    mock_model.get_item.assert_called_once_with(999)
    mock_view.clear_inputs.assert_called_once()
    mock_view.show_message.assert_called_once_with("Error", "Selected item not found.")
