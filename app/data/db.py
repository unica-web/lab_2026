from sqlmodel import create_engine, SQLModel, Session


sqlite_file_name = "/home/asotgiu/lab_2026/app/data/database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(
    sqlite_url,
    connect_args={"check_same_thread": False},
    echo=True
)

def init_database():
    SQLModel.metadata.create_all(engine)
