#
# (c) 2023 Michael Fitzgerald (mpfitz@ucla.edu)
#
# Some code for querying Vizier for catalog to construct a CMD.
# NOTE: I am using astroquery 0.4.6 on Ubuntu. I've tried to update it but this is the latest available.



from astroquery.vizier import Vizier

# https://vizier.cds.unistra.fr/viz-bin/VizieR?-source=J/AJ/133/1658
catalog_name = 'J/AJ/133/1658/acssggc'
cluster_name = 'M2'

# The row limit thing doesn't work for some reason
#Vizier.ROW_LIMIT = 100
#Vizier.ROW_LIMIT = 1000
#Vizier.ROW_LIMIT = -1 # get all sources (DO NOT DO THIS, WORST MISTAKE OF MY LIFE)

result = Vizier(catalog=catalog_name, columns=['Vmag', 'V-I'], row_limit=3000, column_filters={'e_Vmag': '<0.3', 'e_V-I': '<0.3', 'V-I': '-2.5 .. 2.5'}).query_constraints()[0]
# this outputs a TableList of only 1 entry (which is a two-column table). Add [0] to get that entry.

# debug
print(result)  # this prints out the first and only element of the TableList.
print(result['Vmag'])  # this prints out only the column named 'Vmag'


# parse the result to get the source list
vi = result['V-I']
vmag = result['Vmag']


# plot the color-magnitude diagram. Color (temperature) on X-axis, Magnitude (brightness) on Y-axis.
import matplotlib as mpl
import pylab
fig = pylab.figure(0)
fig.clear()
ax = fig.add_subplot(111)

ax.scatter(vi, vmag,
           marker='.',  # very small point
           c='red',  # color='k' gives black. I'd rather have a more visible color.
           s=2., # experiment with marker size
           )

# Add title and axes labels
pylab.title(f"Color-Magnitude Diagram (V-I vs Vmag) of {cluster_name}")
pylab.xlabel('V-I')
pylab.ylabel('Vmag')
pylab.grid(True)

# invert the y axis
pylab.gca().invert_yaxis()

# we're not using pylab
pylab.draw()
pylab.show()
fig.savefig('hw4prob3.pdf', dpi=300)

