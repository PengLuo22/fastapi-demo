# schemas.py
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime


# 基础Book Schema
class BookBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="书名")
    author: str = Field(..., min_length=1, max_length=100, description="作者")
    publisher: Optional[str] = Field(None, max_length=100, description="出版社")
    publish_time: Optional[datetime] = Field(None, description="出版时间")
    isbn: Optional[str] = Field(None, max_length=20, description="ISBN编号")
    description: Optional[str] = Field(None, description="书籍描述")


# 创建书籍时的请求模型
class BookCreate(BookBase):
    pass


# 更新书籍时的请求模型
class BookUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    publisher: Optional[str] = None
    publish_time: Optional[datetime] = None
    isbn: Optional[str] = None
    description: Optional[str] = None


# 书籍响应模型
class BookResponse(BookBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# 分页查询响应模型
class PaginatedBookResponse(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    items: List[BookResponse]