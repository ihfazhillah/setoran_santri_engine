from setoran_models import db 

db.bind("sqlite", "setoran.sqlite", create_db=True)
db.generate_mapping(create_tables=True)
