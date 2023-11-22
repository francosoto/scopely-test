import structlog
from app.config import DB_HOST, DB_USERNAME, DB_PASSWORD, DB_DATABASE
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, DataError
from sqlalchemy.orm import sessionmaker


# Yield dependency
def get_db():
    """
    This function ensures that we close the DB session after we finish our work
    See:
    https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/
    """
    db = DbConnector()
    try:
        yield db
    finally:
        db.close()


logger = structlog.get_logger(logger_name=__name__)


class DBException(Exception):
    def __init__(self, message="Some database error has been happened"):
        self.message = message
        super().__init__(self.message)


class DataIntegrityException(Exception):
    def __init__(self, message="Some data integrity error has been happened"):
        self.message = message
        super().__init__(self.message)


class DataException(Exception):
    def __init__(self, message="Some data error has been happened"):
        self.message = message
        super().__init__(self.message)


class DbConnector:
    def __init__(self):
        self._sess = self.connect()
        self.session = self._sess()

    @property
    def connection(self):
        return self._sess

    def connect(self):
        """Connect to the database server"""
        engine = create_engine(
            "mysql+pymysql://{}:{}@{}/{}".format(
                DB_USERNAME, DB_PASSWORD, DB_HOST, DB_DATABASE
            ),
            echo=False,
        )
        return sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def __exit__(self):
        self.close()

    def commit(self):
        self.session.commit()

    def close(self):
        self.session.close()

    def add(self, obj=None):
        try:
            self.session.add(obj)
            self.commit()
            self.session.refresh(obj)
            return obj
        except IntegrityError as e:
            logger.error("Data Integrity error", error=str(e))
            raise DataIntegrityException(str(e))
        except DataError as e:
            logger.error("Data error", error=str(e))
            raise DataException(str(e))
        except SQLAlchemyError as e:
            logger.error("Database error", error=str(e))
            raise DBException(str(e))

    def refresh(self, obj=None):
        self._sess.refresh(obj)

    def fetch_one_by_id(self, where, by):
        try:
            return self.session.query(where).filter(where.id == by).first()
        except SQLAlchemyError as e:
            logger.error("Database error", error=str(e))
            raise DBException(str(e))
