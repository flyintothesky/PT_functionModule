import re
from string import digits
from dataService import DbService
from cutWord import *
from config import *
from cal_sim import *


def split_route(test_route):
    '''
               正则方式切分测试路径
    '''
    # 正则表达式/\中的任何一个出现至少一次
    split_route = re.split('\\\\|/', test_route)
    # 返回已切分的测试路径
    return split_route

def split_name(test_name):
    '''
               正则方式切分测试名称
    '''
    # 正则表达式_-中的任何一个出现至少一次
    split_name = re.split('_|-', test_name)
    # 返回已切分的测试路径
    return split_name

def get_testroute_last_route(split_route, j):
    '''
               解析得到测试路径中模块的名称
             获取功能点后的字段
    '''
    last_route = []
    start = int(j) + 3
    end = int(j) + 4
    last_route = split_route[start] + split_route[end]
    last_route1 = list(cut_word(last_route))
    return last_route1


def get_testname_module_name(split_route):
     '''
             解析得到测试路径中模块的名称
     '''
     name_len = len(split_route)
     for i in range(name_len):
         if name_len <= 1:
            seg_name = list(cut_word(split_route[i]))
            return seg_name
         else:
            module = list(cut_word(split_route[i]))
            sub_module = list(cut_word(split_route[i + 1]))
            seg_name = module + sub_module
            return seg_name

def get_testroute_module_name(split_route, test_keyword, sys_keyword):
    '''
               解析得到测试路径中模块的名称
              通过自定义的关键字集合，去除噪音数据
    '''
    # 通过测试关键字过滤，默认其后的字段为系统字段，最后定位模块字段
    route_len = len(split_route)
    for i in range(route_len):
        # 得到切分字符串的list
        seg_route = list(cut_word(split_route[i]))
        # 与测试关键字(test_keyword)比对，统计是否包含测试关键字(test_keyword)
        test_result = (set(test_keyword).union(set(seg_route))) ^ (set(test_keyword) ^ set(seg_route))
        # 如不包含，长度为0
        if len(list(test_result)) == 0:
            # 模块
            module_route = list(cut_word(split_route[i + 1]))
            # 子模块
            sub_module_route = list(cut_word(split_route[i + 2]))
            # 合并模块和子模块
            combin_module_route = module_route + sub_module_route
            # 返回含模块名称的路径
            return combin_module_route, i, route_len

def get_testcaseroute_module_name(split_route, test_keyword, sys_keyword):
    '''
               解析得到测试路径中模块的名称
              通过自定义的关键字集合，去除噪音数据
    '''
    # 通过测试关键字过滤，默认其后的字段为系统字段，最后定位模块字段
    route_len = len(split_route)
    if route_len == 1:
        module_route=split_route
        i = 0
        return module_route, i, route_len
    else:   
        for i in range(route_len):
            # 得到切分字符串的list
            seg_route = list(cut_word(split_route[i]))
            # 与测试关键字(test_keyword)比对，统计是否包含测试关键字(test_keyword)
            test_result = (set(test_keyword).union(set(seg_route))) ^ (set(test_keyword) ^ set(seg_route))
            # 如不包含，长度为0
            if len(list(test_result)) == 0:
                # 模块
                module_route = list(cut_word(split_route[i + 1]))
                # 子模块
                sub_module_route = list(cut_word(split_route[i + 2]))
                # 合并模块和子模块
                combin_module_route = module_route + sub_module_route
                # 返回含模块名称的路径
                return combin_module_route, i, route_len

def occ_sim(target, source):
    '''
              计算解析出的模块名与实际模块名的相似度
              计算公式：相似度=相同词的个数/所有词的个数
    '''
    # 并集
    union_set = set(target).union(source)
    # 交集
    intersection_set = set(target) & set(source)
    # 相似度
    sim_score = (len(intersection_set)) / (len(union_set))
    # 返回值
    return sim_score

