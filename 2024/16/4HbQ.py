'''
Copied from /u/4HbQ as an example of Dijkstra's algorithm:
https://www.reddit.com/r/adventofcode/comments/1hfboft/2024_day_16_solutions/m2bcfmq/
https://topaz.github.io/paste/#XQAAAQDjAgAAAAAAAAAzHIoib6pXbueH4X9F244lVRDcOZab5q1+VXY/ex42qR7D+RJIsq5/YCi6YHJak4tBC2I+oV44GGsk3yILWGnOyXBRhMTGj1iPohCpnraI7cOVIQMgn6rgSzIs8ivVrm/FjrPnA3L7V10T3k8AVKb27JewAo1T1wA11F9z4rI0R1fmuEZ5K+nQHoaofPDKAZ51R/ZOdCADcaXlpPtbO2QrM5ZR6x57jTd2o/v7MNJDNSOMaxeEh4EUz8J3j16sRLDEMw14sC64F/hO2MBhFBQKExg7/Y98qGz3k4PqLSZv+dbTshbBbXWfD8lGlqlB32772xeE3tDXnVzzpfvJIVm8E0aZFC8AVl/SGdE9RhilT65yaz/v++YJfMZrlxLUxGDGwvltVjHFzk4d+vejcuSNueWSnuLwqNO76o4YZv6S8rC7VcEE/V36ABuJIPGbes4Q8+O6qPZH6Cmrzvp/PEZbNAoUqp3A+SvjG/SsBDkS28QDoMVDMhijw5z+25s3jEI2QwXa+pQeAaplnJrlW7AwJsXrqq5Tcahh4DOUabyx/CosbFl1/97cvJ8=
'''
from collections import defaultdict, deque
from time import time
from heapq import heappop, heappush

grid = {i+j*1j: c for i,r in enumerate(open('./input'))
                  for j,c in enumerate(r) if c != '#'}

start, = (p for p in grid if grid[p] == 'S')

seen = []
best = 1e9
dist = defaultdict(lambda: 1e9)
todo = [(0, t:=0, start, 1j, [start])]
#todo = deque([(0, t:=0, start, 1j, [start])])

start_time = time()
while todo:
    val, _, pos, dir, path = heappop(todo)
    #val, _, pos, dir, path = todo.popleft()

    if val > dist[pos, dir]: continue
    else: dist[pos, dir] = val

    if grid[pos] == 'E' and val <= best:
        seen += path
        best = val

    for r, v in (1, 1), (+1j, 1001), (-1j, 1001):
        v, t, p, d = val+v, t+1, pos + dir*r, dir*r
        if p not in grid: continue
        heappush(todo, (v, t, p, d, path + [p]))
        #todo.append((v, t, p, d, path + [p]))
end_time = time()


print(best, len(set(seen)))
print('time: ', end_time-start_time)