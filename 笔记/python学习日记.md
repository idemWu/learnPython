# Python 学习日记

## Day 0：环境搭建（2026-04-28）

### 确认 Python 环境

```bash
f:/py/python.exe --version    python --version
# Python 3.14.4

f:/py/python.exe -m pip --version  python -m pip --version
# pip 26.0.1
```

> **问：为什么虚拟环境外要写 `f:/py/python.exe`，虚拟环境内直接写 `python`？**
>
> 答：跟 **环境变量 PATH** 有关。
> - 系统 PATH 里没有 `python`，所以必须写完整路径。
> - 激活虚拟环境后，`.venv\Scripts\Activate.ps1` 会把 `.venv\Scripts` 临时加到 PATH 最前面。
> - 输入 `python` 时，系统会优先找到虚拟环境的 `python.exe`。
> - 用 `where python` 可以验证第一个路径指向 `.venv\Scripts\python.exe`。

### 创建虚拟环境

```bash
f:/py/python.exe -m venv .venv     python -m venv .venv
```

### 激活虚拟环境（PowerShell）：

```bash
.\.venv\Scripts\Activate.ps1
```

> 注意：文件名是 `ps1`（数字1），不是 `psl`（字母l）。
> 激活成功后，命令行前面会出现 `(.venv)` 标记。

### 理解：虚拟环境是什么？

虚拟环境就像前端的 `node_modules`，把项目依赖隔离开，不跟系统其他项目冲突。

---

### Day 1 实战：熟悉 Python 数据结构

创建了 `day1.py`，练习列表（list）和字典（dict）：

```python
# 模拟用户数据处理
users = [{"name": "Tom", "age": 18}]

def add_user(name, age):
    users.append({"name": name, "age": age})

add_user("Jerry", 20)
print(users)
```

运行结果：
```
[{'name': 'Tom', 'age': 18}, {'name': 'Jerry', 'age': 20}]
```

> **核心概念对照前端：**
> - 列表 `[]` = 前端的 **数组** `[]`
> - 字典 `{}` = 前端的 **对象** `{}`
> - `append()` = 前端的 `.push()`

这是后端最常用的数据结构，后面处理 API 请求、数据库查询都离不开它。

---

## Day 2：FastAPI 入门（2026-04-28）

### 安装依赖

```bash
pip install fastapi uvicorn
```

- `fastapi`：后端框架，类似前端的 Express / Koa
- `uvicorn`：服务器，负责运行 FastAPI 应用

### 创建第一个接口 —— main.py

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {"msg": "hello world"}
```

### 启动服务：两种方式

#### 方式一：用 uvicorn 命令（推荐）

```bash
uvicorn main:app --reload
```
- `main`：对应 `main.py` 文件名（不加 `.py`）
- `app`：对应文件里的 `app = FastAPI()` 变量
- `--reload`：代码改动后自动重启服务（开发阶段必加）

#### 方式二：用 python 直接运行

先在 `main.py` 末尾加上：
```python
import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
```

然后：
```bash
python main.py
```

> **区别：**
> - `uvicorn main:app --reload`：命令行启动，适合生产环境搭配 systemd/supervisor
> - `python main.py`：适合本地开发调试，一行命令搞定
>
> **`__name__` 是什么？**
> - 每个 Python 文件都有一个内置的 `__name__` 变量
> - 直接运行 `python main.py` 时，`__name__` = `"__main__"`
> - 被其他文件 `import` 时，`__name__` = 文件名
> - 所以 `if __name__ == "__main__"` 就是"只有直接运行这个文件时才执行"

启动后访问：
- http://127.0.0.1:8000 → 返回 `{"msg":"hello world"}`
- http://127.0.0.1:8000/docs → 自动生成的接口文档（Swagger UI）

### pip vs npm 对照

`pip` 就是 Python 的 `npm`。

| 操作 | npm (Node.js) | pip (Python) |
|--|--|--|
| 安装包 | `npm install xxx` | `pip install xxx` |
| 记录依赖 | `package.json` | `requirements.txt` / `pyproject.toml` |
| 安装全部依赖 | `npm install` | `pip install -r requirements.txt` |
| 卸载包 | `npm uninstall xxx` | `pip uninstall xxx` |
| 查看已安装 | `npm list` | `pip list` |
| 冻结当前版本 | `npm shrinkwrap` | `pip freeze > requirements.txt` |

### PostgreSQL 驱动安装

```bash
pip install psycopg2-binary
```

- `psycopg2`：PostgreSQL 的 Python 驱动
- `binary` 版本不需要额外装 C 库，开箱即用
- SQLAlchemy 连接 PostgreSQL 时需要用到它

连接字符串格式：
```
postgresql://用户名:密码@localhost:5432/数据库名
```

```bash
pip freeze > requirements.txt
```

记录当前环境所有依赖。换电脑后恢复：
```bash
pip install -r requirements.txt
```

#### pyproject.toml

类似前端的 `package.json`，功能更全面：

```toml
[project]
name = "blogs-api-system"
version = "0.1.0"
description = "博客 API 后端系统"
requires-python = ">=3.14"

