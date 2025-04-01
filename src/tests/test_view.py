import pytest
from unittest.mock import Mock, patch, call
import sys
import os

# Mock PyQt6 before importing any modules that use it
mock_qt = Mock()
sys.modules['PyQt6'] = mock_qt
sys.modules['PyQt6.QtWidgets'] = Mock()
sys.modules['PyQt6.QtCore'] = Mock()

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.view.view import View
from src.model.model import Item

@pytest.fixture
def view():
    """Create a View instance with all Qt widgets mocked."""
    # Create mock instances
    name_input = Mock()
    name_input.setPlaceholderText = Mock()
    name_input.setText = Mock()
    name_input.clear = Mock()
    
    desc_input = Mock()
    desc_input.setPlaceholderText = Mock()
    desc_input.setText = Mock()
    desc_input.clear = Mock()
    
    item_list = Mock()
    item_list.clear = Mock()
    item_list.addItem = Mock()
    item_list.currentItem = Mock()
    
    add_button = Mock()
    add_button.setText = Mock()
    update_button = Mock()
    update_button.setText = Mock()
    delete_button = Mock()
    delete_button.setText = Mock()

    # Configure mock QLineEdit
    mock_line = Mock()
    mock_line.return_value = name_input
    mock_line.side_effect = [name_input, desc_input]

    # Configure mock QListWidget
    mock_list = Mock()
    mock_list.return_value = item_list

    # Configure mock QPushButton
    mock_button = Mock()
    mock_button.side_effect = [add_button, update_button, delete_button]

    with patch('PyQt6.QtWidgets.QWidget'), \
         patch('PyQt6.QtWidgets.QVBoxLayout'), \
         patch('PyQt6.QtWidgets.QHBoxLayout'), \
         patch('PyQt6.QtWidgets.QLineEdit', mock_line), \
         patch('PyQt6.QtWidgets.QListWidget', mock_list), \
         patch('PyQt6.QtWidgets.QPushButton', mock_button):

        # Create view instance
        view = View()

        # Set mock attributes
        view.name_input = name_input
        view.description_input = desc_input
        view.item_list = item_list
        view.add_button = add_button
        view.update_button = update_button
        view.delete_button = delete_button

        # Configure mock behaviors
        name_input.setPlaceholderText("Enter name")
        desc_input.setPlaceholderText("Enter description")
        add_button.setText("Add")
        update_button.setText("Update")
        delete_button.setText("Delete")

        return view

def test_view_initialization(view):
    """Test that view initializes with all required widgets and layouts."""
    # Test that all required widgets exist
    assert hasattr(view, 'name_input')
    assert hasattr(view, 'description_input')
    assert hasattr(view, 'item_list')
    assert hasattr(view, 'add_button')
    assert hasattr(view, 'update_button')
    assert hasattr(view, 'delete_button')

    # Test that widgets have correct properties
    assert view.name_input.setPlaceholderText.call_args == call("Enter name")
    assert view.description_input.setPlaceholderText.call_args == call("Enter description")
    assert view.add_button.setText.call_args == call("Add")
    assert view.update_button.setText.call_args == call("Update")
    assert view.delete_button.setText.call_args == call("Delete")

def test_populate_list(view):
    """Test populating the list widget with items."""
    # Create test items
    items = [
        Item(id=1, name="Item 1", description="Description 1"),
        Item(id=2, name="Item 2", description="Description 2")
    ]
    
    # Create mock list items
    mock_items = [Mock(), Mock()]
    with patch('PyQt6.QtWidgets.QListWidgetItem', side_effect=mock_items):
        # Call populate_list
        view.populate_list(items)
    
    # Assert list was cleared first
    assert view.item_list.clear.called
    
    # Verify each item was set up correctly
    expected_calls = [
        (call("Item 1"), call(0, 1)),  # setText, setData for first item
        (call("Item 2"), call(0, 2))   # setText, setData for second item
    ]
    
    for i, (text_call, data_call) in enumerate(expected_calls):
        assert mock_items[i].setText.call_args == text_call
        assert mock_items[i].setData.call_args == data_call
    
    # Assert items were added to list
    assert view.item_list.addItem.call_count == 2

def test_get_selected_item_id_with_selection(view):
    """Test getting selected item ID when an item is selected."""
    # Create mock selected item
    mock_item = Mock()
    mock_item.data.return_value = 1
    view.item_list.currentItem.return_value = mock_item
    
    # Get selected item ID
    item_id = view.get_selected_item_id()
    
    # Assert correct ID was returned
    assert item_id == 1
    assert mock_item.data.call_args == call(0)  # 0 is the role

def test_get_selected_item_id_no_selection(view):
    """Test getting selected item ID when no item is selected."""
    # Mock no selection
    view.item_list.currentItem.return_value = None
    
    # Get selected item ID
    item_id = view.get_selected_item_id()
    
    # Assert None was returned
    assert item_id is None

def test_set_input_fields(view):
    """Test setting input field values."""
    # Set input fields
    view.set_input_fields("Test Name", "Test Description")
    
    # Assert text was set correctly
    assert view.name_input.setText.call_args == call("Test Name")
    assert view.description_input.setText.call_args == call("Test Description")

def test_clear_inputs(view):
    """Test clearing input fields."""
    # Clear inputs
    view.clear_inputs()
    
    # Assert text was cleared
    assert view.name_input.clear.called
    assert view.description_input.clear.called

def test_show_message(view):
    """Test showing message box."""
    # Show message
    with patch('PyQt6.QtWidgets.QMessageBox') as mock_msgbox:
        view.show_message("Test Title", "Test Message")
        
        # Assert message box was shown with correct parameters
        assert mock_msgbox.information.call_args == call(
            view,
            "Test Title",
            "Test Message"
        )
