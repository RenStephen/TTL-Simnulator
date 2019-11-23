import csv
import operator
from edge import SingleAggregator
from arrival import arrival
from edge import trippleAggregator





key_arrival_rates={}
key_time_set={}
documents = ['akamai_int_keys_merged_0_2_synthetic_top_1200_num_2850000_speedup_5000.00000000.csv','akamai_int_keys_merged_0_2_top_1200_num_2837989_speedup_5000.00000000.csv']

with open(documents[0]) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    iterCSV = iter(readCSV)
    next(iterCSV)

    for row in iterCSV:
        if row[1] in key_arrival_rates.keys():
            key_arrival_rates[row[1]].newArrival(row[0])
        else:
            key_arrival_rates[row[1]]=arrival(row[0],row[1])

        if row[1] in key_time_set.keys():
            key_time_set[row[1]].append(float(row[0]))
        else:
            key_time_set[row[1]]=[float(row[0])]


for key in key_arrival_rates.keys():
    key_arrival_rates[key].computeArrivalRate()


# sort=sorted(arrival_rates.values(), key=operator.attrgetter('arrival_rate'))
# f = open("akamai_symthetic.txt", "w")
# for key in sort:
#     f.write(str((key.arrival_rate,key.key))+"\n")
# f.close()

delay=10
cost1 = 1
cost2 =1
cost3=1

key='147'
print(key_arrival_rates[key].arrival_rate)
for beta in range(41):
    for alpha in range(41):
        agg = trippleAggregator( float(beta*0.025),float(alpha*0.025), delay, key_arrival_rates[key].arrival_rate,cost1,cost2,cost3,0,3)

        finaltime=0
        for time in key_time_set[key]:
            agg.input(time)
            finaltime=time
        agg.edge1.output()
        agg.edge2.output()
        agg.parent.output()

        print(str(agg.getCost()/finaltime)+"\t", end=" ")

    print()








