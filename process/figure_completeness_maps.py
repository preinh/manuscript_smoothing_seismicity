# -*- coding: utf-8 -*-
# Python Numerical and Plotting Libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
# from matplotlib.lines import mlines
from copy import deepcopy

# HMTK Catalogue Import/Export Libraries
from hmtk.parsers.catalogue.csv_catalogue_parser import CsvCatalogueParser, CsvCatalogueWriter


# HMTK Declustering Tools
from hmtk.seismicity.declusterer.dec_afteran import Afteran
from hmtk.seismicity.declusterer.dec_gardner_knopoff import GardnerKnopoffType1
from hmtk.seismicity.declusterer.distance_time_windows import (GardnerKnopoffWindow,
                                                               GruenthalWindow,
                                                               UhrhammerWindow)

# HMTK Completeness Tools
from hmtk.seismicity.completeness.comp_stepp_1971 import Stepp1971

from hmtk.plotting.seismicity.completeness.cumulative_rate_analysis import SimpleCumulativeRate
from hmtk.plotting.seismicity.completeness.plot_stepp_1972 import create_stepp_plot

# HMTK Plotting Tools
from hmtk.plotting.mapping import HMTKBaseMap
from hmtk.plotting.seismicity.catalogue_plots import (plot_depth_histogram,
                                                      plot_magnitude_time_scatter,
                                                      plot_magnitude_time_density,
                                                      plot_magnitude_depth_density,
                                                      plot_rate,
                                                      plot_weekday_histogram,
                                                      plot_hour_histogram,
                                                      plot_observed_recurrence)


print 'Imports OK!'

project_home = "/Users/pirchiner/dev/pshab_source_models"
_model = "background"

config = {
#    'catalog': project_home + "/data/catalogs/hmtk_bsb2013.csv",
    'catalog': project_home + "/data/catalogs/hmtk_bsb2014.11.csv",
    'declustered_catalog': project_home + "/"+_model+"/catalogs/bsb2014.11_declustered_catalog.csv",
    #'source_model': project_home + "/"+_model+"/raw/"+_model+"_bsb2014.11_geometries.xml",
    'map_config': {'min_lon': -80.0, 'max_lon': -30.0, 'min_lat': -37.0, 'max_lat': 13.0, 'resolution':'l'},
    # BR_Geral
    'fixed_completeness1' : np.array([[2014., 3.16],
                                      [1980., 4.28],
                                      [1968., 4.85],
                                      [1962., 6.0],
                                      [1940., 6.5]]),

    # pirchiner_simplificado
    'fixed_completeness2' : np.array([[2014., 3.0],
                                      [1975., 3.8],
                                      [1960., 4.8],
                                      [1938., 6.5]]),

}

# reading
parser = CsvCatalogueParser(config['catalog'])
catalogue = parser.read_file()
print 'Input complete: %s events in catalogue' % catalogue.get_number_events()
print 'Catalogue Covers the Period: %s to %s' % (catalogue.start_year,
    catalogue.end_year)

# Sort catalogue chronologically
catalogue.sort_catalogue_chronologically()
print 'Catalogue sorted chronologically!'

# 3.0 - 0.3 uncertainty
min_mag = 3.0
# filter magnitudes Mw lower than 3.0
_idx = catalogue.data['magnitude'] >= min_mag
catalogue.purge_catalogue(_idx)

# get the method
decluster_method = GardnerKnopoffType1()

# config the method, selecting the windows
decluster_config = {'time_distance_window': UhrhammerWindow(),
                    'fs_time_prop': 1.0}

#---------------------------------------------
# declustering
cluster_index_uh, cluster_flags_uh = \
    decluster_method.decluster(catalogue, decluster_config)
#---------------------------------------------

# adding to the catalog
# The cluster flag (main shock or after/foreshock)
# and cluster index to the catalogue keys
catalogue.data['cluster_index_uh'] = cluster_index_uh
catalogue.data['cluster_flags_uh'] = cluster_flags_uh

# create a copy from the catalogue object to preserve it
catalogue_uh = deepcopy(catalogue)
#catalogue_af = deepcopy(catalogue)

