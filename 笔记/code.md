# Python 列表方法速查（对照 JavaScript 数组）

## 基础操作

| 操作 | Python | JavaScript | 说明 |
|------|--------|------------|------|
| 创建空列表 | `lst = []` | `let lst = []` | |
| 访问元素 | `lst[0]` | `lst[0]` | |
| 长度 | `len(lst)` | `lst.length` | Python 用函数，JS 用属性 |
| 最后一个元素 | `lst[-1]` | `lst[lst.length - 1]` | Python 支持负数索引 |

## 增删改

| 操作 | Python | JavaScript | 说明 |
|------|--------|------------|------|
| 末尾添加 | `lst.append(x)` | `lst.push(x)` | |
| 指定位置插入 | `lst.insert(0, x)` | `lst.splice(0, 0, x)` | |
| 删除末尾 | `lst.pop()` | `lst.pop()` | 一样 |
| 删除指定位置 | `lst.pop(0)` | `lst.splice(0, 1)` | Python pop 返回被删元素 |
| 删除指定值 | `lst.remove(x)` | `lst.splice(lst.indexOf(x), 1)` | Python 按值删 |
| 清空 | `lst.clear()` | `lst.length = 0` | |

## 查找

| 操作 | Python | JavaScript | 说明 |
|------|--------|------------|------|
| 查索引 | `lst.index(x)` | `lst.indexOf(x)` | |
| 判断存在 | `x in lst` | `lst.includes(x)` | |
| 计数 | `lst.count(x)` | `lst.filter(v => v === x).length` | |

## 遍历

| 操作 | Python | JavaScript | 说明 |
|------|--------|------------|------|
| 直接遍历 | `for x in lst:` | `for (const x of lst)` | |
| 带索引遍历 | `for i, x in enumerate(lst):` | `lst.forEach((x, i) => {})` | |
| 索引范围 | `for i in range(5):` | `for (let i = 0; i < 5; i++)` | |

## 变换

| 操作 | Python | JavaScript | 说明 |
|------|--------|------------|------|
| 映射 | `list(map(fn, lst))` | `lst.map(fn)` | |
| 过滤 | `list(filter(fn, lst))` | `lst.filter(fn)` | |
| 排序 | `lst.sort()` | `lst.sort()` | |
| 反转 | `lst.reverse()` | `lst.reverse()` | |
| 切片 | `lst[1:3]` | `lst.slice(1, 3)` | |
| 拼接 | `lst1 + lst2` | `lst1.concat(lst2)` | |
| 展开 | `[*lst1, *lst2]` | `[...lst1, ...lst2]` | |

## 常用小技巧

```python
# 列表推导式（类似 JS 的 map + filter 合体）
[x * 2 for x in range(10) if x % 2 == 0]
# 等价 JS: [0,1,2,3,4,5,6,7,8,9].filter(x => x % 2 === 0).map(x => x * 2)

# 解构
a, b = [1, 2]        # a=1, b=2
first, *rest = [1,2,3]  # first=1, rest=[2,3]

# 同时拿到索引和值
for i, x in enumerate(['a', 'b', 'c']):
    print(i, x)  # 0 a / 1 b / 2 c
```

---

## SQLAlchemy Column 常用参数

`Column` 用来定义数据库表的字段。

```python
Column(类型, primary_key=True, index=True, nullable=False, unique=True, default=xxx)
```

| 参数 | 说明 | 示例 |
|--|--|--|
| `类型` | 字段类型 | `Integer`, `String`, `Boolean`, `DateTime`, `Float`, `Text` |
| `primary_key` | 是否为主键 | `Column(Integer, primary_key=True)` |
| `index` | 是否创建索引（加快查询速度） | `Column(String, index=True)` |
| `nullable` | 是否允许为空（默认允许） | `Column(String, nullable=False)` |
| `unique` | 是否唯一（如用户名不重复） | `Column(String, unique=True)` |
| `default` | 默认值 | `Column(DateTime, default=datetime.utcnow)` |
| `server_default` | 数据库层面的默认值 | `Column(Integer, server_default=text("0"))` |
| `autoincrement` | 是否自增（主键默认开启） | `Column(Integer, autoincrement=True)` |

### 常用字段类型

| 类型 | 对应数据库 | 说明 |
|--|--|--|
| `Integer` | INT | 整数 |
| `String(长度)` | VARCHAR | 字符串，PostgreSQL 会自动转成 VARCHAR |
| `Text` | TEXT | 长文本，不限长度 |
| `Boolean` | BOOLEAN | 布尔值 |
| `DateTime` | TIMESTAMP | 日期时间 |
| `Float` | FLOAT | 浮点数 |
| `LargeBinary` | BLOB | 二进制数据（如图片、文件） |

