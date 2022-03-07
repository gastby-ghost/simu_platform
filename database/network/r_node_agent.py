import uuid
import pymysql
import random

conn = pymysql.connect(host='localhost',user = "simu",password = "szj0622@SZJ0419",db = "test")
cursor = conn.cursor()

net_guid='e0a658a5-6884-11ec-828f-61e8c2066380'
model_bdi_guid='5ef5dc15-6887-11ec-82e9-9822eff6f6cd'
#默认个体是个体集中前多少个个体，否则数量一多太难查询了
#1. 查询网络中有多少个节点
s="SELECT NODE_NUM FROM NET WHERE NET_GUID='%s'"%net_guid
cursor.execute(s)
node_num=cursor.fetchone()[0]
#2. 查询节点数的个体
s="SELECT AGENT_GUID FROM AGENT LIMIT %d"%node_num
cursor.execute(s)
agent_guid_list=list(cursor.fetchall())
#3. 按顺序插入关系
id=0
for i in agent_guid_list:
    cursor.execute("INSERT INTO NET_AGENT_R(NAR_GUID,NET_GUID,AGENT_GUID,NODE_ID)"
                   "VALUES (UUID(),'%s','%s',%d)"%(net_guid,i[0],id))
    #插入bdi参数
    belief=random.randint(1,10)
    cursor.execute("INSERT INTO PA_BDI_AGENT(PA_BDI_AGENT_GUID,AGENT_GUID,MODEL_PA_BDI_GUID,BELIEF)"
                   "VALUES (UUID(),'%s','%s',%d)"%(i[0],model_bdi_guid,belief))
    id+=1
conn.commit()
conn.close()