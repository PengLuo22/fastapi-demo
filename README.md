# FastAPI 书籍管理 API

> 一个适合 Python 新手学习的 FastAPI 项目，实现完整的书籍 CRUD（增删改查）功能

## 项目简介

这是一个使用 FastAPI 框架构建的 RESTful API，用于管理书籍信息。项目采用了现代化的异步编程方式，代码结构清晰，非常适合学习 FastAPI 和 SQLAlchemy。

## 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| FastAPI | 最新 | Web 框架，提供高性能的 API |
| SQLAlchemy | 2.0+ | ORM（对象关系映射）工具 |
| aiomysql | 最新 | 异步 MySQL 驱动 |
 Pydantic | 最新 | 数据验证 |
| MySQL | 8.0 | 数据库 |
| Docker | - | 容器化部署 MySQL |

## 项目结构

```
fastapi-demo/
├── main.py           # 主应用文件 - 定义所有 API 路由
├── models.py         # 数据库模型 - 定义数据表结构
├── schemas.py        # 数据验证模型 - 定义请求/响应数据格式
├── database.py       # 数据库配置 - 连接池管理
├── crud.py           # 数据库操作 - 封装增删改查逻辑
├── dependencies.py   # 依赖注入 - 数据库会话管理
├── docker-compose.yml # Docker 配置 - 启动 MySQL 容器
├── init.sql          # 数据库初始化脚本
├── .env              # 环境变量配置（需自行创建）
├── .env.example      # 环境变量示例
└── README.md         # 项目说明文档
```

---

## 给有经验开发者的快速通道

> 如果你是 Java/Go/Node.js 等语言的开发者，或者已经有 Web 开发经验，可以参考以下内容节省时间。

### 可以快速浏览或跳过的部分

| 章节 | 是否可跳过 | 说明 |
|------|-----------|------|
| 文件详解（新手必读） | ⏩ 可快速浏览 | 如果你熟悉 ORM、分层架构，直接看代码即可 |
| 核心概念解释 | ⏩ 大部分可跳过 | ORM、依赖注入都是通用概念 |
| 什么是异步编程 | ⏭️ 可跳过 | 如果你了解 async/await 或协程 |
| 安装步骤（虚拟环境） | ⏭️ 可跳过 | 直接看依赖安装部分即可 |
| 使用示例（curl 命令） | ⏭️ 可跳过 | 直接看 Swagger UI 更方便 |

### 建议重点关注的 Python/FastAPI 特性

| 特性 | 类比说明 | 代码位置 |
|------|---------|---------|
| **Pydantic** | 类似 Java 的 Validation Annotation + Lombok | `schemas.py` |
| **依赖注入** | 类似 Spring 的 @Autowired | `dependencies.py`, `main.py` |
| **异步 ORM** | 类似 Spring WebFlux + R2DBC | `crud.py`, `database.py` |
| **路由装饰器** | 类似 @GetMapping/@PostMapping | `main.py:47+` |
| **async/await** | 类似 JS/C# 的 async/await | 所有 async 函数 |

### FastAPI vs 其他框架速览

```python
# FastAPI 路由定义
@app.get("/book/{book_id}")
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    return await BookCRUD.get_book(db, book_id)

# 相当于 Java Spring Boot
@GetMapping("/book/{book_id}")
public Book getBook(@PathVariable int book_id, @Autowired DbService db) {
    return bookService.getBook(bookId);
}
```

### 快速启动（3 步）

```bash
# 1. 安装依赖
pip install fastapi uvicorn sqlalchemy aiomysql python-dotenv pydantic

# 2. 启动数据库
docker-compose up -d

# 3. 运行应用
uvicorn main:app --reload
```

然后访问 http://localhost:8000/docs 查看 API 文档，即可开始测试。

### 项目架构（一句话）

**经典三层架构**：Controller (`main.py`) → Service/DAO (`crud.py`) → Model (`models.py`)

### Python 新语法速查（针对 Java 开发者）

| Python | Java |
|--------|------|
| `async def` | `public CompletableFuture` |
| `await` | `.get()` 或 `.join()` |
| `from x import y` | `import x.y;` |
| `x: int`（类型注解） | `int x` |
| `List[Book]` | `List<Book>` |
| `Optional[str]` | `String` 或 `@Nullable` |

