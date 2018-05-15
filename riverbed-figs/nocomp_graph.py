from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()

ind = np.arange(0, 8, 2)
width = 0.5

result1 = (0.359, 0.528, 0.739, 1.137)
results1_std = (0.01, 0.005, 0.009, 0.02) 
result2 = (0.369, 0.527, 0.742, 1.138)
results2_std = (0.005, 0.0037, 0.011, 0.022)
result3 = (0.363, 0.525, 0.740, 1.132)
results3_std = (0.013, 0.01, 0.01, 0.018)

rects1 = ax.bar(ind, result1, width, color='0.75', edgecolor='k', yerr=results1_std)
rects2 = ax.bar(ind + width, result2, width, color='w', edgecolor='k', yerr=results2_std)
rects3 = ax.bar(ind + 2*width, result3, width, color='0.35', edgecolor='k', yerr=results3_std)

ax.set_xlabel('RTT latency (ms)')
ax.set_ylabel('Response Time (s)')
x1, x2, y1, y2 = plt.axis()
plt.axis((x1, x2, 0, 4))
plt.title('Hash-only log')
ax.set_yticks(np.arange(0, 4.5, 0.5))
ax.set_xticks(ind+width)
ax.set_xticklabels(('20', '100', '200', '400'))
ax.legend( (rects1[0], rects2[0], rects3[0]), ('500 KBit/s', '1000 KBit/s', '2000 KBit/s'), loc=2, title="Throughput")

pp = PdfPages('nocomp_att.pdf')
pp.savefig(fig)
pp.close()
plt.show() 