dependencies = [
    "fastapi>=0.136.0",
    "uvicorn>=0.46.0",
]
```

| 文件 | 类似前端 | 作用 |
|--|--|--|
### Swagger 文档是怎么来的？

Swagger 是 **API 文档自动生成工具**。

传统后端开发：写完接口后需要手动写文档（接口地址、参数、返回格式），很容易文档和代码不一致。

FastAPI 的做法：

```
你写的代码（类型注解）
        ↓
FastAPI 自动解析（依赖 Pydantic）
        ↓
生成 OpenAPI 规范（JSON）
        ↓
Swagger UI 渲染成网页
```

> **关键点：**
> - 不是"FastAPI 接了 Swagger"，而是 FastAPI 原生支持 OpenAPI 标准
> - Swagger 只是把 OpenAPI 规范渲染成可视化页面
> - 只要你改了接口，文档自动更新，零维护成本
>
> 这也是为什么很多人选 FastAPI 而不是 Flask —— **写代码的同时文档就生成了**。

| 文件 | 类似前端 | 作用 |
|--|--|--|
| `requirements.txt` | `package-lock.json` | 纯依赖清单 |
| `pyproject.toml` | `package.json` | 项目配置 + 依赖清单 |
| `.venv/` | `node_modules/` | 隔离的项目依赖目录 |

---

## Day 3：数据库（2026-04-29）

### SQLAlchemy + PostgreSQL 配置

安装依赖（用 Poetry）：
```bash
poetry add sqlalchemy psycopg2-binary python-dotenv
```

### 项目结构

```
database.py  → 数据库连接配置
models.py    → 数据模型（表结构）
main.py      → API 接口
.env         → 环境变量（数据库密码等）
```

### database.py

```python
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# 必须先加载 .env 文件
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)
```

### models.py

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
```

### main.py（数据库版本）

```python
from fastapi import FastAPI, Depends
from pydantic import BaseModel, ConfigDict
import uvicorn

from models import User
from database import SessionLocal

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    age: int

class UserCreate(BaseModel):
    name: str
    age: int

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users", response_model=list[UserResponse])
def get_users(db=Depends(get_db)):
    return db.query(User).all()

@app.get("/users/{user_id}", response_model=UserResponse)
def search_user(user_id: int, db=Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        return user
    return {"error": "用户不存在"}

@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db=Depends(get_db)):
    new_user = User(name=user.name, age=user.age)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
```

### 重要概念

- `create_engine()` = 创建数据库连接（类似前端的连接池）
- `SessionLocal` = 数据库会话，增删改查都要通过它
- `Depends(get_db)` = FastAPI 依赖注入，自动创建和关闭数据库连接
- `response_model=UserResponse` = 告诉 FastAPI 怎么把 SQLAlchemy 对象转成 JSON
- `ConfigDict(from_attributes=True)` = 允许 Pydantic 从 ORM 对象读取属性

### 数据库写入流程：数据是怎么存进去的？

一个 `POST /users` 请求的完整链路：

