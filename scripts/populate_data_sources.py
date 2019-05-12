import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from hatchet.db.meta_models import DataSource


DB_URI = f"sqlite:///{os.getcwd()}/data.sqlite"
con = create_engine(DB_URI)
Session = sessionmaker(bind=con)


SOURCES = [
    DataSource(name="Wikipedia", url="http://en.wikipedia.org"),
    DataSource(name="ESPN", url="http://www.espn.com"),
    DataSource(name="Sports Reference", url="http://www.sports-reference.com/cfb/")
]

def main():
    session = Session()
    for source in SOURCES:
        session.add(source)
    session.commit()
    session.close()


if __name__ == "__main__":
    main()
