#!/usr/bin/python3
# -*- coding=utf-8 -*-
# date: 2017-12-2
# 读取经纬度xml，并存入mysql中
import xml.dom.minidom
# import pymsql
from os.path import dirname
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


# 定义城市对象:
class City(Base):
    # 表的名字:
    __tablename__ = 'city'

    # 表的结构:
    id = Column(String(20), primary_key=True)
    cname = Column(String(20))
    pname = Column(String(20))
    longitude = Column(String(20))
    altitude = Column(String(20))


# dsn = 'mysql://root@localhost/test'
dsn = 'sqlite:///:memory:'


class Test(object):
    def __init__(self, dsn):
        try:
            eng = create_engine(dsn, echo=True)
        except ImportError:
            raise RuntimeError()

        try:
            eng.connect()  # 尝试连接数据库
        except exc.OperationalError:
            eng = create_engine(dirname(dsn))
            eng.excute('CREATE DATABASE test').close()
            eng = create_engine(dsn)

        Session = orm.sessionmaker(bind=eng)
        self.ses = Session()
        self.city = City.__table__
        self.eng = self.city.metadata.bind = eng  # 引擎与表的元数据进行额外的绑定

    def insert(self, cname, pname, longitude, altitude):
        self.ses.add_all(City(cname, pname, longitude, altitude))
        self.ses.commit()

    def check(self, lo, al):
        try:
            city = self.ses.query(
                City).filter_by(
                longitude=103.97, altitude=24.85)
            printf('%s') % city


    def __getattr__(self, attr):
        return getattr(self.users, attr)
    def finish(self):
       self.ses.connection().close()

def main():
    dom = xml.dom.minidom.parse('jinweiduxinxi.xml')
    root = dom.documentElement
    p_list = root.getElementsByTagName('provinces')

    try:
        orm = Test(dsn)  # 创建一个SQLAlchemyTest对象，将其用于所有的数据库操作
    except RuntimeError:
        printf('ERROR: sql not supported or unreachable, exiting')
        return

    printf('\n*** Create users table (drop old one if appl.)')
    orm.drop(checkfirst=True)
    orm.create()

    printf('\n*** Insert citys into table')
    for i in range(len(p_list)):
        c_list = p_list[i].getElementsByTagName('city')
        for j in range(len(c_list)):
            p_name = p_list[i]
            c_name = c_list[j]
            longitude = c_list[j].getAttribute('longitude')
            altitude = c_list[j].getAttribute('latitude')
            orm.insert(p_name, c_name, longitude, altitude)

        #    longitude_input = input('please enter the longtitude: ')
        #   altitude_input = input('please enter the altitude: ')
        #  orm.check(longitude_input, altitude_input)

    orm.finish()

if __name__ == '__main__':
    main()


