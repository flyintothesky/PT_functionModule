from getProductcode import route_process

if __name__ == '__main__':
    # testcase
    test_route = ['业务授权交易业务', '(招商银行App7.0）信用卡授权数据实时接入需求_ST/投产1测试/ATMC/授权业务/业务授权交易业务/AMEX渠道交易/取现类交易']
    # 获取it_code
    ProductCode = route_process(test_route)
    print(ProductCode)