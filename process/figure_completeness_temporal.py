# -*- coding: utf-8 -*-
# Python Numerical and Plotting Libraries
import numpy as np
import matplotlib.pyplot as plt
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
    'fixed_completeness1' : np.array([[2014., 3.5],
                                   [1980., 4.5],
                                   [1968., 5.0],
                                   [1962., 6.0],
                                   [1940., 7.0]]),

    # pirchiner_simplificado
    'fixed_completeness2' : np.array([[1985., 2.0],
                                      [1975., 3.0],
                                      [1960., 4.0],
                                      [1900., 6.0]]),

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
min_mag = 2.0
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
           'time_bin': 2.0,
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
plot_magnitude_time_scatter(catalogue_uh,
  # completeness_table=config['fixed_completeness2'],
  # completeness_table=completeness_table,
  fmt_string='k+',
  color='SkyBlue',
  # color='orange',
  # filename="../z_img_completeness_temporal_scatter_fixed.pdf", 
  # filetype='pdf', 
  dpi=300,
  figsize=(9, 4),
  overlay=True)

completeness_table=config['fixed_completeness2']
plt.step(completeness_table[:,0], completeness_table[:,1], 
  where='post', 
  linewidth=4,
  color='Navy',
  label="Simplified")

completeness_table=completeness_table_stepp
plt.step(completeness_table[:,0], completeness_table[:,1], 
  where='post',
  linewidth=2,
  color = 'red',
  label="Stepp")


plt.legend(loc=2)
plt.show()

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
