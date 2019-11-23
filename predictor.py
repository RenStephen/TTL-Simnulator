
import math

l=40
c1=1
c2=1
c3=1
d=1

ratio=2/4
l1=ratio*l
l2=(1-ratio)*l

beta=0.0
for i in range(41):

    T1=0
    T2=0
    if l1!=0:
        T1 = (-1 + beta * d * l1 + math.sqrt(1 + math.pow(beta * d, 2) * (l1 * l1))) / (l1)
        T2 = max((-1 + (1-beta) * d * (l1/(1+l1*T1)) + math.sqrt(1 + math.pow((1-beta) * d, 2) * math.pow(l1/(1+l1*T1),2))) / (l1/(1+l1*T1)),0.0)
    # print(T1,T2)

    alpha = 0.0
    for j in range (41):
        T3=0
        T4=0
        if l2!=0:
            T3 = (-1 + alpha * d * l2 + math.sqrt(1 + math.pow(alpha * d, 2) * (l2 * l2))) / (l2)
            T4 = max((-1 + (1 - alpha) * d * (l2 / (1 + l2 * T1)) + math.sqrt(1 + math.pow((1 - alpha) * d, 2) * math.pow(l2 / (1 + l2 * T1), 2))) / (l2 / (1 + l2 * T1)),0)

        T5=max(T2,T4)

        edge_departure = l1/(1+l1*T1)+l2/(1+l2*T3)
        edge_cost=c1*l1/(1+l1*T1)+c2*l2/(1+l2*T3)
        parent_cost=c3*edge_departure/(1+edge_departure*T5)

        print(str(edge_cost+parent_cost)+"\t",end=" ")

        alpha +=0.025

    print()

    beta+=0.025