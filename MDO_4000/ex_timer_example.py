#Timer example

import sched, time
#from
#https://stackoverflow.com/questions/3410976/how-to-round-a-number-to-significant-figures-in-python
from math import log10, floor
def round_to_1(x):
    return round(x, -int(floor(log10(abs(x)))))


t_then = 0
t_now = 0
diff = 0
t_total = 0

s = sched.scheduler(time.time, time.sleep)

def print_time():
    global t_now, t_then, diff, t_total
    t_now = time.time()
    #print ("From t_now", t_now)
    #print ("From t_then" , t_then)
    diff = t_now - t_then
    
    if diff != t_now:
        #print ("Diff = ", t_now - t_then)
        t_total += round_to_1(diff)
    t_then = t_now
    #print('\n')

count = 0


while count <= 5:
    # https://docs.python.org/2/library/sched.html
    #scheduler.enter(delay, priority, action, argument)
    s.enter(1, 1, print_time, ())
    s.run()
    print("Total Time: ", t_total)
    #print("Time Printed")
    count = count + 1

print("Completed")
