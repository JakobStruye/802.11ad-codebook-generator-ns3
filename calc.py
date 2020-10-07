import numpy as np
import matplotlib.pyplot as plt

sector_angle_diff = 1 #degree
tick = 0.001 #s
tick_rotation= 0.15 #degree
switch_ticks = 5
predict_ticks = 2

simtime = 1000

times = np.arange(0,1000,tick)
orientations = np.arange(0,tick_rotation*times.shape[0], tick_rotation)
print(times[10], orientations[10])
sectors = np.arange(0,times.shape[0], sector_angle_diff)

cur_sector = 0
cur_sector_pred = 0
errors = []
errors_pred = []
for (idx, t) in enumerate(times):
    if idx % 1000 == 0:
        print(idx, times.shape[0])
    orientation = orientations[idx]

    if idx % switch_ticks == 0 and abs(orientation - sectors[cur_sector]) > abs(orientation - sectors[(cur_sector+1) % sectors.shape[0]]):
        cur_sector = (cur_sector + 1) % sectors.shape[0]
    errors.append(abs(orientation - sectors[cur_sector]))
    if idx % switch_ticks == 0 and abs((orientation + predict_ticks * tick_rotation) - sectors[cur_sector_pred]) > abs((orientation + predict_ticks * tick_rotation) - sectors[(cur_sector_pred+1) % sectors.shape[0]]):
        cur_sector_pred = (cur_sector_pred + 1) % sectors.shape[0]
    errors_pred.append(abs(orientation - sectors[cur_sector_pred]))


errors.sort()
errors_pred.sort()
yvals = np.arange(0, 1.0, 1 / float(len(errors)))
plt.plot(errors, yvals, label="nopred")
plt.plot(errors_pred, yvals, label="pred")
plt.legend()

plt.show(block=True)