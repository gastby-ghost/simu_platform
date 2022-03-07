-- 数据库文档：用于创建表
-- UTF-8
-- 单洲君

-- 清除所有的已有表更新数据       
SET FOREIGN_KEY_CHECKS=0;       
DROP TABLE IF EXISTS SCH;   
DROP TABLE IF EXISTS AGENT;     
DROP TABLE IF EXISTS AGENT_SET;     
DROP TABLE IF EXISTS AGENT_SET_R;    
DROP TABLE IF EXISTS NET_TYPE;                    
DROP TABLE IF EXISTS NET;       
DROP TABLE IF EXISTS NET_AGENT_R;   
DROP TABLE IF EXISTS NET_EDGE;      
DROP TABLE IF EXISTS PA_BDI;  
DROP TABLE IF EXISTS PA_BDI_RULER; 
DROP TABLE IF EXISTS PA_BDI_MODEL_RULER_R;   
DROP TABLE IF EXISTS PA_BDI_AGENT;              
DROP TABLE IF EXISTS AGENT_SPREAD;     
SET FOREIGN_KEY_CHECKS=1;

-- 方案(SCH)
CREATE TABLE SCH
(
    SCH_GUID        VARCHAR(50) NOT NULL  ,
    SCH_NAME        VARCHAR(50) NOT NULL,
    SCH_CREATE_TIME DATE        NOT NULL,
    SCH_AIM         VARCHAR(150)    NULL,
    SCH_CREATE_ROLE VARCHAR(50)     NULL,
    SCH_REMARK      TEXT            NULL,
    PRIMARY KEY (SCH_GUID)
);

-- 个体(AGENT)
CREATE TABLE AGENT
(
    AGENT_GUID      VARCHAR(50)         NOT NULL  ,
    GENDER          VARCHAR(10)             NULL,
    AGE             INT                     NULL,
    EDU_LEVEL_GUID  VARCHAR(50)             NULL,
    PSYCHOLOGY_GUID VARCHAR(50)             NULL,
    OCCUPATION_GUID VARCHAR(50)             NULL,
    ECONOMY_GUID    VARCHAR(50)             NULL,
    BEHAVE_GUID     VARCHAR(50)             NULL,
    LONGITUDE       INT             NULL,
    LATITUDE        INT             NULL,
    PRIMARY KEY (AGENT_GUID)
);

-- 个体集合(AGENT_SET)
CREATE TABLE AGENT_SET
(
    SET_GUID          VARCHAR(50)         NOT NULL  ,
    SCH_GUID          VARCHAR(50)             NULL,
    SET_REMARK      TEXT            NULL,
    PRIMARY KEY (SET_GUID),
    FOREIGN KEY (SCH_GUID) REFERENCES SCH(SCH_GUID)
);

-- 个体集合归属关系(AGENT_SET_R)
CREATE table AGENT_SET_R
(
    ASR_GUID          VARCHAR(50)         NOT NULL  ,
    SET_GUID          VARCHAR(50)         NOT NULL,
    AGENT_GUID        VARCHAR(50)         NOT NULL,
    PRIMARY KEY (ASR_GUID),
    FOREIGN KEY (SET_GUID) REFERENCES AGENT_SET(SET_GUID),
    FOREIGN KEY (AGENT_GUID) REFERENCES AGENT(AGENT_GUID)
);

-- 网络类型(NET_TYPE)
CREATE TABLE NET_TYPE
(
    NET_TYPE_GUID     VARCHAR(50)         NOT NULL  ,
    NET_TYPE_NAME   VARCHAR(50) NOT NULL,
    NET_TYPE_REMARK TEXT            NULL,
    PRIMARY KEY (NET_TYPE_GUID)
);

-- 网络(NET)
CREATE TABLE NET
(
    NET_GUID          VARCHAR(50)         NOT NULL  ,
    NET_TYPE_GUID     VARCHAR(50)         NOT NULL,
    NODE_NUM            INT                 NOT NULL,
    SCH_GUID          VARCHAR(50)             NULL,
    NET_REMARK      TEXT            NULL,
    PRIMARY KEY (NET_GUID),
    FOREIGN KEY (NET_TYPE_GUID) REFERENCES NET_TYPE(NET_TYPE_GUID),
    FOREIGN KEY (SCH_GUID) REFERENCES SCH(SCH_GUID)
);


