from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()

ind = np.arange(0, 8, 2)
width = 0.5

result1 = (1.93, 2.3, 2.1, 3.8)
result2 = (0.7, 0.9, 1.2, 1.94)
result3 = (0.52, 0.85, 1.15, 1.92)
results1_std = (0.147, 0.15, 0.012, 0.22)
results2_std = (0.008, 0.084, 0.097, 0.012)
results3_std = (0.09, 0.089, 0.133,  0.013)

rects1 = ax.bar(ind, result1, width, color='0.75', edgecolor='k', yerr=results1_std)
rects2 = ax.bar(ind + width, result2, width, color='w', edgecolor='k', yerr=results2_std)
rects3 = ax.bar(ind + 2*width, result3, width, color='0.35', edgecolor='k', yerr=results3_std)

ax.set_xlabel('RTT latency (ms)')
ax.set_ylabel('Response Time (s)')
x1, x2, y1, y2 = plt.axis()
plt.axis((x1, x2, 0, 4))
plt.title('Verbose log with compression')
ax.set_yticks(np.arange(0, 4.5, 0.5))
ax.set_xticks(ind+width)
ax.set_xticklabels(('20', '100', '200', '400'))
ax.legend( (rects1[0], rects2[0], rects3[0]), ('500 KBit/s', '1000 KBit/s', '2000 KBit/s'), title="Throughput")

pp = PdfPages('comp_att.pdf')
pp.savefig(fig)
pp.close()
plt.show() 
