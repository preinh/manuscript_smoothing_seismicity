import numpy as np
import matplotlib
import matplotlib.pyplot as plt
#import matplotlib.ticker as mtick
from matplotlib.ticker import FuncFormatter

def to_percent(y, position):
    # Ignore the passed in position. This has the effect of scaling the default
    # tick locations.
    s = "%.2f"%(100 * y)
    # The percent symbol needs escaping in latex
    if matplotlib.rcParams['text.usetex'] == True:
        return s + r'$\%$'
    else:
        return s + '%'


# kernel functions
def h(m, p):
	return p[0]*np.exp(m*p[1])


def kernel_kagan_knopoff(r, m, p, aw=1.5):
	h2 = h(m, p)
	r2 = r*r

	factor1 = (aw - 1)/np.pi/h2
	factor2 = (1 + (r2/h2))**(-aw)
	return factor1 * factor2


def kernel_kagan_knopoff(r, m, p, aw=1.5):
	h2 = h(m, p)
	r2 = r*r

	factor1 = (aw - 1)/np.pi/h2
	factor2 = (1 + (r2/h2))**(-aw)
	return factor1 * factor2



# plot setup
parameters = [1.39, 1.18]
distances = np.linspace(-50, 50, 200)
magnitudes = [3, 4, 5, 6]
colors= ['g', 'b', 'r', 'orange']

f = plt.figure(figsize=(10,12))

for i, m in enumerate(magnitudes):
	values = kernel_kagan_knopoff(
		distances,
		m,
		parameters)

	plt.plot(distances, values, c=colors[i],
		linewidth=2, 
		#marker=None,
		#marker='none', 
		label="mag=%.1f"%m)

plt.xlim((-50,50))
plt.xlabel("distances [km]")
plt.ylabel("density")
plt.title("Kagan-Knopoff kernels for Brazilian bandwidths")
plt.legend()

# format percentual axis
# fmt = '%.2f%%' # Format you want the ticks, e.g. '40%'
# ticks = mtick.FormatStrFormatter(fmt)
formatter = FuncFormatter(to_percent)
plt.gca().yaxis.set_major_formatter(formatter)


plt.show()