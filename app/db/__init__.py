from app.db.database import Base
from app.db.database import engine
from app.db.models.user_model import User
from app.db.models.log_model import Log


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