# Nmero de eventos con magnitud mayor a la minima selecccionada
#print '\n'
#print 'Número de eventos con magnitud mayor a la mínima selecccionada',
#np.min(catalogue.data['magnitude']), 'es:', catalogue.get_number_events()

# purge...
catalogue_uh.purge_catalogue(cluster_flags_uh == 0)
# cluster_flags == 0: mainshocks
#catalogue_af.purge_catalogue(cluster_flags_af == 0)
# cluster_flags == 0: mainshocks

print 'Gardner-Knopoff/UhrhammerWindow\tbefore: ', 
catalogue.get_number_events(), " after: ",
catalogue_uh.get_number_events()

#completeness_table =

#print config['fixed_completeness']
# completeness
_config = {'magnitude_bin': 0.5,
           'time_bin': 5.0,
           'increment_lock': True}
completeness_algorithm = Stepp1971()
# completeness_algorithm = SimpleCumulativeRate()
completeness_table = completeness_algorithm.completeness(catalogue_uh,
                                        _config,
                                        # saveplot="completeness_temporal_stepp"
                                        )

completeness_table_stepp = completeness_table
print completeness_table
print config['fixed_completeness2']


map_dpi = 300
add_geology = False
add_sourcemodel = False
savefig=True

#map_title = 'Brazilian Seismic Zones'
map_title = 'Earthquake epicenters on the BSB2014.11 catalog'
#map_title = 'ISC-GEM Catalogue'
#map_title = 'South-American Lithology'

# Configure the limits of the map and the coastline resolution
map_config = {'min_lon': -80.0, 'max_lon': -30.0, 'min_lat': -37.0, 'max_lat': 14.0, 'resolution':'l'}
#map_config = {'min_lon': -72.0, 'max_lon': -68.0, 'min_lat': -22.0, 'max_lat': -18.0, 'resolution':'l'}
#map_config = {'min_lon': -95.0, 'max_lon': -25.0, 'min_lat': -65.0, 'max_lat': 25.0, 'resolution':'l'}



basemap1 = HMTKBaseMap(map_config, map_title, dpi=map_dpi)
#basemap1.add_catalogue(catalogue, linewidth=1., alpha=0.5)


_c = deepcopy(catalogue_uh)
# _c.catalogue_mt_filter(config['fixed_completeness2'], reverse=True)
_c.catalogue_mt_filter(completeness_table_stepp, reverse=True)


basemap1.add_size_scaled_points(_c.data['longitude'], 
                                 _c.data['latitude'],
                                 np.exp(_c.data['magnitude']-3),
                                 edgecolor='red',
                                 facecolor='none',
                                 alpha=0.7,
                                 linewidth=1,
                                 color='red',
                                 overlay=True)


_c = deepcopy(catalogue_uh)
# _c.catalogue_mt_filter(config['fixed_completeness2'], reverse=True)
_c.catalogue_mt_filter(config['fixed_completeness1'], reverse=False)

basemap1.add_size_scaled_points(_c.data['longitude'], 
                                 _c.data['latitude'],
                                 np.exp(_c.data['magnitude']-3),
                                 edgecolor='lightgreen',
                                 facecolor='none',
                                 alpha=0.7,
                                 linewidth=1,
                                 color='lightgreen',
                                 overlay=True)


# plot_magnitude_time_scatter(_c,
#   # completeness_table=config['fixed_completeness2'],
#   # completeness_table=completeness_table,
#   # fmt_string='k+',
#   marker='+',
#   s=60,
#   # linestyle='',
#   alpha=0.8,
#   linewidth=2,
#   edgecolor='lightgreen',
#   color='lightgreen',
#   # color='orange',
#   # filename="../z_img_completeness_temporal_scatter_fixed.pdf", 
#   # filetype='pdf', 
#   dpi=300,
#   figsize=(20, 10),
#   overlay=True)

completeness_table = config['fixed_completeness2']
# plt.step(completeness_table[:, 0], completeness_table[:, 1], 
#   where='post', 
#   linewidth=3,
#   color='blue',
#   label="Simplified")


