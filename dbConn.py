import pymysql
import configparser

class MySQLConn(object):
    """docstring for MySQLConn"""

    _configParser = configparser.SafeConfigParser()
    _configParser.read('sql.source')

    def __init__(self):
        try:
            self._host = self._configParser.get('database','host')
            self._port = self._configParser.getint('database','port')
            self._user = self._configParser.get('database','user')
            self._passwd = self._configParser.get('database','passwd')
            self._dbname = self._configParser.get('database','dbname')
            self._charset = self._configParser.get('database','charset')
            self._conn = pymysql.connect(host=self._host,user=self._user,passwd=self._passwd,db=self._dbname,port=self._port,charset=self._charset)
            self._cursor = self._conn.cursor()
        except Exception as e:
            print("Mysqldb Error:%s" % e)
        else:
            print("Create MySQL database connection successfull...")
        finally:
            pass

    def executeOne(self,sql,params):
        try:
            self._cursor.execute(sql,params)
            self._conn.commit()
        except Exception as e:
            print("Mysqldb Error:%s" % e)
            print("Execute SQL: %s with params: %s failed..." % (sql, params))
            self._conn.rollback()
        else:
            print("Execute SQL: %s with params: %s successfull..." % (sql, params))
            pass
        finally:
            pass

    def fetchAll(self,sql,params):
        try:
            self._cursor.execute(sql,params)
            return self._cursor.fetchall()
        except Exception as e:
            print("Mysqldb Error:%s" % e)
            print("Execute SQL: %s with params: %s failed..." % (sql, params))
        else:
            #print "Execute SQL: %s with params: %s successfull..." % (sql, params)
            pass
        finally:
            pass
        
    def fetchONE(self,sql,params):
        try:
            self._cursor.execute(sql,params)
            return self._cursor.fetchone()
        except Exception as e:
            print("Mysqldb Error:%s" % e)
            print("Execute SQL: %s with params: %s failed..." % (sql, params))
        else:
            #print "Execute SQL: %s with params: %s successfull..." % (sql, params)
            pass
        finally:
            pass

    def __del__(self):
        try:
            self._cursor.close()
            self._conn.close()
        except Exception as e:
            print("Mysqldb Error:%s" % e)
            print("Close MySQL database connection failed...")
        else:
            print("Close MySQL database connection successfull...")
        finally:
            pass
