# main.py
from fastapi import FastAPI, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import math

from database import async_engine, Base
from models import Book
from schemas import BookCreate, BookResponse, PaginatedBookResponse, BookUpdate
from crud import BookCRUD
from dependencies import get_db

# 创建FastAPI应用
app = FastAPI(
    title="书籍管理API",
    description="使用FastAPI + SQLAlchemy + aiomysql的异步书籍管理API",
    version="1.0.0"
)


# 启动事件：创建数据库表
@app.on_event("startup")
async def startup():
    """
    应用启动时创建数据库表
    """
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ 数据库表创建成功！")
    except Exception as e:
        print(f"⚠️  数据库连接失败: {e}")
        print("📝 请确保 MySQL 服务已启动，或者检查 .env 文件中的数据库配置")


# 关闭事件：关闭数据库连接
@app.on_event("shutdown")
async def shutdown():
    """
    应用关闭时清理数据库连接
    """
    await async_engine.dispose()
    print("👋 数据库连接已关闭")


# 书籍API路由
@app.post(
    "/book/",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
    summary="创建新书籍",
    description="添加一本新书到数据库"
)
async def create_book(
        book: BookCreate,
        db: AsyncSession = Depends(get_db)
):
    """
    创建新书籍：
    - **name**: 书名（必填）
    - **author**: 作者（必填）
    - **publisher**: 出版社（可选）
    - **publish_time**: 出版时间（可选）
    - **isbn**: ISBN编号（可选）
    - **description**: 书籍描述（可选）
    """
    # 检查ISBN是否已存在（如果提供了ISBN）
    if book.isbn:
        exists = await BookCRUD.book_exists(db, book.isbn)
        if exists:
            raise HTTPException(
                status_code=400,
                detail=f"ISBN '{book.isbn}' 已存在"
            )

    try:
        created_book = await BookCRUD.create_book(db, book)
        return created_book
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"创建书籍失败: {str(e)}"
        )


@app.get(
    "/book/",
    response_model=PaginatedBookResponse,
    summary="分页查询书籍",
    description="支持分页、按作者筛选、关键字搜索"
)
async def get_books(
        page: int = Query(1, ge=1, description="页码，从1开始"),
        page_size: int = Query(10, ge=1, le=100, description="每页数量"),
        author: Optional[str] = Query(None, description="按作者筛选"),
        keyword: Optional[str] = Query(None, description="搜索关键字（书名或描述）"),
        db: AsyncSession = Depends(get_db)
):
    """
    分页查询书籍列表：
    - **page**: 页码，默认1
    - **page_size**: 每页数量，默认10，最大100
    - **author**: 按作者筛选（可选）
    - **keyword**: 搜索关键字（可选，匹配书名或描述）
    """
    books, total = await BookCRUD.get_books_paginated(
        db,
        page=page,
        page_size=page_size,
        author=author,
        keyword=keyword
    )

    total_pages = math.ceil(total / page_size) if total > 0 else 0

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "items": books
    }


@app.get(
    "/book/{book_id}",
    response_model=BookResponse,
    summary="获取单本书籍",
    description="根据ID获取书籍详情"
)
async def get_book(
        book_id: int,
        db: AsyncSession = Depends(get_db)
):
    """
    根据书籍ID获取详情
    """
    book = await BookCRUD.get_book(db, book_id)
    if not book:
        raise HTTPException(
            status_code=404,
            detail=f"ID为 {book_id} 的书籍不存在"
        )
    return book


@app.put(
    "/book/{book_id}",
    response_model=BookResponse,
    summary="更新书籍",
    description="更新书籍信息"
)
async def update_book(
        book_id: int,
        book_update: BookUpdate,
        db: AsyncSession = Depends(get_db)
):
    """
    更新书籍信息：
    - 只更新提供的字段
    """
    updated_book = await BookCRUD.update_book(db, book_id, book_update)
    if not updated_book:
        raise HTTPException(
            status_code=404,
            detail=f"ID为 {book_id} 的书籍不存在"
        )
    return updated_book


@app.delete(
    "/book/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="删除书籍",
    description="根据ID删除书籍"
)
async def delete_book(
        book_id: int,
        db: AsyncSession = Depends(get_db)
):
    """
    删除指定ID的书籍
    """
    deleted = await BookCRUD.delete_book(db, book_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"ID为 {book_id} 的书籍不存在"
        )
    return None


# 健康检查接口
@app.get("/health", summary="健康检查")
async def health_check():
    """
    检查服务状态
    """
    return {
        "status": "healthy",
        "service": "running"
    }


# 添加一些测试数据（可选）
@app.post("/book/init/test-data", status_code=status.HTTP_201_CREATED)
async def init_test_data(db: AsyncSession = Depends(get_db)):
    """
    初始化测试数据（仅用于开发测试）
    """
    from datetime import datetime

    test_books = [
        BookCreate(
            name="三体",
            author="刘慈欣",
            publisher="重庆出版社",
            publish_time=datetime(2008, 1, 1),
            isbn="9787536692930",
            description="地球文明与三体文明的第一次接触"
        ),
        BookCreate(
            name="活着",
            author="余华",
            publisher="作家出版社",
            publish_time=datetime(2012, 8, 1),
            isbn="9787506365437",
            description="讲述了福贵一生的悲欢离合"
        ),
        BookCreate(
            name="百年孤独",
            author="加西亚·马尔克斯",
            publisher="南海出版公司",
            publish_time=datetime(2011, 6, 1),
            isbn="9787544253994",
            description="魔幻现实主义代表作"
        )
    ]

    created_books = []
    for book in test_books:
        # 检查ISBN是否已存在
        if book.isbn:
            exists = await BookCRUD.book_exists(db, book.isbn)
            if not exists:
                created = await BookCRUD.create_book(db, book)
                created_books.append(created)

    return {
        "message": f"成功创建 {len(created_books)} 本测试数据",
        "books": created_books
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)


