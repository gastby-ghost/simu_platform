import numpy as np
class Base_graph:
    def __init__(self,A,graph_type):
        # 子类必须初始化A和graph_type。
        self.graph_type = graph_type
        self.A=A# A是一个逻辑矩阵
    
    def get_st(self):
        return Base_graph.A_to_st(self.A,self.get_node_num())
    def get_node_num(self)->int:
        return np.size(self.A,0)
    def get_edge_num(self)->int:
        return np.sum(self.A)//2
    def max_edge_num(self):
        return self.get_node_num()*(self.get_node_num()-1)//2
    def degree_data(self) ->np.ndarray:
        return np.sum(self.A,0)
    def degree_distribute(self) -> dict:
        degree=np.sum(self.A,0)
        #print(degree.dtype)
        # degree.sort()
        # print(degree)
        from collections import Counter
        return Counter(degree)
    def get_num_A(self):
        return self.A.astype(int)

    def A_to_st(A, N=None)->list:
        if not N:
            N = np.size(A,0)
        st=list()
        for i in range(N-1):
            for j in range(i+1,N):
                if A[i,j]:
                    st.append((i,j))
        return st
    def st_to_A(st,N=None):
        if not N:
            N = max(max(row) for row in st)+1
        A = np.zeros((N,N)).astype(bool)
        for (r,c) in st:
            A[r,c]=True
            A[c,r]=True
        return A

class Rand_odd_graph(Base_graph):
    def __init__(self,N,p=0.2):
        import numpy as np
        A = np.random.rand(N,N)
        A = np.tril(A)
        A[np.eye(N).astype(bool)]=0
        
        A[A>p]=0
        A=A.astype(bool)
        A = A+A.T

        super().__init__(A,'er_random')

class BA_graph(Base_graph):
    def __init__(self,N,n,k,base = '随机'):
        '''
        新增节点选择m个邻居
        '''
        import numpy as np
        A = np.zeros((N,N)).astype(bool)
        if base=='随机':
            A_old = Rand_odd_graph(n,0.5).A
            A[0:n,0:n]=A_old
        elif base == '全连接':
            A_old = Rand_odd_graph(n,1).A
            A[0:n,0:n]=A_old
        for i in range(n,N):
            print(i)
            degree = np.sum(A,axis=0)
            degree = degree[0:i]
            if np.sum(degree)==0:
                degree = np.ones((i))
            degree = degree/np.sum(degree)
            choice = np.random.choice(np.arange(0, i), size=(1,k),p=degree,replace=False)
            A[i,choice]=True
            A[choice,i]=True
        
        super().__init__(A,'BA_Scale_free')

class Small_world(Base_graph):
    def __init__(self,N,k,beta):
        '''
        k: 和左右各k人 要求2k+1<=N，beta: 重连概率
        '''
        
        A=np.zeros((N,N)).astype(bool)
        # s看边的起点集合，t是终点集合，s和t同一位置的元素连起来就是一条边
        s = np.repeat(np.arange(N).reshape(N,1),k,axis=1)
        t = s+ np.repeat(np.arange(k).reshape(1,k),N,axis=0)
        t = np.mod(t+1,N)
        for source in range(N):
            switch_edge = np.random.rand(k) < beta # source 发出m条边，其中部分switch_edge要断开，改为new_target
            new_target = np.random.rand(N)# 权重不同
            new_target[source]=0 # 新边不能是和自己 
            new_target[s[t==source]] = 0 # 不能是已有的 从t发给s的
            new_target[t[source, ~switch_edge]] =0 # 不能是已有的 从s发出的 且此回合不改变的边
            b = np.argsort(-new_target)
            t[source,switch_edge] = b[0:sum(switch_edge>0)]
        st = np.append(np.reshape(s,(k*N,1)),np.reshape(t,(k*N,1)),axis=1)
        super().__init__( Base_graph.st_to_A(st.tolist(),N),'watt_Small_world')