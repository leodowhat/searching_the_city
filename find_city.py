#!/usr/bin/python3
# -*- coding=utf-8 -*-
# date: 2017-12-5
import xml.dom.minidom
import pymysql
from os.path import dirname
from sqlalchemy import Column, String, create_engine, exc, orm, Integer, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
 
# 创建对象的基类:
Base = declarative_base()

# 定义城市对象:
class City(Base):
    # 表的名字:
    __tablename__ = 'city'

    # 表的结构:
    id = Column(Integer, primary_key=True, autoincrement = True)
    cname = Column(String(50))
    pname = Column(String(50))
    longitude = Column(String(20), index = True)
    altitude = Column(String(20), index = True)
# dsn = 'mysql+pymysql://{user}:{password}@{host}:{port}/{db}?charset={charset}'.format(
#         user = root,
#         host = localhost,
#         password ='',
#         db = test,
#         port = 3306,
#         charset = 'utf-8'),pool_size = 30,max_overflow = 0
dsn = 'mysql+pymysql://root:zhang@localhost:3306/test?charset=utf8'
#dsn = 'sqlite:///:memory:'
def main():
    try:
        orm = Test(dsn)#创建一个SQLAlchemyTest对象，将其用于所有的数据库操作
    except RuntimeError:
        print('ERROR: sql not supported or unreachable, exiting')
        return
    
    orm.insert()
    print('\n*** Insert citys into table completed!!!')

    orm.check()
    orm.finish()

class Test(object):
    def __init__(self, dsn):
        try:
            eng = create_engine(dsn,echo = True)
        except ImportError:
            raise RuntimeError()
            
        try:
            eng.connect()#尝试连接数据库
        except exc.OperationalError:
            print(''' please create database first.''')
            # eng = create_engine(dirname(dsn))
            # eng.execute('CREATE DATABASE test').close()
            # eng = create_engine(dsn)

        Base.metadata.drop_all(bind = eng)
        Base.metadata.create_all(bind = eng) 

        Session = orm.sessionmaker(bind=eng)
        self.ses = Session()
        self.city = City.__table__
        self.eng = self.city.metadata.bind = eng#引擎与表的元数据进行额外的绑定
        
    def insert(self):
        dom = xml.dom.minidom.parse('jinweiduxinxi.xml')
        root = dom.documentElement
        p_list = root.getElementsByTagName('provinces')
        for i in range(len(p_list)):
            c_list = p_list[i].getElementsByTagName('city')
            for j in range(len(c_list)):
                p_name = p_list[i].getAttribute('name')
                c_name = c_list[j].getAttribute('name')
                longitude = c_list[j].getAttribute('longitude')
                altitude = c_list[j].getAttribute('latitude')
#                self.ses.excute('INSERT INTO city (cname, pname, longitude, altitude) VALUES(c_name, p_name, longitude, altitude)')
                self.ses.add(City(cname = c_name, pname = p_name, longitude =longitude, altitude = altitude))
                self.ses.commit()

    def check(self):
        longitude_input = input('''please enter the longitude:''')
        altitude_input = input('''please enter the altitude:''')
        rs = self.ses.query(City).filter(and_(City.longitude == longitude_input, City.altitude == altitude_input)).all()
        if not rs:
            print('-'*30)
            print('''input error!''') 
        else:
            print('-'*30)
            for city in rs:
                print ('''the location you find is :''' +city.pname+city.cname)
                print('''the nearest city is:''' + city.min_distance_place)


    def finish(self):
       self.ses.connection().close()
       

    
#    longitude_input = input('please enter the longtitude: ')
 #   altitude_input = input('please enter the altitude: ')
  #  orm.check(longitude_input, altitude_input)
    
#    orm.finish()
    
if __name__ == '__main__':
    main()