```
浏览器发请求 → FastAPI 接收 → 执行代码 → PostgreSQL 改表
```

#### 四步走

```python
# 第 1 步：创建 Python 对象（还没碰数据库）
new_user = User(name=user.name, age=user.age)
# 此时 new_user 只是内存里的对象，数据库不知道它存在

# 第 2 步：把对象加入 Session（还没提交）
db.add(new_user)
# 标记为"待插入"，类似 git add，数据库还是没变化

# 第 3 步：提交到数据库（真正改表了）
db.commit()
# 真正向 PostgreSQL 发送了 INSERT 语句
# users 表里多了一条记录

# 第 4 步：刷新拿到数据库生成的 id
db.refresh(new_user)
# id 是数据库自动生成的（自增），Python 对象里还没有
# refresh() 去数据库把最新的 id 拿回来
```

#### 一句话总结

| 代码 | 类似 Git | 实际效果 |
|--|--|--|
| `new_user = User(...)` | 写了个新文件 | 内存里的对象 |
| `db.add(new_user)` | `git add` | 标记为待插入 |
| `db.commit()` | `git commit` | **真正写入数据库** |
| `db.refresh(new_user)` | 重新读文件 | 拿到数据库生成的 id |

#### 为什么需要 `db.refresh()`？

因为 `id` 是数据库自增生成的，Python 对象一开始不知道：

```python
new_user = User(name="张三", age=25)
print(new_user.id)  # → None

db.add(new_user)
db.commit()         # 数据库生成了 id = 3
print(new_user.id)  # → 还是 None！Session 没有自动同步回来

db.refresh(new_user)
print(new_user.id)  # → 3，现在拿到了
```

不调 `refresh()`，前端拿到的就是 `{"id": null, "name": "张三", "age": 25}`，下次操作这条数据就没法定位。

### 前端视角：Pydantic vs SQLAlchemy 模型的区别

**为什么有两个"Model"？容易搞混。**

| 代码 | 属于哪个库 | 作用 | 类比前端 |
|--|--|--|--|
| `class Base(DeclarativeBase)` | SQLAlchemy | 数据库模型的基类 | `class Model {}`（TS 基类） |
| `class Post(Base)` | SQLAlchemy | 数据库里的一张表 | 数据库表结构定义 |
| `class PostCreate(BaseModel)` | Pydantic | 定义请求体格式 | TypeScript 接口 `interface PostCreate {}` |
| `class PostResponse(BaseModel)` | Pydantic | 定义响应体格式 | TypeScript 接口 `interface PostResponse {}` |

**简单理解：**
- **SQLAlchemy 模型（继承 `Base`）** = 数据库表长什么样
- **Pydantic 模型（继承 `BaseModel`）** = 前后端传输数据长什么样

```
前端发请求 → Pydantic 验证请求体格式
                           ↓
                     SQLAlchemy 操作数据库
                           ↓
              Pydantic 把数据库对象转成 JSON 返回前端
```

### `pass` 是什么？

`pass` 在 Python 里就是 **"什么都不做"**，是个占位符。

当语法要求必须写点什么，但你暂时不需要写代码时使用。

```python
class Base(DeclarativeBase):
    pass  # 这个类没有自己的方法，纯粹就是继承基类
```

类比 JavaScript：
```javascript
class Base extends DeclarativeBase {
    // 空类，没有任何方法
}
```

没有 `pass` 的话，Python 会报语法错误，因为类体不能为空。

### `model_config = ConfigDict(from_attributes=True)`

Pydantic 默认只认**字典和 JSON**，不认识 SQLAlchemy 对象。

加了这个配置后，Pydantic 就能从 SQLAlchemy 对象上**读取属性**，转成 JSON 返回给前端。

```python
db_user = db.query(User).first()  # 这是 SQLAlchemy 对象
return UserResponse.model_validate(db_user)  # Pydantic 把对象属性读出来转 JSON
```

### 踩坑记录

**Bug 6：`passlib` + 新版 `bcrypt` 不兼容**

新版 `bcrypt`（5.x）删掉了 `__about__` 属性，`passlib` 依赖这个属性来检测版本，导致密码加密时报错：

