import os
import random
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy import Column,Integer,String,ForeignKey,DateTime,Date,Text,Enum
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

USERNAME='root'
PASSWORD='123456'
HOST='127.0.0.1'
PORT=3306
DATABASE='person'
DB_URI='mysql+pymysql://{}:{}@{}:{}/{}'.format(USERNAME,PASSWORD,HOST,PORT,DATABASE)

engine=create_engine(DB_URI,echo=True)
Base=declarative_base(engine)
DEFAULT_AVATAR_DIR='static/avatar/default/'
default_avatars=['../'+DEFAULT_AVATAR_DIR+i for i in os.listdir(DEFAULT_AVATAR_DIR)]
class User(Base):
    __tablename__='user'
    Id=Column(Integer,primary_key=True)
    Name=Column(String(50),nullable=False)
    Email=Column(String(50),nullable=False)
    Password=Column(String(100),nullable=False)
    Avatar=Column(String(100),nullable=False,default=random.sample(default_avatars,1)[0])
    Notify=Column(Enum('1','2','3'),nullable=False,default='1')
    Lastlogin=Column(DateTime,nullable=False,default=datetime.now)
class Tech(Base):
    __tablename__='tech'
    Id=Column(Integer,primary_key=True)
    Label=Column(String(20),nullable=False)
    Detail=Column(String(320),nullable=False)
class Game(Base):
    __tablename__='game'
    Id=Column(Integer,primary_key=True)
    Label=Column(String(30),nullable=False)
    Name=Column(String(20),nullable=False)
    Detail=Column(String(360),nullable=False)
    Image=Column(String(100),nullable=False)
    Url=Column(String(100),nullable=False)
class Comment(Base):
    __tablename__='comment'
    Id=Column(Integer,primary_key=True)
    Content=Column(Text,nullable=False)
    Path=Column(String(20),nullable=False)
    From=Column(Integer,ForeignKey('user.Id'),nullable=False)
    Time=Column(DateTime,nullable=False,default=datetime.now)
class Like(Base):
    __tablename__='like'
    Id=Column(Integer,primary_key=True)
    To=Column(Integer,ForeignKey('comment.Id'),nullable=False)
    From=Column(Integer,ForeignKey('user.Id'),nullable=False)
class GameData(Base):
    __tablename__='gamedata'
    Id=Column(Integer,primary_key=True)
    GameName=Column(String(20),nullable=False)
    Player=Column(String(32),nullable=False)
    Data=Column(Text,nullable=False,default='')
    Result=Column(String(32),nullable=False,default='')
Base.metadata.create_all()

sem=sessionmaker(bind=engine)()

def model_to_dict(result):
    from collections import Iterable
    try:
        if isinstance(result, Iterable):
            tmp = [dict(zip(res.__dict__.keys(), res.__dict__.values())) for res in result]
            for t in tmp:
                t.pop('_sa_instance_state')
        else:
            tmp = dict(zip(result.__dict__.keys(), result.__dict__.values()))
            tmp.pop('_sa_instance_state')
        return tmp
    except BaseException as e:
        print(e.args)
        raise TypeError('Type error of parameter')