def testdemand_route_and_name_process():
    # 定义不同的相似度列表
    occ_sim_route_1 = []
    occ_sim_route_2 = []
    occ_sim_route_3 = []
    occ_sim_route_4 = []
    cos_sim_route_1 = []
    cos_sim_route_2 = []
    cos_sim_route_3 = []
    cos_sim_route_4 = []
    occ_sim_last_route_1 = []
    occ_sim_last_route_2 = []
    occ_sim_last_route_3 = []
    occ_sim_last_route_4 = []
    cos_sim_last_route_1 = []
    cos_sim_last_route_2 = []
    cos_sim_last_route_3 = []
    cos_sim_last_route_4 = []
    occ_sim_route_name_1 = []
    occ_sim_route_name_2 = []
    occ_sim_route_name_3 = []
    occ_sim_route_name_4 = []
    cos_sim_route_name_1 = []
    cos_sim_route_name_2 = []
    cos_sim_route_name_3 = []
    cos_sim_route_name_4 = []
    route_len_abnormal = []
    # 连接数据库
    dbService = DbService()
    # 读取数据库测试路径信息
    testdemands = dbService.selectTestdemandroute()
    print("==================== Evaluation of Test Demands is Begin ==============================")
    # 逐条读取路径数据
    for row in testdemands:
        # 获取路径信息
        testcase_route_source = row[1]
        # 判断路径是否为乱码
        r = '[^\w\u4e00-\u9fff]+'
        # 过滤符号字母
        testcase_route = re.sub(r, '', testcase_route_source)
        # 过滤数字
        remove_digits = str.maketrans('', '', digits)
        res = testcase_route.translate(remove_digits)
        #  路径不是乱码继续执行
        if res != '':
            # 获取测试需求路径信息
            target_split_route = split_route(row[1])
            # 解析出测试需求路径中的模块名
            target_moduleName, i, route_len = get_testroute_module_name(target_split_route, Config.test_keyword,
                                                                        Config.sys_keyword)
            # 获取测试需求名称
            target_split_name = split_name(row[2])
            # 解析测试名称中的模块名
            target_moduleName1 = get_testname_module_name(target_split_name)
            # 合并解析出路径中的模块名和解析测试名称中的模块名
            target_moduleName2 = target_moduleName + target_moduleName1
            # 从数据库读取模块信息
            source_moduleName = list(cut_word(row[0]))
            # 获取testtask
            testtask_id = row[3]
            # 判断路径长度，符合要求返回last路径，不符合返回空
            if route_len - i >= 6:
                target_last_route_name = get_testroute_last_route(target_split_route, i)
            else:
                target_last_route_name = ['']
                route_len_abnormal.append(testtask_id)
            # 计算相似度
            # 匹配相似度
            occ_sim_route_score = occ_sim(target_moduleName, source_moduleName)
            occ_sim_route_name_score = occ_sim(list(set(target_moduleName2)), source_moduleName)
            occ_sim_last_route_score = occ_sim(list(set(target_last_route_name)), source_moduleName)
            # 余弦相似度
            likelihood = Likelihood()
            cos_sim_route_score = likelihood.likelihood(target_moduleName, source_moduleName, punctuation=True)
            cos_sim_route_name_score = likelihood.likelihood(list(set(target_moduleName2)), source_moduleName, punctuation=True)
            cos_sim_last_route_score = likelihood.likelihood(list(set(target_last_route_name)), source_moduleName, punctuation=True)

        # 结果统计路径匹配相似度
        if 0 == occ_sim_route_score:
            occ_sim_route_1.append(occ_sim_route_score)
        elif 0 < occ_sim_route_score < 0.50:
            occ_sim_route_2.append(occ_sim_route_score)
        elif 0.50 <= occ_sim_route_score < 1:
            occ_sim_route_3.append(occ_sim_route_score)
        else:
            occ_sim_route_4.append(occ_sim_route_score)
        # 结果统计路径余弦相似度
        if 0 == cos_sim_route_score:
            cos_sim_route_1.append(cos_sim_route_score)
        elif 0 < cos_sim_route_score < 0.50:
            cos_sim_route_2.append(cos_sim_route_score)
        elif 0.50 <= cos_sim_route_score < 1:
            cos_sim_route_3.append(cos_sim_route_score)
        else:
            cos_sim_route_4.append(cos_sim_route_score)

            # 结果统计last路径匹配相似度
        if 0 == occ_sim_last_route_score:
            occ_sim_last_route_1.append(occ_sim_last_route_score)
        elif 0 < occ_sim_last_route_score < 0.50:
            occ_sim_last_route_2.append(occ_sim_last_route_score)
        elif 0.50 <= occ_sim_last_route_score < 1:
            occ_sim_last_route_3.append(occ_sim_last_route_score)
        else:
            occ_sim_last_route_4.append(occ_sim_last_route_score)
        # 结果统计last路径余弦相似度
        if 0 == cos_sim_last_route_score:
            cos_sim_last_route_1.append(cos_sim_last_route_score)
        elif 0 < cos_sim_last_route_score < 0.50:
            cos_sim_last_route_2.append(cos_sim_last_route_score)
        elif 0.50 <= cos_sim_last_route_score < 1:
            cos_sim_last_route_3.append(cos_sim_last_route_score)
        else:
            cos_sim_last_route_4.append(cos_sim_last_route_score)

            # 结果统计名称余弦相似度
        if 0 == occ_sim_route_name_score:
            occ_sim_route_name_1.append(occ_sim_route_name_score)
        elif 0 < occ_sim_route_name_score < 0.50:
            occ_sim_route_name_2.append(occ_sim_route_name_score)
        elif 0.50 <= occ_sim_route_name_score < 1:
            occ_sim_route_name_3.append(occ_sim_route_name_score)
        else:
            occ_sim_route_name_4.append(occ_sim_route_name_score)
        # 结果统计路径余弦相似度
        if 0 == cos_sim_route_name_score:
            cos_sim_route_name_1.append(cos_sim_route_name_score)
        elif 0 < cos_sim_route_name_score < 0.50:
            cos_sim_route_name_2.append(cos_sim_route_name_score)
        elif 0.50 <= cos_sim_route_name_score < 1:
            cos_sim_route_name_3.append(cos_sim_route_name_score)
        else:
            cos_sim_route_name_4.append(cos_sim_route_name_score)
        #    print(route_len_abnormal)
    # 打印路径评估结果
    print("======================= Final Test Demands Route Results 测试需求路径================================")
    print('测试需求路径匹配相似度：', '不相似:', len(occ_sim_route_1), '相似度低:', len(occ_sim_route_2), '相似度高:', len(occ_sim_route_3),
          '完全一样:', len(occ_sim_route_4))
    print('测试需求路径余弦相似度：', '不相似:', len(cos_sim_route_1), '相似度低:', len(cos_sim_route_2), '相似度高:', len(cos_sim_route_3),
          '完全一样:', len(cos_sim_route_4))
    print("==================== Evaluation Test Demands Route is Done 测试需求路径==============================")
    # 打印名称评估结果
    print("======================= Final Test Demands Route+Name Results 测试需求路径+名称================================")
    print('测试需求路径+测试需求名称匹配相似度：', '不相似:', len(occ_sim_route_name_1), '相似度低:', len(occ_sim_route_name_2), '相似度高:',
          len(occ_sim_route_name_3), '完全一样:', len(occ_sim_route_name_4))
    print('测试需求路径+测试需求名称余弦相似度：', '不相似:', len(cos_sim_route_name_1), '相似度低:', len(cos_sim_route_name_2), '相似度高:',
          len(cos_sim_route_name_3), '完全一样:', len(cos_sim_route_name_4))
    print("==================== Evaluation Test Demands Route+Name is Done 测试需求路径+名称==============================")
    # 打印last路径评估结果
    print("======================= Final Test Demands Last Route Results 测试需求结尾路径================================")
    print('测试需求路径匹配相似度：', '不相似:', len(occ_sim_last_route_1) - len(route_len_abnormal), '相似度低:',
          len(occ_sim_last_route_2), '相似度高:', len(occ_sim_last_route_3), '完全一样:', len(occ_sim_last_route_4), '路径长度不足:',
          len(route_len_abnormal))
    print('测试需求路径余弦相似度：', '不相似:', len(cos_sim_last_route_1) - len(route_len_abnormal), '相似度低:',
          len(cos_sim_last_route_2), '相似度高:', len(cos_sim_last_route_3), '完全一样:', len(cos_sim_last_route_4), '路径长度不足:',
          len(route_len_abnormal))
    print("==================== Evaluation Test Demands Last Route is Done 测试需求结尾路径==============================")
    print("==============================================================================================")

