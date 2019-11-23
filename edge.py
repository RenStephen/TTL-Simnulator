import math
from random import randint

class edge:

    def __init__(self, cost, parent):
        self.TTL=0
        self.cost = cost
        self.parent = parent

        self.end_time=-1
        self.start_time=-1

        self.keys_sent=0
        self.keys_arrived=0
        # print("edge made")

    def setTTL(self,delay, arrival_rate):
        if arrival_rate == 0:
            self.TTL=0
        else:
            self.TTL=(-1+delay*arrival_rate+math.sqrt(1+(delay)*(delay)*arrival_rate*arrival_rate))/arrival_rate
        return self.TTL

    def input(self, time):

        self.keys_arrived += 1

        if self.start_time==-1:
            self.start_time=time

        if self.end_time==-1:
            self.end_time=time+self.TTL

        # if the TTL has expired
        if time >= self.end_time:
            self.output()
            self.end_time = time + self.TTL

    def output(self):
        self.keys_sent+=1

        # flush to the parent
        self.parent.input(self.end_time)


    def getCost(self):
        return self.cost*self.keys_sent


class parent:

    def __init__(self, cost):
        self.TTL=0
        self.cost = cost

        self.end_time=-1
        self.start_time=-1

        self.keys_sent=0
        self.keys_arrived=0

    def setTTL(self,delay, arrival_rate, multiple=False):


        if multiple:
            TTL4=0
            TTL3=0
            if arrival_rate[0]!=0:
                TTL3=(-1+delay[0]*arrival_rate[0]+math.sqrt(1+(delay[0])*(delay[0])*arrival_rate[0]*arrival_rate[0]))/arrival_rate[0]
            if arrival_rate[1]!=0:
                TTL4=(-1+delay[1]*arrival_rate[1]+math.sqrt(1+(delay[1])*(delay[1])*arrival_rate[1]*arrival_rate[1]))/arrival_rate[1]
            self.TTL=max(TTL3,TTL4)
        else:
            self.TTL=(-1+delay*arrival_rate+math.sqrt(1+(delay)*(delay)*arrival_rate*arrival_rate))/arrival_rate
        return self.TTL

    def hardsetTTL(self, ttl):
        self.TTL=ttl

    def input(self, time):
        self.keys_arrived += 1

        if self.start_time == -1:
            self.start_time = time

        if self.end_time == -1:
            self.end_time = time + self.TTL

        # if the TTL has expired
        if time >= self.end_time:
            self.output()
            self.end_time = time + self.TTL

    def output(self):
        self.keys_sent+=1


    def getCost(self):
        return self.cost*self.keys_sent


class SingleAggregator:

    def __init__(self,beta,delay,arrival_rate,cost1,cost2):
        self.parent=parent(cost2)
        self.edge = edge(cost1,self.parent)

        eTTL=self.edge.setTTL(beta*delay,arrival_rate)
        self.parent.setTTL((1-beta)*delay,arrival_rate/(1+arrival_rate*eTTL))

    def input(self,key):
        self.edge.input(key)

    def getCost(self):
        return self.parent.getCost()+self.edge.getCost()

class trippleAggregator:
    def __init__(self, beta, alpha, delay, arrival_rate, cost1, cost2, cost3, num,den):

        self.parent=parent(cost3)
        self.edge1=edge(cost1, self.parent)
        self.edge2=edge(cost2, self.parent)

        self.num=num
        self.den=den

        arrival_rate1=(num/den)*arrival_rate
        arrival_rate2=(1-num/den)*arrival_rate

        TTL1=self.edge1.setTTL(beta*delay, arrival_rate)
        TTL2=self.edge2.setTTL(alpha*delay, arrival_rate)

        d1=arrival_rate1/(1+arrival_rate1*TTL1)
        d2=arrival_rate2/(1+arrival_rate2*TTL2)

        self.parent.setTTL([(1-beta)*delay,(1-alpha)*delay],[d1,d2], multiple=True)

        # TTL3=max(self.parent.setTTL((1-beta)*delay, d1),self.parent.setTTL((1-alpha)*beta, d2))
        # self.parent.hardsetTTL(TTL3)


    def input(self,key):

        x = randint(0,self.den)
        if x <self.num:
            self.edge1.input(key)
        else:
            self.edge2.input(key)



    def getCost(self):
        return self.parent.getCost()+self.edge1.getCost()+self.edge2.getCost()

