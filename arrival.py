class arrival:

    def __init__(self, time,key ):
        self.start_time=float(time)
        self.end_time=float(time)
        self.num_arrivals=1
        self.key=key
        self.arrival_rate=0

    def newArrival(self,time):
        self.num_arrivals+=1
        self.end_time=float(time)

    def computeArrivalRate(self):
        self.arrival_rate=self.num_arrivals/(self.end_time-self.start_time)

    def __eq__(self, other):
        return self.arrival_rate==other.arrival_rate
    def __lt__(self, other):
        return self.arrival_rate < other.arrival_rate
    def __gt__(self, other):
        return self.arrival_rate > other.arrival_rate