from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

engine = create_engine('sqlite://', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from .models import Appointment
    Base.metadata.create_all(bind=engine)
    db_session.bulk_save_objects([
        Appointment(
            description="New Year's Day",
            date=datetime(2018, 1, 1).date(),
            time=datetime(1, 1, 1, 12, 0).time()
        ),
        Appointment(
            description="Interview",
            date=datetime(2018, 2, 19).date(),
            time=datetime(1, 1, 1, 16, 45).time()
        )
    ])
    db_session.commit()
