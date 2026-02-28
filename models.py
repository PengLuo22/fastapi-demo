# models.py
from sqlalchemy import Column, Integer, String, DateTime, Text
from database import Base
from datetime import datetime

class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True, comment="主键ID")
    name = Column(String(200), nullable=False, index=True, comment="书名")
    author = Column(String(100), nullable=False, index=True, comment="作者")
    publisher = Column(String(100), nullable=True, comment="出版社")
    publish_time = Column(DateTime, nullable=True, comment="出版时间")
    isbn = Column(String(20), unique=True, nullable=True, comment="ISBN编号")
    description = Column(Text, nullable=True, comment="书籍描述")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    def __repr__(self):
        return f"<Book {self.name} by {self.author}>"