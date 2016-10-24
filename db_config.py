from setoran_models import db 


def setoran_beneran():
    db.bind("sqlite", "setoran.sqlite", create_db=True)
    db.generate_mapping(create_tables=True)
    return db


def testing_binding():
    db.bind("sqlite", "testing.sqlite", create_db=True)
    db.generate_mapping(create_tables=True)
    return db
