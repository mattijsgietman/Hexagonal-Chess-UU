import numpy as np
import matplotlib.pyplot as plt

episodes = np.arange(0, 6500, 100)

model_1092_0_99 =[0,2,0,4,8,1,9,8,7,12,10,6,6,7,9,10,14,14,12,14,21,12,21,20,14,33,27,24,25,23,23,26,18,20,16,25,22,31,16,21,22,24,33,26,28,36,31,35,28,38,33,28,38,39,24,40,33,41,36,36,33,47,37,41,47]
model_1092_0_9 = [0,4,3,5,1,5,8,9,12,11,9,9,17,8,15,15,19,26,32,21,22,23,34,26,31,29,24,32,31,33,36,29,42,38,28,33,43,35,36,42,47,41,39,41,43,35,45,49,42,51,53,47,46,50,53,48,54,49,48,56,49,57,54,48,55]
model_1092_0_85 = [0,4,0,3,4,3,4,4,6,7,12,8,9,14,9,15,14,15,15,20,20,20,13,19,19,18,25,29,25,29,38,36,32,43,41,34,37,36,46,54,40,55,43,56,48,54,51,54,52,51,62,56,55,59,50,64,67,60,67,65,63,61,61,73,64]
model_1092_0_8 = [5,1,9,5,12,10,3,11,9,5,11,10,17,15,22,16,23,13,14,19,31,24,25,28,31,33,25,30,32,28,35,41,44,46,35,31,37,39,35,41,38,43,36,43,41,41,43,43,51,54,47,50,46,46,59,48,56,47,48,57,53,53,53,51,55]
model_91_085 = [0,4,6,6,11,10,7,6,10,9,15,11,8,11,16,17,12,12,11,15,14,10,18,16,19,22,22,14,18,17,13,10,12,17,15,25,17,22,26,26,16,17,24,27,23,23,26,28,27,30,30,27,22,22,35,29,28,42,42,35,46,52,32,46,43]

#plt.plot(episodes, model_1092_0_99, label='Gamma=0.99')
#plt.plot(episodes, model_1092_0_9, label='Gamma=0.9')
#plt.plot(episodes, model_1092_0_85, label='Gamma=0.85')
plt.plot(episodes, model_91_085, label='Gamma=0.85')
#plt.plot(episodes, model_1092_0_8, label='Gamma=0.8')
plt.xlabel('Episodes')
plt.ylabel('Wins in last 100 games')
plt.title('Win Percentage vs Episodes Input Dimensions=91')
plt.ylim(0, 100)
plt.legend()
plt.show()
'''

min_max_results = [6.8,2.3,5.2,2.4,4.7,3,1.4,2.9,5.2,6.4,6.6,6.9]
min_max_results_no_alpha_beta = [151,12.2,48.4,3.4,47.8,6.2,3.6,4.2,7.8,25.9,22.6,30.1]

puzzles = np.arange(1, 13, 1)
width = 0.35

fig, ax = plt.subplots()
#rects1 = ax.bar(puzzles, min_max_results, width, label='Including Alpha-Beta Pruning')
rects2 = ax.bar(puzzles, min_max_results_no_alpha_beta, width, label='Excluding Alpha-Beta Pruning')

ax.set_xlabel('Puzzle')
ax.set_ylabel('Time (seconds)')
ax.set_title('Time to Solve Puzzles')
ax.set_xticks(puzzles)
ax.legend()

fig.tight_layout()

plt.show()
'''