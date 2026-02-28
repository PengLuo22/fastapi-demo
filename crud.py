# crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.engine import Result
from typing import Optional, List
from models import Book
from schemas import BookCreate, BookUpdate


class BookCRUD:
    @staticmethod
    async def create_book(db: AsyncSession, book: BookCreate) -> Book:
        """
        创建新书籍
        """
        db_book = Book(**book.model_dump())
        db.add(db_book)
        await db.commit()
        await db.refresh(db_book)
        return db_book

    @staticmethod
    async def get_book(db: AsyncSession, book_id: int) -> Optional[Book]:
        """
        根据ID获取单本书籍
        """
        return await db.get(Book, book_id)

    @staticmethod
    async def get_books_paginated(
            db: AsyncSession,
            page: int = 1,
            page_size: int = 10,
            author: Optional[str] = None,
            keyword: Optional[str] = None
    ) -> tuple[List[Book], int]:
        """
        分页查询书籍列表，支持按作者和关键字搜索
        """
        # 构建基础查询
        query = select(Book)

        # 添加过滤条件
        if author:
            query = query.where(Book.author == author)
        if keyword:
            query = query.where(
                (Book.name.contains(keyword)) |
                (Book.description.contains(keyword))
            )

        # 获取总数
        count_query = select(func.count()).select_from(query.subquery())
        total = await db.scalar(count_query)

        # 分页
        query = query.order_by(Book.created_at.desc())
        query = query.offset((page - 1) * page_size).limit(page_size)

        result: Result = await db.execute(query)
        books = result.scalars().all()

        return books, total or 0

    @staticmethod
    async def update_book(
            db: AsyncSession,
            book_id: int,
            book_update: BookUpdate
    ) -> Optional[Book]:
        """
        更新书籍信息
        """
        db_book = await BookCRUD.get_book(db, book_id)
        if db_book:
            update_data = book_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_book, field, value)
            await db.commit()
            await db.refresh(db_book)
        return db_book

    @staticmethod
    async def delete_book(db: AsyncSession, book_id: int) -> bool:
        """
        删除书籍
        """
        db_book = await BookCRUD.get_book(db, book_id)
        if db_book:
            await db.delete(db_book)
            await db.commit()
            return True
        return False

    @staticmethod
    async def book_exists(db: AsyncSession, isbn: str) -> bool:
        """
        检查ISBN是否已存在
        """
        result = await db.execute(select(Book).where(Book.isbn == isbn))
        return result.scalar_one_or_none() is not None