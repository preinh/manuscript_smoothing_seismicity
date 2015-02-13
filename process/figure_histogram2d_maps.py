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

project_home = "."
_model = "background"

config = {
#    'catalog': project_home + "/data/catalogs/hmtk_bsb2013.csv",
    'catalog': project_home + "/hmtk_bsb2014.11_uniform_assump.csv",
#    'declustered_catalog': project_home + "/"+_model+"/catalogs/bsb2014.11_declustered_catalog.csv",
    #'source_model': project_home + "/"+_model+"/raw/"+_model+"_bsb2014.11_geometries.xml",
    'map_config': {'min_lon': -80.0, 'max_lon': -30.0, 'min_lat': -37.0, 'max_lat': 13.0, 'resolution':'l'},
    'nbins': 25,
    # BR_Geral
    # 'fixed_completeness1' : np.array([[2014., 3.16],
    #                                   [1980., 4.28],
    #                                   [1968., 4.85],
    #                                   [1962., 6.0],
    #                                   [1940., 6.5]]),

    # # pirchiner_simplificado
    # 'fixed_completeness2' : np.array([[2014., 3.0],
    #                                   [1975., 3.8],
    #                                   [1960., 4.8],
    #                                   [1938., 6.5]]),

}

# reading
parser = CsvCatalogueParser(config['catalog'])
catalogue = parser.read_file()
print 'Input complete: %s events in catalogue' % catalogue.get_number_events()
print 'Catalogue Covers the Period: %s to %s' % (catalogue.start_year,
    catalogue.end_year)

observation_time = catalogue.end_year - catalogue.start_year + 1

# Sort catalogue chronologically
catalogue.sort_catalogue_chronologically()
print 'Catalogue sorted chronologically!'

# 3.0 - 0.3 uncertainty
min_mag = 3.0
# filter magnitudes Mw lower than 3.0


map_dpi = 120
add_geology = False
add_sourcemodel = False
savefig=True

#map_title = 'Brazilian Seismic Zones'
map_title = u'a-value [hist2D, 2.0$^o$, b=1, Assump. compl.]'
#map_title = 'ISC-GEM Catalogue'
#map_title = 'South-American Lithology'

# Configure the limits of the map and the coastline resolution
map_config = {'min_lon': -80.0, 'max_lon': -30.0, 'min_lat': -37.0, 'max_lat': 14.0, 'resolution':'l'}
#map_config = {'min_lon': -72.0, 'max_lon': -68.0, 'min_lat': -22.0, 'max_lat': -18.0, 'resolution':'l'}
#map_config = {'min_lon': -95.0, 'max_lon': -25.0, 'min_lat': -65.0, 'max_lat': 25.0, 'resolution':'l'}



basemap1 = HMTKBaseMap(map_config, map_title, dpi=map_dpi)
#basemap1.add_catalogue(catalogue, linewidth=1., alpha=0.5)




_c = deepcopy(catalogue)
# _c.catalogue_mt_filter(config['fixed_completeness2'], reverse=True)
# _c.catalogue_mt_filter(completeness_table_stepp, reverse=True)

basemap1.add_size_scaled_points(_c.data['longitude'], 
                                 _c.data['latitude'],
                                 np.exp(_c.data['magnitude']-3),
                                 edgecolor='gray',
                                 facecolor='none',
                                 alpha=0.7,
                                 linewidth=1,
                                 color='red',
                                 overlay=True)

# count EQ in bins: histo_2D
heatmap, xedges, yedges = np.histogram2d(catalogue.data['longitude'], 
  catalogue.data['latitude'], bins=(config['nbins'], config['nbins']),
  normed=False)


#limits of image
extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

_lambda = heatmap.T / observation_time
_m_min = min(catalogue.data['magnitude'])
_b_value = 1.0

a_value = np.log10(_lambda) + _b_value*_m_min
#_data = np.log10(a_value)

# plot image and colorbar
_ax = plt.imshow(a_value, 
             origin='low', 
             extent=extent,
#             cmap=plt.cm.Reds,
             cmap=plt.cm.RdYlGn_r,
             interpolation='nearest',
             vmin=-0.5, vmax=2.5,
             )
_cb = plt.colorbar(_ax, extend='both')
_cb.set_label('a-value', fontsize='small')





plt.show()


if savefig: 
  basemap1.savemap("/Users/pirchiner/Desktop/z_img_2dhist_assump_%d.pdf"%config['nbins'], 
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
