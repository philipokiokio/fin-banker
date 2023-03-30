from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

# application import config.
from src.app.config import db_settings

# DB URL for connection
SQLALCHEMY_DATABASE_URL = f"postgresql://{db_settings.username}:{db_settings.password}@{db_settings.hostname}:{db_settings.port}/{db_settings.name}"

# Creating DB engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Creating and Managing session.
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionLocal = scoped_session(SessionFactory)

# Domain Modelling Dependency
Base = declarative_base()


print("Database is Ready!")


TEST_SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL + "_test"
test_engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL)
TestFactory = sessionmaker(autoflush=False, autocommit=False, bind=test_engine)
TestSessionLocal = scoped_session(TestFactory)


def get_test_db():
    print("Test Database is Ready!")
    test_db = TestSessionLocal()

    try:
        yield test_db
    finally:
        test_db.close()
    TestSessionLocal.remove()
