from app.models.task import *
from app.beckend.db import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    age = Column(Integer)
    slug = Column(String, unique=True, index=True)
    tasks = relationship("Task", back_populates="user",cascade="save-update, merge, delete")



# from sqlalchemy.schema import CreateTable
#
# print(CreateTable(Task.__table__))
