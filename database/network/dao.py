import uuid
class Dao:
    def __init__(self) -> None:
        import pymysql
    # 打开数据库连接
        self.conn = pymysql.connect(host='localhost',user = "simu",password = "szj0622@SZJ0419",db = "test")
    def close(self):
        # 关闭数据库连接
        self.conn.close()
    def save_graph(self, type, st,dimen):
        cursor = self.conn.cursor()
        try:
            #1. 检查是否存在该种网络类型，不存在就添加，并获取在表中的编号
            cursor.execute("select NET_TYPE_GUID FROM NET_TYPE WHERE NET_TYPE_NAME=%s", type)
            type_GUid = cursor.fetchone()
            if not type_GUid:
                type_GUid=uuid.uuid1()
                s="insert into NET_TYPE(NET_TYPE_GUID,NET_TYPE_NAME) VALUES('%s','%s')"%(type_GUid,type)
                cursor.execute(s)
                self.conn.commit()
            else:
                type_GUid = type_GUid[0]
            #2. 像网络表中插入新的记录，并获取其编号
            net_guid = uuid.uuid1().__str__()
            s="insert into NET(NET_GUID,NET_TYPE_GUID,NODE_NUM) VALUES('%s','%s',%d)"%(net_guid,type_GUid,dimen)
            cursor.execute(s)
            self.conn.commit()
            #3. 像网络边表中插入数据
            for i in st:
                edge_guid=uuid.uuid1().__str__()
                s="insert into NET_EDGE (EDGE_GUID,NET_GUID,S_ID,E_ID) VALUES('%s','%s',%d,%d)"%(edge_guid,net_guid,i[0],i[1])
                cursor.execute(s)
            self.conn.commit()
        except Exception as r:
            print(r)
        finally:
            cursor.close()
    #根据网络的GUID查询数据
    def load_graph(self, net_guid):
        cursor = self.conn.cursor()
        try:
            s="select NET_TYPE_NAME from NET_TYPE where NET_TYPE_GUID=(select NET_TYPE_GUID from NET where NET_GUID='%s' )"%net_guid
            cursor.execute(s)
            net_type=cursor.fetchone()[0]
            cursor.execute("select S_ID,E_ID from NET_EDGE WHERE NET_GUID='%s'"%net_guid)
            return cursor.fetchall(),net_type
        except Exception as r:
            print(r)
        finally:
            cursor.close()


'''
    def save_graph(self,table,st,append=False):
        # 1 覆盖、删除再存（没有就直接创建） 2 追加(没有就创建) 
        cursor = self.conn.cursor() 
        try:
            if not append:
                cursor.execute('drop table if exists '+table)
            cursor.execute('create table if not exists '+table+'(start int not null, end int not null)')
            s = cursor.executemany("insert into "+table+"(start, end) values(%s, %s)", st)
            self.conn.commit()
            print(s)
        except Exception as r:
            print(r)
        finally:
            cursor.close()
    def load_graph(self, table):
        cursor = self.conn.cursor() 
        try:
            cursor.execute('select * from '+table)
            return cursor.fetchall()
        except Exception as r:
            print(r)
        finally:
            cursor.close()
'''


# Dao().save_graph('nodes',[(1,14),(2,4)],False)
# print(Dao().load_graph('nodes'))