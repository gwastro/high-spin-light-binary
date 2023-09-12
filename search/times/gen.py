from pycbc import dq

start_time = 1253977218
end_time = 1338166018 

hsegs = dq.query_flag('H1', 'DATA', start_time, end_time)
lsegs = dq.query_flag('L1', 'DATA', start_time, end_time)
vsegs = dq.query_flag('V1', 'DATA', start_time, end_time)


print(abs(hsegs))
print(abs(lsegs))
print(abs(vsegs))


from pycbc.events.veto import segments_to_start_end
import numpy
from ligo.segments import *


span = segmentlist([(start_time, end_time)])

hoff = span - hsegs
loff = span - lsegs
voff = span - lsegs

off = hoff & loff & voff

target = 86400 * 2
start = start_time
stop = off[0][0]
j = 0

bounds = []
while stop < end_time:
    dur = 0
    while dur < target and stop < end_time:
        tspan = segmentlist([segment(start, stop)])
        dur = abs(hsegs & lsegs & vsegs & tspan)

        j += 1
        stop = off[j][1]
    else:
        start = off[j-1][1]
        bounds.append(tspan)
        
        print(tspan, dur, abs(hsegs & lsegs & tspan) / 86400.0, abs(tspan) / 86400.0)
    

# merge last one into the previous
last = bounds[-1]
bounds = bounds[:-1]
bounds[-1] = last | bounds[-1]

pat = \
"""
[workflow]
start-time = {}
end-time = {}

"""

for k, bound in enumerate(bounds):
    f = open('gps_times_O3b_analysis_{}.ini'.format(k), 'w')
    f.write(pat.format(bound[0][0], bound[0][1]))
