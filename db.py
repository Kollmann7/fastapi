from sqlmodel import create_engine, SQLModel, Session

DATABASE_URL = "sqlite:///db.sqlite"
engine = create_engine(DATABASE_URL, echo = True)


def get_session():
    with Session(engine) as session:
        yield session
