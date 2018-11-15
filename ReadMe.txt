1、使用环境：
Python3.6

2、扩展包（Python Extension Packages内有安装文件）：
jieba：文本处理，CMD进入所在文件夹，运行python setup.py install
pymysql：数据库连接，CMD进入所在文件夹，运行pip install xxxxx.whl
configparser：解析配置文件，CMD进入所在文件夹，运行pip install xxxxx.whl

3、文件结构
----PT-functionModuleV1.0文件夹
|-----config.py 配置关键字，用于过滤测试、系统等噪声数据（可修改）
|-----cal_sim.py 计算相似度类（不可修改）
|-----dataService.py 封装的数据服务接口（不可修改）
|-----dbConn.py 封装的数据库连接接口（不可修改）
|-----cutWord.py 封装的分词接口（不可修改）
|-----main.py 主程序，执行该文件
|-----sql.source 数据库连接配置信息（可修改）和SQL语句
|-----dicts（文件夹）jieba分词调用 
   |-----custom_words.txt 自定义词库（可修改）
   |-----stop_words.txt
   |-----synonym.txt
|-----Python Extension Packages（文件夹） 提供程序运行所需扩展包
   |-----jieba（文件夹）
   |-----configparser-3.5.0-py3-none-any.whl
   |-----PyMySQL-0.9.2-py2.py3-none-any.whl

修改sql.source数据库连接配置信息，保证程序可以正常访问数据库，并读取所需信息。
|----------------------|
|[database]            |
|host = xxx.xxx.xxx.xxx|
|port = 3306           |
|user = xxxx           |
|passwd = xxxx         |
|dbname = fpplatform   | 
|charset = utf         |
|----------------------|   

4、运行方式
环境和扩展包都安装好后，可使用CMD进入所在文件夹，运行python main.py，就会解析测试需求的路径和名称、测试案例的路径和名称，并计算与实际模块名称的相似度。
相似度：1）匹配相似度；2）余弦相似度
  相似度=0:        不相似
  0<相似度<50%:    相似度低
  50%<=相似度<100%:相似度高
  相似度=100%:     完全一样

例子：运行信息输出如下：
Create MySQL database connection successfull...
==================== Evaluation of Test Demands is Begin ==============================
======================= Final Test Demands Route Results ================================
测试需求路径匹配相似度： 不相似: 1 相似度低: 0 相似度高: 0 完全一样: 0
测试需求路径余弦相似度： 不相似: 1 相似度低: 0 相似度高: 0 完全一样: 0
==================== Evaluation Test Demands Route is Done ==============================
======================= Final Test Demands Route+Name Results ================================
测试需求路径+测试需求名称匹配相似度： 不相似: 1 相似度低: 0 相似度高: 0 完全一样: 0
测试需求路径+测试需求名称余弦相似度： 不相似: 1 相似度低: 0 相似度高: 0 完全一样: 0
==================== Evaluation Test Demands Route+Name is Done ==============================
======================= Final Test Demands Last Route Results ================================
测试需求路径匹配相似度： 不相似: 1 相似度低: 0 相似度高: 0 完全一样: 0
测试需求路径余弦相似度： 不相似: 1 相似度低: 0 相似度高: 0 完全一样: 0
==================== Evaluation Test Demands Last Route is Done ==============================
==============================================================================================
Close MySQL database connection successfull...
Create MySQL database connection successfull...
==================== Evaluation of Test Cases is Begin ==============================
======================= Final Test Cases Route Results ================================
测试案例路径匹配相似度： 不相似: 0 相似度低: 0 相似度高: 1 完全一样: 0
测试案例路径余弦相似度： 不相似: 0 相似度低: 0 相似度高: 2 完全一样: 0
==================== Evaluation Test Cases Route is Done ==============================
======================= Final Test Cases Route+Name Results ================================
测试案例路径+测试案例名称匹配相似度： 不相似: 0 相似度低: 0 相似度高: 1 完全一样: 0
测试案例路径+测试案例名称余弦相似度： 不相似: 0 相似度低: 0 相似度高: 1 完全一样: 0
==================== Evaluation Test Cases Route+Name is Done ==============================
======================= Final Test Demands Last Route Results ================================
测试需求路径匹配相似度： 不相似: 1 相似度低: 0 相似度高: 0 完全一样: 0
测试需求路径余弦相似度： 不相似: 1 相似度低: 0 相似度高: 0 完全一样: 0
==================== Evaluation Test Demands Last Route is Done ==============================
Close MySQL database connection successfull...


5、遇到问题
如遇到问题可及时反馈解决。
遇到问题可能涉及数据库连接，数据表读取，数据格式等。