---

## 文件详解（新手必读）

### 1. models.py - 数据库模型
**作用**：定义数据库表的结构

```python
class Book(Base):
    __tablename__ = "book"  # 对应数据库中的表名

    id = Column(Integer, primary_key=True)  # 主键
    name = Column(String(200), nullable=False)  # 书名，必填
    author = Column(String(100), nullable=False)  # 作者，必填
    # ... 更多字段
```

**新手提示**：把这个文件想象成数据库表的"设计图"，它告诉 Python 程序数据库长什么样。

### 2. schemas.py - 数据验证模型
**作用**：定义 API 接口接收和返回的数据格式

- `BookCreate`：创建书籍时需要的数据
- `BookUpdate`：更新书籍时可以传的数据
- `BookResponse`：返回给客户端的数据格式
- `PaginatedBookResponse`：分页查询的响应格式

**新手提示**：Pydantic 会自动验证数据，比如检查书名不能为空、长度不能超过200等。

### 3. database.py - 数据库连接
**作用**：管理与数据库的连接

- 从 `.env` 文件读取数据库配置
- 创建异步数据库引擎
- 创建会话工厂

**新手提示**：就像拨号上网，这个文件负责建立和维护与数据库的连接。

### 4. crud.py - 数据库操作
**作用**：封装所有的数据库操作（增删改查）

- `create_book()` - 创建书籍
- `get_book()` - 获取单本书籍
- `get_books_paginated()` - 分页查询书籍列表
- `update_book()` - 更新书籍
- `delete_book()` - 删除书籍

**新手提示**：CRUD = Create（创建）、Read（读取）、Update（更新）、Delete（删除）

### 5. dependencies.py - 依赖注入
**作用**：为每个请求提供数据库会话

```python
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session  # 将数据库会话传递给需要的路由
```

**新手提示**：依赖注入是 FastAPI 的核心概念，可以理解为"自动提供需要的工具"。

### 6. main.py - 主应用
**作用**：定义所有的 API 路由和业务逻辑

```python
@app.post("/book/")  # POST 请求，创建书籍
@app.get("/book/")   # GET 请求，查询书籍列表
@app.get("/book/{id}")  # GET 请求，获取单本书籍
@app.put("/book/{id}")  # PUT 请求，更新书籍
@app.delete("/book/{id}")  # DELETE 请求，删除书籍
```

## 快速开始

### 前置要求

- Python 3.8+
- MySQL 8.0+（或使用 Docker）
- pip（Python 包管理工具）

### 安装步骤

#### 1. 克隆项目（如果从 Git 仓库）

```bash
git clone <你的仓库地址>
cd fastapi-demo
```

#### 2. 创建虚拟环境（推荐）

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# 或
.venv\Scripts\activate  # Windows
```

#### 3. 安装依赖

```bash
pip install fastapi uvicorn sqlalchemy aiomysql python-dotenv pydantic
```

或使用 requirements.txt（如果有的话）：

```bash
pip install -r requirements.txt
```

#### 4. 启动 MySQL 数据库

**方式一：使用 Docker（推荐）**

```bash
docker-compose up -d
```

**方式二：使用本地 MySQL**

确保 MySQL 服务已运行，并创建数据库：

```sql
CREATE DATABASE jack_ai CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### 5. 配置环境变量

复制 `.env.example` 为 `.env`：

```bash
cp .env.example .env
```

编辑 `.env` 文件，修改数据库配置：

```env
DB_USER=root
DB_PASSWORD=root123
DB_HOST=localhost
DB_PORT=3306
DB_NAME=jack_ai
```

#### 6. 启动应用

```bash
# 方式一：使用 uvicorn 命令
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 方式二：直接运行 main.py
python main.py
```

启动成功后，你会看到：
```
✅ 数据库表创建成功！
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## API 接口文档

启动应用后，访问以下地址查看自动生成的 API 文档：

- **Swagger UI**（交互式文档）：http://localhost:8000/docs
- **ReDoc**（美观文档）：http://localhost:8000/redoc

### 接口列表

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/book/` | 创建新书籍 |
| GET | `/book/` | 分页查询书籍列表 |
| GET | `/book/{book_id}` | 获取单本书籍详情 |
| PUT | `/book/{book_id}` | 更新书籍信息 |
| DELETE | `/book/{book_id}` | 删除书籍 |
| GET | `/health` | 健康检查 |
| POST | `/book/init/test-data` | 初始化测试数据 |