### 示例：定义一个用户表

```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)           # 主键，自增
    username = Column(String, unique=True, nullable=False)       # 唯一，不能为空
    email = Column(String, unique=True, index=True)              # 唯一，有索引
    hashed_password = Column(String, nullable=False)             # 密码，不能为空
    is_active = Column(Boolean, default=True)                    # 默认启用
    created_at = Column(DateTime, default=datetime.utcnow)       # 创建时间
```

---

## 虚拟环境（Windows / PowerShell）

激活（提示符前会出现 `(.venv)`）：

```powershell
cd F:\pythonCode\blogsAPISystem
.\.venv\Scripts\Activate.ps1
```

若提示无法运行脚本：

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**觉得激活麻烦时**：不激活也可以，直接用 venv 里的解释器，路径清晰、不易混用全局 Python：

```powershell
.\.venv\Scripts\python.exe main.py
.\.venv\Scripts\python.exe -m pip install 包名
```

Cursor / VS Code：选好解释器为 `.venv\Scripts\python.exe`，终端常会自带虚拟环境。

---

## FastAPI：JWT + `OAuth2PasswordBearer`

`oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")` 的含义：

- 告诉 FastAPI：**受保护接口从请求头读取** `Authorization: Bearer <token>`
- `tokenUrl` 主要给 **Swagger / OpenAPI 文档**用，标明 token 从哪个登录地址换取

`get_current_user` 里 `token: str = Depends(oauth2_scheme)`：请求进来时先取 token，再解码、查库。

使用 **表单登录**（`OAuth2PasswordRequestForm`）时，需要安装 **`python-multipart`**，否则会报错：`Form data requires "python-multipart"`。

---

## OAuth2 Password Flow vs HTTP Bearer（文档体验）

| 方案 | 运行时本质 | Swagger `Authorize` 常见样子 |
|------|------------|------------------------------|
| **OAuth2 Password** | 仍是 `Bearer <token>` | 用户名 / 密码表单（或配合 token URL） |
| **HTTP Bearer** | 只认 Bearer 头 | Often 单一 token 输入框 |

JWT 校验逻辑可以相同；差别多在「文档里怎么登录、怎么填 token」。

访问受保护接口时，请求头必须是：

`Authorization: Bearer <access_token>`（注意 **`Bearer` 后面有空格**）。

---

## `raise HTTPException(status_code, detail)`

- `raise`：立刻结束当前处理函数
- `HTTPException`：FastAPI 按给定状态码返回 JSON 错误
- 常用：`400` 参数/业务错误，`401` 未登录或 token 无效，`403` 无权限，`404` 资源不存在

---

## 鉴权写在路由上还是「全局」？

- **不是所有接口都要登录**（如 `/`、`/register`、`/login`），一般不挂在整个 `app` 上。
- **按路由注入** `Depends(get_current_user)`：一眼能看出哪个接口要登录。
- 进阶：用 `APIRouter(..., dependencies=[Depends(get_current_user)])` 给一组路由统一加鉴权。

---

## 本地调试：`/docs` 转圈、`curl` 超时

常见原因：

1. **多个 uvicorn / 多次 `python main.py`**，端口 `8000` 上不止一个监听进程，或大量 `CLOSE_WAIT` → 连接卡住。
2. **数据库连不上**（如 Postgres 未启动、`DATABASE_URL` 错误），部分请求会一直等。

处理思路：

1. 停掉所有服务，`netstat -ano | findstr ":8000"`，对多余 PID `taskkill /PID xxx /F`。
2. **只在一个终端**启动：`.\.venv\Scripts\python.exe main.py`。
3. 自检：`curl.exe -m 5 http://127.0.0.1:8000/` 应很快返回 `{"msg":"hello world"}`。

怀疑 reload 捣乱时，可暂时把 `reload=False` 跑稳后再开。

---

## `post_owned_by`（文章归属判断）

用于 **PUT/DELETE 文章** 前判断「是不是本人」：

1. **`post.user_id` 与 `user.id`** 转成 `int` 后相等 → 有权。
2. 否则再看 **`post.author` 与 `user.username`**（`strip()` 后）是否相等 → 兼容旧数据里 `user_id` 曾填错的情况。

详细逐行解释见 **`笔记/python学习日记.md`** 里「`post_owned_by` 函数逐行翻译」一节。