def testcase_route_and_name_process():
    # 定义不同的相似度列表
    occ_sim_route_1 = []
    occ_sim_route_2 = []
    occ_sim_route_3 = []
    occ_sim_route_4 = []
    cos_sim_route_1 = []
    cos_sim_route_2 = []
    cos_sim_route_3 = []
    cos_sim_route_4 = []
    occ_sim_last_route_1 = []
    occ_sim_last_route_2 = []
    occ_sim_last_route_3 = []
    occ_sim_last_route_4 = []
    cos_sim_last_route_1 = []
    cos_sim_last_route_2 = []
    cos_sim_last_route_3 = []
    cos_sim_last_route_4 = []
    occ_sim_route_name_1 = []
    occ_sim_route_name_2 = []
    occ_sim_route_name_3 = []
    occ_sim_route_name_4 = []
    cos_sim_route_name_1 = []
    cos_sim_route_name_2 = []
    cos_sim_route_name_3 = []
    cos_sim_route_name_4 = []
    route_len_abnormal = []
    # 连接数据库
    dbService = DbService()
    # 读取数据库测试路径信息
    testcases = dbService.selectTestcaseroute()
    print("==================== Evaluation of Test Cases is Begin ==============================")
    # 逐条读取路径数据
    for row in testcases:
        # 获取路径信息
        testcase_route_source = row[1]
        # 判断路径是否为乱码
        r = '[^\w\u4e00-\u9fff]+'
        # 过滤符号字母
        testcase_route = re.sub(r, '', testcase_route_source)
        # 过滤数字
        remove_digits = str.maketrans('', '', digits)
        res = testcase_route.translate(remove_digits)
        #  路径不是乱码继续执行
        if res != '':
            # 获取路径信息
            target_split_route = split_route(row[1])
            # 解析出路径中的模块信息
            target_moduleName, i, route_len = get_testcaseroute_module_name(target_split_route, Config.test_keyword,
                                                                        Config.sys_keyword)
            # 获取需求名称
            target_split_name = split_name(row[2])
            # 解析测试名称中的模块名
            target_moduleName1 = get_testname_module_name(target_split_name)
            # 合并解析出路径中的模块名和解析测试名称中的模块名
            target_moduleName2 = target_moduleName + target_moduleName1
            # 从数据库读取模块信息
            source_moduleName = list(cut_word(row[0]))
            # 获取testTask
            testtask_id = row[3]
            # 判断路径长度，符合要求返回last路径，不符合返回空
            if route_len - i >= 6:
                target_last_route_name = get_testroute_last_route(target_split_route, i)
            else:
                target_last_route_name = ['']
                route_len_abnormal.append(testtask_id)
            # 计算相似度
            # 匹配相似度
            occ_sim_route_score = occ_sim(target_moduleName, source_moduleName)
            occ_sim_route_name_score = occ_sim(list(set(target_moduleName2)), source_moduleName)
            occ_sim_last_route_score = occ_sim(list(set(target_last_route_name)), source_moduleName)
            # 余弦相似度
            likelihood = Likelihood()
            cos_sim_route_score = likelihood.likelihood(target_moduleName, source_moduleName, punctuation=True)
            cos_sim_route_name_score = likelihood.likelihood(list(set(target_moduleName2)), source_moduleName, punctuation=True)
            cos_sim_last_route_score = likelihood.likelihood(list(set(target_last_route_name)), source_moduleName, punctuation=True)

        # 结果统计路径匹配相似度
        if 0 == occ_sim_route_score:
            occ_sim_route_1.append(occ_sim_route_score)
        elif 0 < occ_sim_route_score < 0.50:
            occ_sim_route_2.append(occ_sim_route_score)
        elif 0.50 <= occ_sim_route_score < 1:
            occ_sim_route_3.append(occ_sim_route_score)
        else:
            occ_sim_route_4.append(occ_sim_route_score)
        # 结果统计路径余弦相似度
        if 0 == cos_sim_route_score:
            cos_sim_route_1.append(cos_sim_route_score)
        elif 0 < cos_sim_route_score < 0.50:
            cos_sim_route_2.append(cos_sim_route_score)
        elif 0.50 <= cos_sim_route_score < 1:
            cos_sim_route_3.append(cos_sim_route_score)
        else:
            cos_sim_route_4.append(cos_sim_route_score)

        # 结果统计last路径匹配相似度
        if 0 == occ_sim_last_route_score:
            occ_sim_last_route_1.append(occ_sim_last_route_score)
        elif 0 < occ_sim_last_route_score < 0.50:
            occ_sim_last_route_2.append(occ_sim_last_route_score)
        elif 0.50 <= occ_sim_last_route_score < 1:
            occ_sim_last_route_3.append(occ_sim_last_route_score)
        else:
            occ_sim_last_route_4.append(occ_sim_last_route_score)
        # 结果统计last路径余弦相似度
        if 0 == cos_sim_last_route_score:
            cos_sim_last_route_1.append(cos_sim_last_route_score)
        elif 0 < cos_sim_last_route_score < 0.50:
            cos_sim_last_route_2.append(cos_sim_last_route_score)
        elif 0.50 <= cos_sim_last_route_score < 1:
            cos_sim_last_route_3.append(cos_sim_last_route_score)
        else:
            cos_sim_last_route_4.append(cos_sim_last_route_score)

        # 结果统计名称匹配相似度
        if 0 == occ_sim_route_name_score:
            occ_sim_route_name_1.append(occ_sim_route_name_score)
        elif 0 < occ_sim_route_name_score < 0.50:
            occ_sim_route_name_2.append(occ_sim_route_name_score)
        elif 0.50 <= occ_sim_route_name_score < 1:
            occ_sim_route_name_3.append(occ_sim_route_name_score)
        else:
            occ_sim_route_name_4.append(occ_sim_route_name_score)
        # 结果统计路径余弦相似度
        if 0 == cos_sim_route_name_score:
            cos_sim_route_name_1.append(cos_sim_route_name_score)
        elif 0 < cos_sim_route_name_score < 0.50:
            cos_sim_route_name_2.append(cos_sim_route_name_score)
        elif 0.50 <= cos_sim_route_name_score < 1:
            cos_sim_route_name_3.append(cos_sim_route_name_score)

        else:
            cos_sim_route_name_4.append(cos_sim_route_name_score)
        #    print(route_len_abnormal)
    # 打印路径评估结果
    print("======================= Final Test Cases Route Results 测试案例路径 ================================")
    print('测试案例路径匹配相似度：', '不相似:', len(occ_sim_route_1), '相似度低:', len(occ_sim_route_2), '相似度高:', len(occ_sim_route_3),
          '完全一样:', len(occ_sim_route_4))
    print('测试案例路径余弦相似度：', '不相似:', len(cos_sim_route_1), '相似度低:', len(cos_sim_route_2), '相似度高:', len(cos_sim_route_3),
          '完全一样:', len(cos_sim_route_4))
    print("==================== Evaluation Test Cases Route is Done 测试案例路径==============================")
    # 打印名称评估结果
    print("======================= Final Test Cases Route+Name Results 测试案例路径+名称================================")
    print('测试案例路径+测试案例名称匹配相似度：', '不相似:', len(occ_sim_route_name_1), '相似度低:', len(occ_sim_route_name_2), '相似度高:',
          len(occ_sim_route_name_3), '完全一样:', len(occ_sim_route_name_4))
    print('测试案例路径+测试案例名称余弦相似度：', '不相似:', len(cos_sim_route_name_1), '相似度低:', len(cos_sim_route_name_2), '相似度高:',
          len(cos_sim_route_name_3), '完全一样:', len(cos_sim_route_name_4))
    print("==================== Evaluation Test Cases Route+Name is Done 测试案例路径+名称==============================")
    # 打印last路径评估结果
    print("======================= Final Test Demands Last Route Results 测试案例结尾路径================================")
    print('测试需求路径匹配相似度：', '不相似:', len(occ_sim_last_route_1) - len(route_len_abnormal), '相似度低:',
          len(occ_sim_last_route_2), '相似度高:', len(occ_sim_last_route_3), '完全一样:', len(occ_sim_last_route_4), '路径长度不足:',
          len(route_len_abnormal))
    print('测试需求路径余弦相似度：', '不相似:', len(cos_sim_last_route_1) - len(route_len_abnormal), '相似度低:',
          len(cos_sim_last_route_2), '相似度高:', len(cos_sim_last_route_3), '完全一样:', len(cos_sim_last_route_4), '路径长度不足:',
          len(route_len_abnormal))
    print("==================== Evaluation Test Demands Last Route is Done 测试案例结尾路径==============================")


if __name__ == '__main__':
    '''
    demand_route_and_name_process：根据测试需求分析评估
    testcase_route_and_name_process：据测试案例分析评估
    '''
    testdemand_route_and_name_process()
    testcase_route_and_name_process()
