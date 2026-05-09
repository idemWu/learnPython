# 定义一个列表（list），里面装了两个字典（dict）
# 列表 = 前端的数组 []
# 字典 = 前端的对象 {}
user = [
    {"name": "Tom", "age": 18},
    {"name": "Jerry", "age": 20},
]

# def：定义函数的关键字（类似 JavaScript 的 function）
# 参数不需要声明类型，直接用冒号后写参数名
def add_user(name, age):
    # append()：往列表末尾添加元素（类似前端的 .push()）
    user.append({"name": name, "age": age})

# 调用函数，传入两个参数
add_user('Jerry', 20)

# print：打印到控制台（类似前端的 console.log）
print(user) 



