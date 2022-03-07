import uuid
import pymysql
import random

conn = pymysql.connect(host='localhost',user = "simu",password = "szj0622@SZJ0419",db = "test")
cursor = conn.cursor()
c_agent_num=500
for i in range(c_agent_num):
    age=random.randint(1,80)
    longitude=random.randint(1,100)
    latitude=random.randint(1,100)
    if age%2==0:
        gender='women'
    else:
        gender='men'
    guid=uuid.uuid1().__str__()
    cursor.execute("insert into AGENT(AGENT_GUID,GENDER,AGE,LONGITUDE,LATITUDE) VALUES ('%s','%s',%d,%d,%d)"
                   %(guid,gender,age,longitude,latitude))

conn.commit()
conn.close()