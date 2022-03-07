-- 1. 生成方案
INSERT INTO 
SCH(SCH_GUID,SCH_NAME,SCH_CREATE_TIME,SCH_AIM,SCH_CREATE_ROLE,SCH_REMARK)
VALUES
(UUID(),"TEST",now(),"test of using database","shan",NULL);

-- 2. 生成网络
-- 这部分的话通过修改过的学长的代码实现，即main函数

-- 3. 生成个体数据
-- 通过代码new_agent生成特定数量的数据

-- 4. 绑定一个方案的情景下，生成一个BDI模型，方案GUID从数据中选择
INSERT INTO
PA_BDI(MODEL_PA_BDI_GUID,SCH_GUID)
VALUES
(UUID(),'bb111aa5-6884-11ec-82e9-9822eff6f6cd');

-- 5. 选择一个网络填入该BDI模型
UPDATE PA_BDI
SET NET_GUID='e0a658a5-6884-11ec-828f-61e8c2066380'
WHERE MODEL_PA_BDI_GUID='5ef5dc15-6887-11ec-82e9-9822eff6f6cd';

-- 6. 选择网络中节点数量的个体与网络联系起来，一一对应,
-- 并生成该BDI方案下所有个体的BDI参数
-- r_node_agent程序实现

-- 1. 生成一个方案，描述方案参数细节

-- 2. 添加一定量的个体，并配置个体参数

-- 3. 使用某个个体集合，生成一个网络，目前考虑的是熟人网络
-- 4. 对个体使用联想记忆网络对信念或者谣言进行学习，生成个人的历史经验或者BDI参数。
-- 5. 利用上述的网络与BDI参数进行BDI模型的演化。