from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from django.db import models

# db = SQLAlchemy()

# class Book(db.Model):


engine = create_engine('mysql://root:123456@localhost:3306/test', echo=True, pool_size=5, pool_recycle=60*30)

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    email = Column(String(64))

    def __init__(self, name, email):
        self.name = name
        self.email = email


# 生成数据库表，创建表，如果存在则忽略
Base.metadata.create_all(engine)

# 创建session，绑定数据库
DbSession = sessionmaker(bind=engine)
session = DbSession()


# # 增加一条数据
# xiaoming = Users('xiaoming', 'xiaoming068@xx.com')
# session.add(xiaoming)   # add会将Module保存到session中
# session.commit()        # commit才会提交到数据库
#
# # TODO: 如果数据属性为unique，插入重复数据时会保存
#
# # 增加多条数据
# 1. add_all增加多条
# xiaohong = Users('xiaohong', 'xiaohong068@xx.com')
# xiaogang = Users('xiaogang', 'xiaogang068@xx.com')
# session.add_all([xiaohong, xiaogang])

# # 2. 遍历数据增加多条
# for instance in [xiaohong, xiaogang]:
#     session.add(instance)

# TODO: add_all也是遍历数据，逐条增加


# 查询数据
users = session.query(Users).filter_by(id=1).all()
for item in users:
    print(item.name, item.email)


# 未commit的数据如何查询
# lisi = Users('lisi', 'lisi068@xx.com')
# session.add(lisi)
# session.commit() 不commit
# session.flush()
users = session.query(Users).filter_by(name='lisi').all()
for item in users:
    print(item.name, item.email)


# 删一条
zhangsan = session.query(Users).filter_by(name='zhangsan').first()
if zhangsan:
    session.delete(zhangsan)
    session.commit()


# 删除所有
session.query(Users).filter(Users.name == 'zhangsan').delete()
session.commit()


# 改
# session.query(Users).filter_by(name='xiaoming').update({'name': 'xiaoming_plus'})
# session.commit()

xiaoming_plus = session.query(Users).filter_by(name='xiaoming_plus').first()
xiaoming_plus.name = 'xiaoming'
session.add(xiaoming_plus)
session.commit()
