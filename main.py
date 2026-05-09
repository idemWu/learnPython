"""
FastAPI 后端接口文件
类似前端：API 路由定义 + 请求/响应数据类型定义
"""
import uvicorn
from datetime import datetime, timedelta, timezone

from fastapi import FastAPI, Depends, HTTPException , OAuth2PasswordBearer
from pydantic import BaseModel, ConfigDict

from models import User, Post
from database import SessionLocal

from passlib.context import CryptContext
from jose import jwt


# ========== JWT 配置 ==========
SECRET_KEY = "your-secret-key-change-this"  # 实际项目放在 .env 中
ALGORITHM = "HS256"  # JWT 加密算法
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # token 有效期（分钟）

# 密码加密上下文（bcrypt 算法）
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    """密码加密，返回哈希值（单向，不可逆）"""
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    """验证密码：明文 vs 数据库里的哈希值"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    """生成 JWT token，data 是要编码的数据（如用户ID、用户名）"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})  # 加入过期时间
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ========== Pydantic 模型（请求/响应数据格式） ==========
# 类似前端的 TypeScript 接口定义

class UserRegister(BaseModel):
    """注册请求体（前端传什么）"""
    username: str
    password: str
    name: str = None
    age: int = None


class UserLogin(BaseModel):
    """登录请求体（前端传什么）"""
    username: str
    password: str


class TokenResponse(BaseModel):
    """登录成功返回的 token"""
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """用户响应体（返回给前端什么）"""
    model_config = ConfigDict(from_attributes=True)  # 允许从 SQLAlchemy 对象读属性
    id: int
    name: str
    age: int


class UserCreate(BaseModel):
    """创建用户请求体（老接口，保留兼容）"""
    name: str
    age: int


class PostCreate(BaseModel):
    """创建文章请求体（前端传什么）"""
    title: str
    content: str
    author: str = None


class PostResponse(BaseModel):
    """文章响应体（返回给前端什么）"""
    model_config = ConfigDict(from_attributes=True)  # 允许从 SQLAlchemy 对象读属性
    id: int
    title: str
    content: str
    author: str


# ========== FastAPI 应用 ==========
app = FastAPI()


def get_db():
    """
    数据库会话依赖注入
    每次请求创建新连接，请求结束自动关闭
    类似前端：每个 API 请求拿到一个独立的数据库连接
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme) , db=Depends(get_db)):
    #1. 先准备一个统一的 401 异常
    credentials_exception = HTTPException(
        status_code = 401,
        detail = "无效的认证凭证",
        headers = {"WWW-Authenticate":"Bearer"}
    )

    #2.解码token ， 取出用户名
    try:
        payload = jwt.decode(token , SECRET_KEY , algorithm=[ALGORITHM])
        username = payload.get('sub')
        if username  is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    #3 去数据库查这个用户
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception

    #4 返回当前登录用户对象
    
    return user 




# ========== 路由（接口） ==========
@app.get("/")
def hello():
    """测试接口"""
    return {"msg": "hello world"}


@app.get("/users", response_model=list[UserResponse])
def get_users(db=Depends(get_db)):
    """获取所有用户列表"""
    return db.query(User).all()


@app.get("/users/{user_id}", response_model=UserResponse)
def search_user(user_id: int, db=Depends(get_db)):
    """根据 ID 查询单个用户"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user


@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db=Depends(get_db)):
    """创建新用户（老接口，保留兼容）"""
    new_user = User(name=user.name, age=user.age)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/register")
def register(user: UserRegister, db=Depends(get_db)):
    """注册：用户名 + 密码，密码加密后存入数据库"""
    # 1. 检查用户名是否已存在
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="用户名已存在")

    # 2. 密码加密（不能明文存）
    hashed_pwd = hash_password(user.password)

    # 3. 创建数据库用户对象
    new_user = User(
        username=user.username,
        hashed_password=hashed_pwd,
        name=user.name,
        age=user.age,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db=Depends(get_db)):
    """登录：验证密码，返回 JWT token（类似前端拿到 token 存 localStorage）"""
    # 1. 查找用户
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="用户不存在")

    # 2. 验证密码
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="密码错误")

    # 3. 生成 JWT token（sub 是 JWT 标准字段，放用户标识）
    token = create_access_token({"sub": db_user.username})

    # 4. 返回 token
    return {"access_token": token, "token_type": "bearer"}




# ===================== POST 文章CRUD ======================
@app.post("/posts" , response_model=PostResponse)
def create_post(post:PostCreate , db=Depends(get_db)):
    new_post = Post(**post.model_dump()) #1.创建 Post 对象
    db.add(new_post)       #2.加入会话
    db.commit()            #3.提交到数据库
    db.refresh(new_post)   #4.拿到数据库生成的 id 
    return new_post        #5.返回给前端 

@app.get("/allPosts")
def get_allPosts(db=Depends(get_db)):
    """""获取所有文章列表"""
    return db.query(Post).all()

@app.get("/posts/{post_id}", response_model=PostResponse)
def get_onePost(post_id: int, db=Depends(get_db)):
    """查看单篇文章"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="文章不存在")
    return post

@app.put("/posts/{post_id}")
def putPost(post_id: int, post_data: PostCreate, db=Depends(get_db)):
    """更新文章"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="文章不存在")

    post.title = post_data.title
    post.content = post_data.content
    post.author = post_data.author

    db.commit()
    db.refresh(post)
    return post

@app.delete("/posts/{post_id}")
def deletePost(post_id: int, db=Depends(get_db)):
    """删除文章"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="文章不存在")
    db.delete(post)
    db.commit()
    return {"message": "文章删除成功"}




if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)