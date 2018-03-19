#!/usr/bin/python3
# -*- coding=utf-8 -*-
# date: 2017-12-5
import xml.dom.minidom
#import pymsql
from os.path import dirname
from sqlalchemy import Column, String, create_engine, orm, Integer, and_,update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from math import sin, asin, cos, radians, fabs, sqrt

from datetime import datetime 
  
# 创建对象的基类:
Base = declarative_base()

# 定义城市对象:
class City(Base):
    # 表的名字:
    __tablename__ = 'city'

    # 表的结构:
    id = Column(Integer, primary_key=True, autoincrement = True)
    cname = Column(String(20))
    pname = Column(String(20))
    longitude = Column(String(20))
    altitude = Column(String(20))
    distance = Column(String(20))

dsn = 'mysql+pymysql://root:zhang@localhost:3306/test?charset=utf8'
#dsn = 'sqlite:///:memory:'
def main():
    try:
        orm = Test(dsn)#创建一个SQLAlchemyTest对象，将其用于所有的数据库操作
    except RuntimeError:
        print('ERROR: sql not supported or unreachable, exiting')
        return
    t1 = datetime.now().timestamp()
    orm.insert()
    t2 = datetime.now().timestamp()
    print('\n*** Insert citys into table completed!!!')
    print('\n*** time used is:' + str(t2-t1)+'s')

    orm.check()
    orm.finish()
######################################################################

EARTH_RADIUS = 6371           # 地球平均半径，6371km     
def hav(theta):  
    s = sin(theta / 2)  
    return s * s  
   
def get_distance_hav(lat0, lng0, lat1, lng1):  
    "用haversine公式计算球面两点间的距离。"  
    # 经纬度转换成弧度

    lat0 = radians(float(lat0))  
    lat1 = radians(float(lat1))  
    lng0 = radians(float(lng0))
    lng1 = radians(float(lng1))
   
    dlng = fabs(lng0 - lng1)  
    dlat = fabs(lat0 - lat1)  
    h = hav(dlat) + cos(lat0) * cos(lat1) * hav(dlng)  
    distance = 2 * EARTH_RADIUS * asin(sqrt(h))  
   
    return distance
#########################################################################
class Test(object):
    def __init__(self, dsn):
        try:
            eng = create_engine(dsn)
        except ImportError:
            raise RuntimeError()
            
        try:
            eng.connect()#尝试连接数据库
        except exc.OperationalError:
            eng = create_engine(dirname(dsn))
            eng.excute('CREATE DATABASE test').close()
            eng = create_engine(dsn)

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
                self.ses.add(City(cname = c_name, pname = p_name, longitude =longitude, altitude = altitude))
                self.ses.commit()

    def check(self):
        longitude_input = input('''please enter the longitude:''')
        altitude_input = input('''please enter the altitude:''')

        t3 = datetime.now().timestamp()

        rs1 = self.ses.query(City).filter(and_(City.longitude == longitude_input, City.altitude == altitude_input)).all()
        if not rs1:
            print('-'*30)
            print('''input error!''') 
        else:
            print('-'*30)
            for city in rs1:
                print ('''the location you find is :''' +city.pname+city.cname)

                t4 = datetime.now().timestamp()
                print('\n*** time used is:' + str(t4-t3)+'s')

                rs2 = self.ses.query(City).all()
                t5 = datetime.now().timestamp()
                for city in rs2:
                    id_iter = city.id
                    print(city.cname+'is calculating!!!')
                    distance_iter = float(get_distance_hav(altitude_input, longitude_input, city.altitude, city.longitude))
                    # self.ses.execute('UPDATE city SET city.distance = distance_iter Where city.id = id_iter')
                    self.ses.query(City).filter(City.id == id_iter).update({"distance" : distance_iter})
                    self.ses.commit()
                    # self.ses.execute(city.update().where(city.id == id_iter).values(distance = distance_iter))
                t6 = datetime.now().timestamp()
                print('\n*** time used for finding is:' + str(t6-t5)+'s')
                rs3 = self.ses.query(City).order_by((-City.distance).desc()).all()
                print('''the nearest city is:''' +rs3[1].pname+rs3[1].cname+'. the distance is:'+rs3[1].distance+'km.')
                t7 = datetime.now().timestamp()
                print('\n*** time used for ordering is:' + str(t7-t6)+'s')

    def finish(self):
       self.ses.connection().close()
    
if __name__ == '__main__':
    main()