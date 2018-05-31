from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()

ind = np.arange(0, 12, 2)
width = 0.5

splinter = (2.8, 23.5, 245, 8.6, 3.6, 44)
olumofin = (16, 128, 512, 128, 128, 192)

rects1 = ax.bar(ind, splinter, width, color='k', edgecolor='k')
rects2 = ax.bar(ind + width, olumofin, width, color='0.5', edgecolor='k')

ax.set_ylabel('Bandwidth (KB)')
x1, x2, y1, y2 = plt.axis()
plt.axis((x1, x2, 0, 5))
ax.set_yticks(np.arange(0, 512+64, 64))
ax.set_xticks(ind+0.5*width)
ax.set_xticklabels(('Rest. Q1', 'Rest. Q2', 'Rest. Q3', 'Flights Q1', 'Flights Q2', 'Maps'))
ax.legend( (rects1[0], rects2[0]), ('Splinter', 'Olumofin et al'))

plt.tight_layout()
pp = PdfPages('bandwidth_comparison.pdf')
pp.savefig(fig)
pp.close()
plt.show() 
