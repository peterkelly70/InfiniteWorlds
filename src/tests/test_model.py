import pytest
import os
import sys

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.model.model import Model, Item

@pytest.fixture
def setup_model():
    """Fixture to set up an in-memory database for each test."""
    test_db_path = ':memory:'
    model = Model(db_path=test_db_path)
    yield model
    # Teardown is implicit as the in-memory DB disappears

@pytest.fixture
def sample_item(setup_model):
    """Fixture to create a sample item for testing."""
    return setup_model.create_item("Sample Item", "Sample Description")

def test_create_item(setup_model):
    """Test creating a new item."""
    model = setup_model
    name = "Test Item"
    description = "A test description"
    new_item = model.create_item(name, description)

    assert new_item.id is not None
    assert new_item.name == name
    assert new_item.description == description

    # Verify it was actually added to the DB
    retrieved_item = model._session.query(Item).filter(Item.id == new_item.id).first()
    assert retrieved_item is not None
    assert retrieved_item.name == name

def test_get_item(setup_model, sample_item):
    """Test retrieving an item by ID."""
    model = setup_model
    retrieved_item = model.get_item(sample_item.id)
    
    assert retrieved_item is not None
    assert retrieved_item.id == sample_item.id
    assert retrieved_item.name == "Sample Item"
    assert retrieved_item.description == "Sample Description"

def test_get_nonexistent_item(setup_model):
    """Test retrieving a non-existent item."""
    model = setup_model
    retrieved_item = model.get_item(999)  # Non-existent ID
    assert retrieved_item is None

def test_update_item(setup_model, sample_item):
    """Test updating an item."""
    model = setup_model
    updated_name = "Updated Item"
    updated_description = "Updated Description"
    
    updated_item = model.update_item(
        sample_item.id,
        name=updated_name,
        description=updated_description
    )
    
    assert updated_item is not None
    assert updated_item.name == updated_name
    assert updated_item.description == updated_description
    
    # Verify changes were persisted
    retrieved_item = model.get_item(sample_item.id)
    assert retrieved_item.name == updated_name
    assert retrieved_item.description == updated_description

def test_update_nonexistent_item(setup_model):
    """Test updating a non-existent item."""
    model = setup_model
    updated_item = model.update_item(999, name="New Name")  # Non-existent ID
    assert updated_item is None

def test_delete_item(setup_model, sample_item):
    """Test deleting an item."""
    model = setup_model
    
    # Verify item exists before deletion
    assert model.get_item(sample_item.id) is not None
    
    # Delete the item
    result = model.delete_item(sample_item.id)
    assert result is True
    
    # Verify item no longer exists
    assert model.get_item(sample_item.id) is None

def test_delete_nonexistent_item(setup_model):
    """Test deleting a non-existent item."""
    model = setup_model
    result = model.delete_item(999)  # Non-existent ID
    assert result is False

def test_get_all_items(setup_model):
    """Test retrieving all items."""
    model = setup_model
    
    # Create multiple items
    items = [
        model.create_item(f"Item {i}", f"Description {i}")
        for i in range(3)
    ]
    
    # Retrieve all items
    all_items = model.get_all_items()
    
    assert len(all_items) == 3
    assert all(isinstance(item, Item) for item in all_items)
    
    # Verify items are in the list
    item_ids = {item.id for item in all_items}
    assert all(item.id in item_ids for item in items)

def test_get_all_items_empty(setup_model):
    """Test retrieving all items when database is empty."""
    model = setup_model
    all_items = model.get_all_items()
    assert len(all_items) == 0
    assert isinstance(all_items, list)
