from Database import basicDatabase, dataItem
from faker import Faker

import os

# Create DB Dir
cwd = os.path.curdir
db_dir_path = os.path.join(cwd, "db_dir_adiel")
db_path = os.path.join(db_dir_path, "db.JSON")

db = basicDatabase(db_path)
fake = Faker('en_US')
fake_json = {'name': fake.name(), 'address': fake.address()}
fake_data_item = dataItem(fake_json)

# check ids are working, and get is working
db.insert_to_or_update_db(fake_data_item.get_item_id(), fake_data_item.get_item())
print((db.get_from_db(fake_data_item.get_item_id())))

# check deletion is working 
db.delete_from_db(fake_data_item.get_item_id())
print((db.get_from_db(fake_data_item.get_item_id())))
