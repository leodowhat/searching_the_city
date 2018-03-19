from math import sin, asin, cos, radians, fabs, sqrt

import xml.dom.minidom

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


def get_nearest_city_id(local_city_id):

    global longitude_list, altitude_list, pname_list, cname_list
    longitude_list = []
    altitude_list = []
    pname_list = []
    cname_list = []
    distance_list = []

    dom = xml.dom.minidom.parse('jinweiduxinxi.xml')
    root = dom.documentElement
    p_list = root.getElementsByTagName('provinces')
    for i in range(len(p_list)):
        c_list = p_list[i].getElementsByTagName('city')
        for j in range(len(c_list)):
            pname_list.append(p_list[i].getAttribute('name'))
            cname_list.append(c_list[j].getAttribute('name'))
            longitude_list.append(c_list[j].getAttribute('longitude'))
            altitude_list.append(c_list[j].getAttribute('latitude'))

    # if len(pname_list) == len(cname_list) :
    #     sum_city = len(pname_list)
    #     print(sum_city)
    # if len(longitude_list) == len(altitude_list) :
    #     sum_city = len(altitude_list)
    #     print(sum_city)
    # else:
    #     print('XML解析错误！')

    sum_city = len(cname_list)
    for i in range(sum_city):
        # print(i)
        distance_list.append(get_distance_hav(altitude_list[local_city_id], longitude_list[local_city_id],
                                              altitude_list[i], longitude_list[i]))

    distance_list.remove(0)
    return distance_list.index(min(distance_list)) + 1
    # 返回第一个匹配的最小值索引，暂不考虑有多个极值的情况


# a = get_nearest_city_id(100)
# x = cname_list.index('青岛')
# print (x)
# y = get_nearest_city_id(x+1)
# print(y)
    global longitude_list, altitude_list, pname_list, cname_list
    longitude_list = [], altitude_list = []
    pname_list = [], cname_list = []

    dom = xml.dom.minidom.parse('jinweiduxinxi.xml')
    root = dom.documentElement
    p_list = root.getElementsByTagName('provinces')
    for i in range(len(p_list)):
        c_list = p_list[i].getElementsByTagName('city')
        for j in range(len(c_list)):
            pname_list.append(p_list[i].getAttribute('name'))
            cname_list.append(c_list[j].getAttribute('name'))
            longitude_list.append(c_list[j].getAttribute('longitude'))
            altitude_list.append(c_list[j].getAttribute('latitude'))
    if len(pname_list) == len(cname_list) == len(longitude_list) = len(altitude_list):
        sum_city = len(pname)
    else:
        print('XML解析错误！')

    distance_list = []
    for i in sum_city:
        distance_list[i] = get_distance_hav(altitude_list[local_city_id], longitude[local_city_id], /
                                            altitude_list[i], longitude[i])
    return distance_list.index(min(distance_list.remove(0)))