# completeness_table=completeness_table_stepp
# completeness_table = np.vstack((completeness_table, [1933, 6.5]))
# plt.step(completeness_table[:, 0], completeness_table[:, 1],
#   where='post',
#   linewidth=4,
#   # alpha=0.6,
#   color = 'darkorange',
#   label="Stepp1972")

# completeness_table = config['fixed_completeness1']
# plt.step(completeness_table[:, 0], completeness_table[:, 1],
#   where='post',
#   linewidth=4,
#   color='green',
#   # alpha=0.6,
#   label=u"Assumpção2014")



# plot_magnitude_time_scatter(_c,
#   # completeness_table=config['fixed_completeness2'],
#   # completeness_table=completeness_table,
#   #fmt_string='k+',
#   marker='+',
#   s=60,
#   alpha=0.8,
#   # linestyle='',
#   linewidth=2,
#   edgecolor='red',
#   color='red',
#   # color='orange',
#   # filename="../z_img_completeness_temporal_scatter_fixed.pdf", 
#   # filetype='pdf', 
#   #dpi=300,
#   #figsize=(9, 4),
#   overlay=True)

_c = deepcopy(catalogue_uh)
_c.catalogue_mt_filter(config['fixed_completeness1'], reverse=True)
_c.catalogue_mt_filter(completeness_table_stepp, reverse=False)



basemap1.add_size_scaled_points(_c.data['longitude'], 
                                 _c.data['latitude'],
                                 np.exp(_c.data['magnitude']-3),
                                 edgecolor='gold',
                                 facecolor='none',
                                 alpha=0.7,
                                 linewidth=1,
                                 color='gold',
                                 overlay=True)



# plot_magnitude_time_scatter(_c,
#   # completeness_table=config['fixed_completeness2'],
#   # completeness_table=completeness_table,
#   #fmt_string='k+',
#   marker='+',
#   s=60,
#   alpha=0.8,
#   # linestyle='',
#   linewidth=2,
#   edgecolor='gold',
#   color='gold',
#   # color='orange',
#   # filename="../z_img_completeness_temporal_scatter_fixed.pdf", 
#   # filetype='pdf', 
#   #dpi=300,
#   #figsize=(9, 4),
#   overlay=True)

# plt.legend(loc=2)
# #plt.gca().set_ylabel("Magnitude")

# Y = catalogue_uh.data['year']
# max_year = np.max(Y)
# min_year = np.min(Y)
# plt.ylim((3,6.5))

# bins = np.arange(min_year - .5, max_year + 1.5, 1)

# ax2 = plt.gca().twinx()
# ax2.hist(catalogue.data['year'],
#   bins=bins,
#   histtype='step',
#   linestyle='dashed',
#   linewidth=4,
#   color='0.70',
#   normed=True,
#   cumulative=True,
#   label="M > 3")


# _c = deepcopy(catalogue_uh)
# _idx = _c.data['magnitude'] >= 4
# _c.purge_catalogue(_idx)

# ax2.hist(_c.data['year'],
#   bins=bins,
#   histtype='step',
#   linestyle='dashed',
#   linewidth=4,
#   color='0.50',
#   normed=True,
#   cumulative=True,
#   label="M > 4")


# # _c = deepcopy(catalogue_uh)
# _idx = _c.data['magnitude'] >= 5
# _c.purge_catalogue(_idx)

# ax2.hist(_c.data['year'],
#   bins=bins,
#   histtype='step',
#   linestyle='dashed',
#   linewidth=4,
#   color='0.1',
#   normed=True,
#   cumulative=True,
#   label="M > 5")

# ax2.set_ylabel("Normalized cumulative distribution")


# plt.xlim((1850,max_year))

# m3_line = Line2D([], [], color='0.7', 
#                         linestyle='dashed',
#                         linewidth=4,
#                         marker='', 
#                         markersize=15, 
#                         label='M > 3')

# m4_line = Line2D([], [], color='0.4',  
#                         linestyle='dashed',
#                         linewidth=4,
#                         marker='', 
#                         markersize=15, 
#                         label='M > 4')

