from itertools import groupby
from graphs import *
class Acquain(Base_graph):
    # inherit_percent, variation_prob, disconnect_prob, 
    def id_generate():
        id =0
        while True:
            yield id
            id+=1
    def __init__(self,init_graph, **args):
        
        super().__init__(init_graph.A, 'acquain')
        self.p_id =Acquain.id_generate()

        # 初始化参数
        self.Time = args.get('Time',30)
        self.inherit_percent = args.get('inherit_p',0.2)
        self.variation_prob = args.get('variation_prob',0.3)
        self.disconnect_prob = args.get('disconnect_prob',0.2)


        # 获取初始种群
        self.init_group()
        print('网络初始化完成，初始网络: {}, 初始个体数：{}, 初始边数：{}, 下面开始演化...'
            .format(init_graph.graph_type, self.get_node_num(),self.get_edge_num()))

        # 演化
        self.evolve()
        print('演化结束，人口数：',len(self.people))

        # people结果输出到A
        self.set_A()        
        

    def init_group(self) ->set:
        # convert A to people for better evolution later
        A = self.A
        people=list()
        N = np.size(A,1)
        for i in range(N):
            import random
            people.append(Person(age = random.randint(0,80),id=next(self.p_id)))
        for i in range(N-1):
            for j in range(i+1,N):
                if A[i][j]:
                    people[i].neighbors.add(people[j])
                    people[j].neighbors.add(people[i])
        self.people = set(people)
    def evolve(self):
        for t in range(self.Time):
            print('t:', t,end='\n' if t%10==9 or t==self.Time-1 else '\t')
            self.inherit()
            self.variation()
            self.disconnect()
            self.die_birth()         
    def set_A(self):
        N = len(self.people)
        people = list(self.people)
        people = sorted(people,key = lambda x:x.id)
        A=np.zeros((N,N)).astype(bool)
        for i in range(N-1):
            for j in range(i+1,N):
                if people[j] in people[i].neighbors:
                    A[i,j]=True
                    A[j,i]=True
        self.A = A

    def inherit(self):
        percent = self.inherit_percent
        for p in self.people : 
            if p.father and p.age==2:
                new_neighbors = set(np.random.choice(list(p.father.neighbors), 
                    size=int(len(p.father.neighbors )*percent),replace=False))
                p.neighbors = p.neighbors | new_neighbors
                p.neighbors.discard(p)
                for neighbor in new_neighbors:
                    if neighbor != p:
                        neighbor.neighbors.add(p)
    def variation(self):
        prob = self.variation_prob
        pp = np.random.rand(len(self.people))
        i = -1
        for p in self.people : 
            i+=1
            if pp[i] > prob:
                continue
            strangers = self.people-p.neighbors
            strangers.discard(p) # 删除自己
            if  strangers:
                target = min(strangers,key=lambda x:abs(x.age-p.age))
                p.neighbors.add(target)
                target.neighbors.add(p)
    def disconnect(self):
        prob = self.disconnect_prob
        pp = np.random.rand(len(self.people))
        i = -1
        for p in self.people : 
            i+=1
            if pp[i] > prob:
                continue
            if p.neighbors:
                # 找一个差距最大的断开
                target = max(p.neighbors, key= lambda x:abs(x.age-p.age))
                p.neighbors.remove(target)
                target.neighbors.remove(p)
    def die_birth(self):
            dying = set() # 即将死亡的人
            birthing = set() # 新生的人
            for p in self.people:
                p.age+=1
                if p.age>=80:
                    dying.add(p)
                if p.age==20:
                    birthing.add(Person(father=p,id = next(self.p_id)))
            # 删除 死亡的个体
            self.people = self.people-dying
            # 删掉所有人的已死亡邻居
            for p in self.people:
                p.neighbors = p.neighbors-dying
            # 出生
            self.people = self.people | birthing
            
class Person:
    def __init__(self, **args) -> None:
        import random
        self.age = args.get('age',0)
        self.id = args.get('id',random.random())
        self.father=args.get('father',None)
        self.neighbors = args.get('neighbors',set())

    # 打印
    def __str__(self) -> str:
        neighbors = ', '.join([str(p.id) for p in self.neighbors])
        return '{age: %d,  id: %d,  father: %s,  neighbors:[%s] }' \
            % (self.age ,self.id, str(self.father.id) if self.father else 'None', neighbors)

