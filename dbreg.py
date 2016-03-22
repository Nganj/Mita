#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Starlord
#
# Created:     01/06/2015
# Copyright:   (c) Starlord 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import _winreg as wreg
def addvalues(conn_name,host, db, user,passwd, port):
    key = wreg.CreateKey(wreg.HKEY_USERS, ".DEFAULT\\Software\\Mita")
##    wreg.SetValue(key, conn_name, wreg.REG_SZ, 'Default')
    key = wreg.CreateKey(wreg.HKEY_USERS, ".DEFAULT\\Software\\Mita"+'\\'+conn_name)
    wreg.SetValueEx(key, 'host', 1, wreg.REG_SZ, host)
    wreg.SetValueEx(key, 'dbname', 2, wreg.REG_SZ, db)
    wreg.SetValueEx(key, 'user', 3, wreg.REG_SZ, user)
    wreg.SetValueEx(key, 'password', 4, wreg.REG_SZ, passwd)
    wreg.SetValueEx(key, 'port', 5, wreg.REG_SZ, port)
##print  'Checking if db exists'
        #check if database is registered in registry
key = None
try:

            mainkey = wreg.OpenKey(wreg.HKEY_USERS, ".DEFAULT\\Software\\Mita", 0, wreg.KEY_ALL_ACCESS)
            main_conns = {}
            try:
                for y in range(10):
                    conn = wreg.EnumKey(mainkey, y)
                    main_conns[y] = conn
##                    print main_conns
            except Exception:
                pass
            key = wreg.OpenKey(wreg.HKEY_USERS, ".DEFAULT\\Software\\Mita\\"+main_conns[0], 0, wreg.KEY_ALL_ACCESS)
            mysql_conn = {}
            if key != None:
##                print 'found'
##                print wreg.QueryValueEx(key, 'port')

                for i in range(5):
                    h, v, o = wreg.EnumValue(key, i)
                    p = h, v
                    mysql_conn[h] = str(v)
##            print mysql_conn['user']
except Exception:
    if key != None:
        pass
##        print 'invalid query'
    else:
##        print 'this is a new installation, creating new key'
        addvalues('connection','192.168.43.116', 'Mita', 'admin','modulator', '3306')