-- 个人网络关系表(NET_AGENT_R)
-- 这个似乎得改一下
CREATE TABLE NET_AGENT_R
(
    NAR_GUID          VARCHAR(50)         NOT NULL  ,
    NET_GUID          VARCHAR(50)         NOT NULL,
    AGENT_GUID        VARCHAR(50)         NOT NULL,
    NODE_ID           INT             NULL,
    PRIMARY KEY (NAR_GUID),
    FOREIGN KEY (NET_GUID) REFERENCES NET(NET_GUID),
    FOREIGN KEY (AGENT_GUID) REFERENCES AGENT(AGENT_GUID)
);

-- 网络连边(NET_EDGE)
CREATE TABLE NET_EDGE
(
    EDGE_GUID         VARCHAR(50)         NOT NULL  ,
    NET_GUID          VARCHAR(50)         NOT NULL,
    S_ID            INT         NOT NULL,
    E_ID            INT         NOT NULL,
    EDGE_WEIGHT     INT             NULL  DEFAULT 1,
    PRIMARY KEY (EDGE_GUID),
    FOREIGN KEY (NET_GUID) REFERENCES NET(NET_GUID)
);

-- PA-BDI模型数据表(PA_BDI)
CREATE TABLE PA_BDI
(
    MODEL_PA_BDI_GUID VARCHAR(50)         NOT NULL  ,
    SCH_GUID          VARCHAR(50)         NOT NULL,
    NET_GUID          VARCHAR(50)             NULL,
    MODEL_PA_BDI_REMARK TEXT        NULL,
    PRIMARY KEY(MODEL_PA_BDI_GUID),
    FOREIGN KEY (SCH_GUID) REFERENCES SCH(SCH_GUID),
    FOREIGN KEY (NET_GUID) REFERENCES NET(NET_GUID)
); 

-- PA-BDI规则表(PA_BDI_RULER)
CREATE TABLE PA_BDI_RULER
(
    PA_BDI_RULER_GUID VARCHAR(50)         NOT NULL  ,
    PA_BDI_RULER_NAME VARCHAR(50) NOT NULL,
    ATTITUDE_THRESHOLD FLOAT    NOT NULL,
    SEND_THRESHOLD  FLOAT       NOT NULL,
    RULER_REMARK    TEXT        NULL,
    PRIMARY KEY (PA_BDI_RULER_GUID)
);

-- PA-BDI模型与规则对应关系(PA_BDI_MODEL_RULER_R)
CREATE TABLE PA_BDI_MODEL_RULER_R
(
    PBMR_GUID         VARCHAR(50)         NOT NULL  ,
    MODEL_PA_BDI_GUID VARCHAR(50)         NOT NULL,
    PA_BDI_RULER_GUID VARCHAR(50)         NOT NULL,
    PRIMARY KEY (PBMR_GUID),
    FOREIGN KEY (MODEL_PA_BDI_GUID) REFERENCES PA_BDI(MODEL_PA_BDI_GUID),
    FOREIGN KEY (PA_BDI_RULER_GUID) REFERENCES PA_BDI_RULER(PA_BDI_RULER_GUID)
);

-- 个体传播情况信息表(AGENT_SPREAD)
CREATE TABLE AGENT_SPREAD
(   
    AS_GUID           VARCHAR(50)         NOT NULL  ,
    MODEL_PA_BDI_GUID VARCHAR(50)         NOT NULL,
    AGENT_SEND_GUID   VARCHAR(50)         NOT NULL,
    AGENT_ACCEPT_GUID VARCHAR(50)         NOT NULL,
    SPREAD_TIME     INT         NOT NULL,
    PRIMARY KEY (AS_GUID),
    FOREIGN KEY (MODEL_PA_BDI_GUID) REFERENCES PA_BDI(MODEL_PA_BDI_GUID),
    FOREIGN KEY (AGENT_SEND_GUID) REFERENCES AGENT(AGENT_GUID),
    FOREIGN KEY (AGENT_ACCEPT_GUID) REFERENCES AGENT(AGENT_GUID)
);

-- PA-BDI模型个体参数(PA_BDI_AGENT)
CREATE TABLE PA_BDI_AGENT
(
    PA_BDI_AGENT_GUID VARCHAR(50)         NOT NULL  ,
    AGENT_GUID        VARCHAR(50)         NOT NULL,
    MODEL_PA_BDI_GUID VARCHAR(50)         NOT NULL,
    BELIEF          INT         NOT NULL,
    SENSIBILITY     INT             NULL,
    ATTITUDE        INT             NULL,
    IMMUNITY        INT             NULL,
    ATTENSIION      INT             NULL,
    PRIMARY KEY (PA_BDI_AGENT_GUID)
);