## 使用示例

### 1. 创建书籍

```bash
curl -X POST "http://localhost:8000/book/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "三体",
    "author": "刘慈欣",
    "publisher": "重庆出版社",
    "publish_time": "2008-01-01T00:00:00",
    "isbn": "9787536692930",
    "description": "地球文明与三体文明的第一次接触"
  }'
```

### 2. 查询书籍列表

```bash
# 基础查询
curl "http://localhost:8000/book/?page=1&page_size=10"

# 按作者筛选
curl "http://localhost:8000/book/?author=刘慈欣"

# 关键字搜索
curl "http://localhost:8000/book/?keyword=三体"
```

### 3. 获取单本书籍

```bash
curl "http://localhost:8000/book/1"
```

### 4. 更新书籍

```bash
curl -X PUT "http://localhost:8000/book/1" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "修改后的描述"
  }'
```

### 5. 删除书籍

```bash
curl -X DELETE "http://localhost:8000/book/1"
```

## 代码架构图解

```
┌─────────────────────────────────────────────────────────────┐
│                        客户端请求                            │
│                    (HTTP Request)                            │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      main.py (路由层)                         │
│  - 接收请求                                                  │
│  - 参数验证                                                  │
│  - 调用业务逻辑                                              │
│  - 返回响应                                                  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    crud.py (数据访问层)                       │
│  - 封装数据库操作                                            │
│  - 执行 SQL 查询                                             │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                  database.py (数据库连接)                     │
│  - 管理连接池                                                │
│  - 提供会话                                                  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      MySQL 数据库                             │
└─────────────────────────────────────────────────────────────┘
```

## 核心概念解释

### 什么是异步编程？

传统同步编程：一次只能做一件事，等待数据库响应时程序会"卡住"。

异步编程：在等待数据库响应时，可以处理其他请求，提高并发能力。

```python
# 异步函数定义
async def get_book(book_id: int):
    # 等待数据库查询时，可以处理其他请求
    book = await db.get(Book, book_id)
    return book
```

### 什么是 ORM？

ORM（Object-Relational Mapping）让我们用 Python 对象操作数据库，而不是写 SQL 语句。

```python
# 使用 ORM（本项目的方式）
book = Book(name="三体", author="刘慈欣")
db.add(book)

# 等价于 SQL
# INSERT INTO book (name, author) VALUES ('三体', '刘慈欣')
```

### 什么是依赖注入？

FastAPI 会自动提供函数需要的参数。

```python
async def get_books(db: AsyncSession = Depends(get_db)):
    # FastAPI 会自动调用 get_db()，并将返回值赋给 db
    books = await db.execute(select(Book))
    return books
```

## 常见问题

### Q1: 启动时提示数据库连接失败？

**A**：检查以下几点：
1. MySQL 服务是否启动
2. `.env` 文件配置是否正确
3. 数据库是否已创建

### Q2: 如何重置数据库？

**A**：停止应用，删除并重新创建 MySQL 容器：

```bash
docker-compose down -v
docker-compose up -d
```

### Q3: 如何查看生成的 SQL 语句？

**A**：在 `database.py` 中将 `echo` 设为 `True`：

```python
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True  # 打印 SQL 语句
)
```

## 学习资源

- [FastAPI 官方文档](https://fastapi.tiangolo.com/zh/)
- [SQLAlchemy 2.0 文档](https://docs.sqlalchemy.org/en/20/)
- [Pydantic 文档](https://docs.pydantic.dev/)

## 下一步

尝试以下练习来提升你的技能：

1. 添加新的字段，如 `price`（价格）
2. 实现批量删除功能
3. 添加书籍分类功能
4. 实现更复杂的搜索（如按出版年份范围）
5. 添加用户认证和授权

## 许可证

MIT License

---

祝你学习愉快！如有问题，欢迎提 Issue。
