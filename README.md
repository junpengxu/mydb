# MyDb
awesome db create myself database

## 实现一个数据库玩玩
### 架构图
![](./static/db_structure.png)

- 其实我认为一个简单的数据库，可以当作一个B树，通过合理的使用B树即可完成一个数据库的实现
- 依赖的B树处理逻辑，采用了开源项目 [NicolasLM/bplustree](https://github.com/NicolasLM/bplustree)
- 画图使用了drawio，原文件存放在    `mydb/static/MyDB-数据库设计.drawio`

### server
- 通过tcp来接受请求
  
### table
- 具体的数据表操作

### client
- 真正操作数据库的客户端

### 设计理念
结构与存储分离，所有的数据表结构都保存到 `mydb` 文件中， 具体文件保存到数据库同名文件

### 已实现功能
- 数据库初始化 `python init_database.py`，可以创建出一个空的数据库结构，并且初始化用户表以及一个用户