```
ValueError: password cannot be longer than 72 bytes
```

修复方法：降级 `bcrypt` 到 4.0.1：

```bash
pip install bcrypt==4.0.1
```

**Bug 1：`os.getenv("DATABASE_URL")` 返回 None**

原因：Python 原生的 `os.getenv()` **只会读操作系统的真实环境变量**，不会自动读 `.env` 文件。

`.env` 只是一个约定俗成的文件，Python 本身不知道它的存在。需要靠 `python-dotenv` 来"搬运"：

```
.env 文件（你写的配置）
       ↓
python-dotenv 搬运工（load_dotenv）
       ↓
操作系统环境变量（os.getenv 能读到的地方）
       ↓
你的代码：os.getenv("DATABASE_URL")
```

如果不用 `.env`，也可以在终端直接设置环境变量：
```bash
# Linux/Mac
export DATABASE_URL=postgresql://...

# Windows (PowerShell)
$env:DATABASE_URL="postgresql://..."
```
但 `.env` 更方便——不用每次开终端都手动设置。

```python
from dotenv import load_dotenv
load_dotenv()  # 必须先调用这个
DATABASE_URL = os.getenv("DATABASE_URL")
```

**Bug 2：`DeclarativeBase() takes no arguments`**

原因：`DeclarativeBase` 是基类，应该继承而不是实例化。

```python
# 错误
Base = DeclarativeBase()

# 正确
class Base(DeclarativeBase):
    pass
```

**Bug 3：`datetime.utcnow()` 在 Python 3.14 中已弃用**

原因：Python 3.12+ 推荐使用时区感知的写法，`utcnow()` 被认为是"naive"时间（不带时区信息）。

```python
# 错误（Python 3.12+ 会报警告）
from datetime import datetime
datetime.utcnow()

# 正确
from datetime import datetime, timezone
datetime.now(timezone.utc)
```

**Bug 4：JWT 工具函数写了但缺少导入**

`create_access_token` 函数里用了 `datetime` 和 `timedelta`，但文件顶部没 import，导致 `NameError`。

```python
# 必须导入
from datetime import datetime, timedelta, timezone
```

**Bug 5：`Depends(get_db)` 的理解误区**

`Depends(get_db)` 不是"拿到数据库"，而是**"拿到一个数据库会话（连接）"**。

这是 FastAPI 的**依赖注入**机制。执行流程：

```
请求到达 → FastAPI 看到 Depends(get_db) 
         → 调用 get_db() 
         → get_db() 创建 db 连接，yield 给接口函数
         → 接口函数执行完毕
         → FastAPI 走 get_db() 的 finally 块，关闭连接
```

**为什么必须用 `Depends`？**

每次请求都会有一个**全新的、独立的**数据库连接，请求结束自动关闭。不用 `Depends` 的话，每个接口都要手动写：

```python
# 不用 Depends，每个接口都要写这些样板代码
def get_users():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        return users
    finally:
        db.close()
```

用 `Depends` 后，FastAPI 自动管理连接的创建和销毁，代码更干净。

```python
# 用 Depends，一行搞定
@app.get("/users")
def get_users(db=Depends(get_db)):
    return db.query(User).all()
```

### Day 4 项目结构规范

代码应该按功能分区，从上到下：

```python
# 1. 标准库 import
import os
from datetime import datetime, timedelta, timezone

# 2. 第三方库 import
from fastapi import FastAPI, Depends
from pydantic import BaseModel, ConfigDict
from passlib.context import CryptContext
from jose import jwt

# 3. 本地模块 import
from models import User
from database import SessionLocal

# 4. 配置常量
SECRET_KEY = "xxx"
ALGORITHM = "HS256"

# 5. 工具函数（加密、JWT 等）
def hash_password(...): ...

# 6. Pydantic 模型
class UserCreate(BaseModel): ...

# 7. FastAPI 应用和路由
app = FastAPI()
@app.get("/") ...
```

不要把所有东西混在一起，路由函数夹在工具函数中间很难读。
