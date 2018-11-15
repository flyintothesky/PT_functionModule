import re
from dataService import DbService
from cutWord import *
from config import *


def split_route(test_route):
    '''
    正则方式切分测试路径
    :param test_route
    :return: split_route
    '''
    # 正则表达式/\中的任何一个出现至少一次
    split_route = re.split('\\\\|/', test_route)
    # 返回已切分的测试路径
    return split_route

def parse_testroute_sysname(split_route, test_keyword):
    '''
    解析得到测试路径中系统的名称
    通过自定义的关键字集合，去除噪音数据
    :param split_route, test_keyword
    :return: sys_route
    '''
    # 通过测试关键字过滤，默认其后的字段为系统字段，最后定位模块字段
    route_len = len(split_route)
    if route_len == 1:
        sys_route = split_route
        i = 0
        return sys_route, i, route_len
    else:
        for i in range(route_len):
            # 得到切分字符串的list
            seg_route = list(cut_word(split_route[i]))
            # 与测试关键字(test_keyword)比对，统计是否包含测试关键字(test_keyword)
            test_result = (set(test_keyword).union(set(seg_route))) ^ (set(test_keyword) ^ set(seg_route))
            # 如不包含关键字，长度为0
            if len(list(test_result)) == 0:
                # 系统路径
                sys_route = split_route[i]
                # 返回系统路径
                return sys_route

def route_process(test_route):
    '''
    解析测试路径中的系统名称并匹配对应的productcode（一对多的关系）
    :param test_route:
    :return: productcode
    '''
    print("==================== Parse Test Route is Begin ==============================")
    # 获取路径信息
    test_route_source = test_route[1]
    # 获取测试需求路径信息
    target_split_route = split_route(test_route_source)
    # 解析出测试路径中的系统名称
    target_sysName = parse_testroute_sysname(target_split_route, Config.test_keyword)
    # 连接数据库
    dbService = DbService()
    # 读取数据库测试路径信息
    productcodes = dbService.selectProductcode(target_sysName)
    it_codes = []
    # 判断是否获取到数据库返回信息
    if len(productcodes) != 0:
       # 获取从数据库查询的所有结果
       for productcode in productcodes:
           productcode = productcode[0]
           it_codes.append(productcode)
       return it_codes
    # 数据库查询无返回
    else:
        productcode = '无对应的ProductCode'
        return productcode
    print("==================== Parse Test Route is Done ==============================")


if __name__ == '__main__':
    # 获取it_code
    ProductCode = route_process(test_route)