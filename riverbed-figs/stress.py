from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure(1, figsize=(5.5,2.5))
ax = fig.add_subplot(111)

ax.set_xlabel("# of universes")
ax.set_ylabel("Response Rate (KB/s)")

x_values = [1, 128, 256, 384, 512, 1023]

ax.set_xticks(np.arange(0, 1025, 128))
ax.set_yticks(np.arange(0, 650, 100))
ax.set_ylim([0,600])
ax.plot(x_values, [525, 525, 525, 525, 525, 525], '-kv', linewidth=2, markersize=8,
               label="no swapping")

ax.plot([256, 384, 512, 1023], [500, 360, 340, 340], '--ko', linewidth=2, markersize=8,
                label="swapping")

plt.legend()
plt.tight_layout()
pp = PdfPages('stress.pdf')
pp.savefig(fig)
pp.close()

plt.show()
