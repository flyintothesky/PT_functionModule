class Config():
    '''
              自定义配置过滤的关键词
              用于过滤测试路径中与模块名称无关的信息
             可根据需求自行添加
    '''
    # 测试关键字：test_keyword
    test_keyword = ['_ST', '投产1', '投产2', 'uat案例 ', 'st案例']
    # 系统关键字：sys_keyword
    sys_keyword =['平台', '系统', '网站']