from graphs import Base_graph, Rand_odd_graph, BA_graph, Small_world
from acquain import Acquain
from dao import Dao
def new_ba():
    # 生成一个图
    g = BA_graph(100,2,2)

    # # 查看图的信息
    # print('------------查看图的信息------------')
    print('边数:',g.get_edge_num(),'最大边数：',g.max_edge_num())
    print('度分布:',g.degree_distribute())
    print('邻接矩阵:',g.A)
    print('st连接:',g.get_st())
    print(Base_graph.st_to_A(Base_graph.A_to_st(g.A)))

    # 保存
    print('------------保存------------')

    d = Dao()
    d.save_graph(g.graph_type,g.get_st(),g.get_node_num())
    d.close()

def new_small_world():
    g=Small_world(50,20,0.3)
    d = Dao()
    d.save_graph(g.graph_type, g.get_st(),g.get_node_num())
    d.close()

def new_acquain():
    # 生成一个熟人网络
    g = Acquain(Rand_odd_graph(200,p=1),Time=180) 
    print(sorted(g.degree_data(),reverse=True))
    print(sum(g.degree_data()))


    d = Dao()
    d.save_graph('acquain',g.get_st(),g.get_node_num())
    d.close


def load_acquain():
    # 读取网络
    from dao import Dao
    d = Dao()
    #由于功能的不完善，guid值只能在数据库里查出来再填进去
    st,net_type = d.load_graph('6131e90c-67cc-11ec-87c7-3bca944c0033')
    g = Base_graph(Base_graph.st_to_A(st), net_type)
    print(g.degree_data())
    key_value = dict(g.degree_distribute())
    for i in sorted (key_value) : 
        print ((i, key_value[i]), end =" ") 
    d.close

if __name__=='__main__':
    new_small_world()