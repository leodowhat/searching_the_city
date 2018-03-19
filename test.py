#!/usr/bin/python3
# -*- coding=utf-8 -*-
# date: 2017-12-8
import xml.dom.minidom

from os.path import dirname
from sqlalchemy import Column, String, create_engine, orm, Integer, and_, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from math import sin, asin, cos, radians, fabs, sqrt

from datetime import datetime


Base = declarative_base()


class City(Base):
    # 表的名字:
    __tablename__ = 'city'

    # 表的结构:
    id = Column(Integer, primary_key=True, autoincrement=True)
    cname = Column(String(20))
    pname = Column(String(20))
    longitude = Column(String(20))
    altitude = Column(String(20))

# 解析ＸＭＬ文件：
longitude_list = []
altitude_list = []
pname_list = []
cname_list = []
distance_list = []
dom = xml.dom.minidom.parse('jinweiduxinxi.xml')
root = dom.documentElemen
p_list = root.getElementsByTagName('provinces')
for i in range(len(p_list)):
    c_list = p_list[i].getElementsByTagName('city')
    for j in range(len(c_list)):
        pname_list.append(p_list[i].getAttribute('name'))
        cname_list.append(c_list[j].getAttribute('name'))
        longitude_list.append(c_list[j].getAttribute('longitude'))
        altitude_list.append(c_list[j].getAttribute('latitude'))


# 经纬度距离计算


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
    distance = 2 * 6371 * asin(sqrt(h))

    return distance


def get_nearest_city_id(local_city_id, longitude_list, altitude_list, pname_list, cname_list, sum_city):
    # 最近城市排序
    sum_city = len(cname_list)
    for i in range(sum_city):
        # print(i)
        distance_list.append(get_distance_hav(altitude_list[local_city_id], longitude_list[local_city_id],
                                              altitude_list[i], longitude_list[i]))
    distance_list.remove(0)
    min_distance = min(distance_list)
    return distance_list.index(min_distance) + 1, min_distance


def main():

    dsn = 'mysql+pymysql://root:zhang@localhost:3306/test?charset=utf8'
    #dsn = 'sqlite:///:memory:'

    try:
        orm = Test(dsn)
    except RuntimeError:
        print('ERROR: sql not supported or unreachable, exiting')
        return
    t1 = datetime.now().timestamp()
    orm.insert()
    t2 = datetime.now().timestamp()
    print('\n*** Insert citys into table completed!!!')
    print('\n*** time used is:' + str(t2 - t1) + 's')

    orm.check()
    orm.finish()


class Test(object):

    def __init__(self, dsn):
        try:
            eng = create_engine(dsn)
        except ImportError:
            raise RuntimeError()

        try:
            eng.connect()  # 尝试连接数据库
        except exc.OperationalError:
            eng = create_engine(dirname(dsn))
            eng.excute('CREATE DATABASE test').close()
            eng = create_engine(dsn)

        Base.metadata.drop_all(bind=eng)
        Base.metadata.create_all(bind=eng)

        Session = orm.sessionmaker(bind=eng)
        self.ses = Session()
        self.city = City.__table__
        self.eng = self.city.metadata.bind = eng  # 引擎与表的元数据进行额外的绑定

    def insert(self):
        # sum_city = len(cname_list)
        # 使用global可以访问到全局变量
        global longitude_list
        global altitude_list
        global pname_list
        global cname_list
        sum_city = len(cname_list)
        for i in range(sum_city):
            self.ses.add(City(cname=cname_list[i], pname=pname_list[i],
                              longitude=longitude_list[i], altitude=altitude_list[i]))
            self.ses.commit()

    def check(self):
        global longitude_list
        global altitude_list
        global pname_list
        global cname_list
        sum_city = len(cname_list)

        longitude_input = input('''please enter the longitude:''')
        altitude_input = input('''please enter the altitude:''')

        t3 = datetime.now().timestamp()

        rs1 = self.ses.query(City).filter(
            and_(City.longitude == longitude_input, City.altitude == altitude_input)).all()
        if not rs1:
            print('-' * 30)
            print('''input error!''')
        else:
            print('-' * 30)
            for city in rs1:
                print ('''the location you find is :''' +
                       city.pname + city.cname)

                t4 = datetime.now().timestamp()
                print('\n*** time used for finding the local city is:' +
                      str(t4 - t3) + 's')

                local_city_id = cname_list.index(city.cname)
                nearest_city_id, nearest_city_distance = get_nearest_city_id(
                    local_city_id, longitude_list, altitude_list, pname_list, cname_list, sum_city)
                print('''the nearest city is:''' + str(pname_list[nearest_city_id]) +
                      str(cname_list[nearest_city_id]) + '. the distance is:' + str(nearest_city_distance) + 'km.')
                t5 = datetime.now().timestamp()
                print('\n*** time used for finding the nearest city is:' +
                      str(t5 - t4) + 's')

    def finish(self):
        self.ses.connection().close()

if __name__ == '__main__':
    main()
