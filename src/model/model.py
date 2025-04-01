from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    def __repr__(self):
        return f"<Item(name='{self.name}', description='{self.description}')>"


class Model:
    def __init__(self, db_path=':memory:'):
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        self._session_maker = sessionmaker(bind=self.engine)
        self._session = self._session_maker()

    def create_item(self, name, description):
        new_item = Item(name=name, description=description)
        self._session.add(new_item)
        self._session.commit()
        return new_item

    def get_item(self, item_id):
        return self._session.query(Item).filter(Item.id == item_id).first()

    def update_item(self, item_id, name=None, description=None):
        item = self.get_item(item_id)
        if item:
            if name:
                item.name = name
            if description:
                item.description = description
            self._session.commit()
            return item
        return None

    def delete_item(self, item_id):
        item = self.get_item(item_id)
        if item:
            self._session.delete(item)
            self._session.commit()
            return True
        return False

    def get_all_items(self):
        return self._session.query(Item).all()

if __name__ == '__main__':
    model = Model('test.db')

    # Create
    item1 = model.create_item('First Item', 'This is the first item')
    print('Created:', item1)

    # Read
    retrieved_item = model.get_item(item1.id)
    print('Retrieved:', retrieved_item)

    # Update
    updated_item = model.update_item(item1.id, name='Updated Item')
    print('Updated:', updated_item)

    # Read All
    all_items = model.get_all_items()
    print('All Items:', all_items)

    # Delete
    model.delete_item(item1.id)
    print('Deleted item')