# m5_line = Line2D([], [], color='0.1',  
#                         linestyle='dashed',
#                         linewidth=4,
#                         marker='', 
#                         markersize=15, 
#                         label='M > 5')

# ax2.legend(handles=[m3_line, m4_line, m5_line],
#   loc=2, bbox_to_anchor=(0, 0.83))

# plt.ylim(0, 1)

plt.show()


if savefig: 
  basemap1.savemap("/Users/pirchiner/Desktop/teste.pdf", 
    filetype='pdf')


exit()
# create_stepp_plot(model=completeness_algorithm,
#   # filename="../z_img_completeness_temporal_stepp.pdf", 
#   show=True,
#   title='Stepp plot [$\Delta_{mag}=0.5, \Delta_{time}=2$]',
#   filetype='pdf', 
#   # figsize=DEFAULT_SIZE, 
#   dpi=300,
#   legendoffset=(1.0, 1.0)
#   )

plt.show()




# # -*- coding: utf-8 -*-

# ### 
# ###    Imports 
# ###

# # Python Numerical and Plotting Libraries
# import pickle
# import numpy as np
# import matplotlib.pyplot as plt
# #plt.xkcd()

# # HMTK Catalogue Import/Export Libraries
# from hmtk.parsers.catalogue.csv_catalogue_parser import CsvCatalogueParser, CsvCatalogueWriter

# # HMTK Plotting Tools
# from hmtk.plotting.seismicity.catalogue_plots import (plot_depth_histogram,
#                                                       plot_magnitude_time_scatter,
#                                                       plot_magnitude_time_density,
#                                                       plot_magnitude_depth_density,
#                                                       plot_observed_recurrence)
# from hmtk.plotting.mapping import HMTKBaseMap
# print 'Imports OK!'


### 
###    Map Config 
###

map_dpi = 150
add_geology = False
add_sourcemodel = False
savefig=False

#map_title = 'Brazilian Seismic Zones'
map_title = 'Earthquake epicenters on the BSB2014.11 catalog'
#map_title = 'ISC-GEM Catalogue'
#map_title = 'South-American Lithology'

# Configure the limits of the map and the coastline resolution
map_config = {'min_lon': -80.0, 'max_lon': -30.0, 'min_lat': -37.0, 'max_lat': 14.0, 'resolution':'l'}
#map_config = {'min_lon': -72.0, 'max_lon': -68.0, 'min_lat': -22.0, 'max_lat': -18.0, 'resolution':'l'}
#map_config = {'min_lon': -95.0, 'max_lon': -25.0, 'min_lat': -65.0, 'max_lat': 25.0, 'resolution':'l'}

# #central
# map_config = {'min_lon': -60.0, 'max_lon': -46.0, 'min_lat': -24.0, 'max_lat': 6.0, 'resolution':'l'}
# #SE
# map_config = {'min_lon': -52.0, 'max_lon': -36.0, 'min_lat': -32.5, 'max_lat': -13.0, 'resolution':'l'}
# #MT
# map_config = {'min_lon': -60.0, 'max_lon': -55.0, 'min_lat': -15.0, 'max_lat': -10.0, 'resolution':'l'}
# #AM
# map_config = {'min_lon': -65.0, 'max_lon': -55.0, 'min_lat': -07.0, 'max_lat': 4.0, 'resolution':'l'}
# #NE
# map_config = {'min_lon': -43.0, 'max_lon': -33.0, 'min_lat': -15, 'max_lat': -1.5, 'resolution':'l'}
# #AC
# map_config = {'min_lon': -75.0, 'max_lon': -68.0, 'min_lat': -13.0, 'max_lat': -4.0, 'resolution':'l'}





basemap1 = HMTKBaseMap(map_config, map_title, dpi=map_dpi)
basemap1.add_catalogue(catalogue, linewidth=1., alpha=0.5)

#basemap1.add_colour_scaled_points(x, y, np.log(z+1), overlay=True)

if savefig: basemap1.savemap("/Users/pirchiner/Desktop/teste.pdf")


plt.show()
