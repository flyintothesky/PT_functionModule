from dbConn import MySQLConn
import configparser


class DbService(object):

    _configParser = configparser.RawConfigParser()
    _configParser.read('sql.source')

    def __init__(self):
    	self._mySQLConn = MySQLConn()

    def selectTestdemandroute(self):
        _selectTestdemandrouteSQL = self._configParser.get('sql','selectTestdemandrouteSQL')
        try:
            return self._mySQLConn.fetchAll(_selectTestdemandrouteSQL, None)
        except Exception as e:
            print('Select Head failed, SQL->%s, params->%s' % (_selectTestdemandrouteSQL,None))
        else:
            pass
        finally:
            pass
    
    def selectTestcaseroute(self):
        _selectTestcaserouteSQL = self._configParser.get('sql','selectTestcaserouteSQL')
        try:
            return self._mySQLConn.fetchAll(_selectTestcaserouteSQL, None)
        except Exception as e:
            print('Select Head failed, SQL->%s, params->%s' % (_selectTestcaserouteSQL,None))
        else:
            pass
        finally:
            pass

    def selectProductcode(self,sysname):
        _selectProductcodeSQL = self._configParser.get('sql', 'selectProductcodeSQL')
        try:
            return self._mySQLConn.fetchAll(_selectProductcodeSQL,sysname)
        except Exception as e:
            print('Select Head failed, SQL->%s, params->%s' % (_selectProductcodeSQL,sysname))
        else:
            pass
        finally:
            pass
