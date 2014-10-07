


1- Comentario general: Lo que has escrito mas que la state-of-the-art y/o la descripción de un modelo de PSHA es mas bien una proyección futura de lo que se piensa hacer en Brazil con respecto a esta temática: grupo PSHAB, mapa de PSHA a nivel nacional para el 2015.

Como state-of-the-art yo mencionaria para Brazil: 
    a) GSHAP: No es un estudio local, pero tengo entendido que  la norma sismica (NBR-14421, mira el adjunto) esta utilizando este mapa.
    b) Dourado (2014) : aunque no este publicado
    c) tu trabajo de maestria 
    d) y algun trabajo a nivel sub-nacional: Ferreira, J, Juliá, J (unpublished) [Zone Sources, CRISIS, NE’s Brazil]
Con esto damos una buena vision del state-of-the-art, pienso...

2- En A.5 (en el Appendix A en general) estamos tratando de describir modelos de PSHA, lo que has escrito esta bien, pero debemos ser mas especificos. Te propongo que tomes un modelo "particular" (preferentemente el tuyo ) y lo describas adecuadamente. Esto seria bien interesante porque GSHAP uso un algoritmo "parecido" (Veneziano et al.) para obtener los resultados en tu pais. Y como me has ya mostrado tus resultados son similares (mas buenos!).


#### Smoothing seismicity to Brazilian PSHA (Pirchiner, 2014) 

### 1. Earthquake catalogue and seismicity processing

This model was produced with the Brazilian Seismic Bulletin (BSB), 2013.08 version,
which is public available at http://www.moho.iag.usp.br/portal/events#catalog under CC-BY licence.
This catalog is mantainded by University of São Paulo (USP).

Almost magnitude values are in the mb scale. No corrections or proxies was applied to get an Mw magnitude value.
This should be corrected in the future.


### 2. Source models definition

The result of the smoothing process is a grid of point sources.
In each point of the grid a smoothed seismicity rate value is assigned. 
For each point a MFD is characterized by the given seismicity rate (a-value), 
the magnitude limits (assigned 3 and 7 for the minimum and maximum respectively)
and a properly b-value choosen 1 (global average) for this model.

The depth distribution considered for all sources was a simple value of 10km with 0 and 20km of upper and lower
seismicity boudaries. Almost earthquakes in the catalogue has no accurated data value.

The nodal plane distribution used for all sources was made assigning 0.25 probability f
or each 0, 90, 180, 270 strike of a dip 45 and rake 90 rupture plane.

The magnitude-area scale relationshp defined for all sources was the writen by Wels-Coppersmith.
 

### 3. Activity rates calculation
The smoothed seismicity rate was computed following the Helmstetter2012 background seismicity for long-term forecast.

The learning catalog contain events from 1960 to 2010. The target catalog comes from 2003 to the end of the catalog (2013) 
plus the early-1960 by the small number of the intraplate events in Brazil. 

The smoothing seismicity model proposed by Helmstetter computes a gausian kernel in the time dimension and a bidimensional gaussian or power-law 
kernel to the space dimension. The local adaptive bandwith of booth kernels for each earthquake in the learning catalog is computed by the proposed coupled nearest neighbour optimization.

Even this smoothing method allow a weigth for completeness space-time variation, this parameter was not used in this case and the magnitude completeness used was the same for all grid. Since the NE and SE seismicity is very increased by low magnitude events in comparision with all the country, the minimum magnitude used for the learning catalog was 3.8.

Using these parameters the optimization of the lakelihood between the model learned prediction and the target observed seismicity,
gives the optimized parameters for the coupled nearest neighbour method and the minimum seismicity rate applied to all the sources in the sense to allow earthquakes occurring at locations that never occurred before.

Since the seismicity rate at the cell is computed by the median of the seismicity rate temporal model located at its center point, the decluster process was not necessary.

The initial grid spacing was definied by 1 degree, but taking sense of area source discretization tests, wich shows high fluctuation on hazard values using discretization distances equal to 20km, the grid was densificated to aproximate 15km. 

### 4. GMPE’s selection

This work was focused on proove the concept of smoothing seismicity and did not much attention to GMPE selection criterias.
For convenience and easy comparision Toro1997 was used as default GMPE.


### 5. Dealing with uncertainties.

For the same reason mentioned above, also uncertainties was not handled as possible and just one source model branch and level was used to perform hazard calculation.

### 6. Calculation setting and PSHA code used

The hazard calculation was computed by openquake-engine, using almost _default_ parameters.

For the earthquake rupture forecast the rupture mesh spacing was setted up to 2km and the bin of MFD was setted up on 0.2 magnitude unit.

The site parameters used on the calculation was 600 km/s to Vs30. The depth with 2.5 km/s and 1.0 km/s was definet in 5 and 100km.

The grid of sites was defined from -80,-37 to -30,+14 divided in slots of 50km.





### Introduction

Brazil do not have any recent study on seismic hazard made in national scale.

But seismologists and engineers are working together in a called 'PSHAB group' to produce one, even preliminarily, before April, 2015.

This construction is trying to follow the best practices on National Hazard Maps building process, and hopefully it would be referred in the SARA context as the Brazilian state of art hazard model on intraplate environment. 



### Earthquake catalogue and seismicity processing

The main catalogue resource is the Brazilian Seismic Bulletin available under a Creative Commons licence, in (at writing moment) 2 versions: 2013.08 and 2014.06.

This catalogue represent the best Brazilian compilation of historic and instrumental earthquakes, since it was constructed up to the Brazilian Seismicity (Berrocal et al, 1984) book, used as base of all CERESIS projects carrying on Brazilian data.

One main problem with this catalogue for now, is the magnitude scale. Most of them have not any Mw magnitude value. Instead, almost magnitudes in this catalogue are in mb scale. The last consideration is that the use of global proxies (eg. Scordillis) to convert them will be made carefully because almost earthquakes in this catalogue are lower than lowest applicable value of some proxies. 




### Source models definition [typologies, etc]

Almost sources in current development are been modelling as area sources.

At the PSHAB context, we are strongly suggesting the consideration of 'active faults' even from Saadi compilation or any other dataset from others well-known specialists.

Since a noticed strain study using SIRGAS data in Brazil (Marotta et al), we are also inviting the researchers to produce a seismic point source grid.

Last, some implementations of smoothing seismicity are been consider as another point sources grid.

The seismicity process workflow may changes until the end of project, but in general consists of
 - declustering procedures
 - spatial filter from catalogue into each zone



### Activity rates calculation

 - time-completeness evaluation

 - recurrence (MFD) evaluation (almost using Weichert method)

 - maximum magnitude (almost defined by the specialist)


### GMPE’s selection    

In the general sense, there are not enough strong motion data available to generate a new ground motion model.

The selection process still unfinished and the recommendation is to use Toro1997 GMPE to get hazard poe results.

The final brazilian hazard model should be report the selection procedure.



### Dealing with uncertainties [logic tree]    
As Brazil didn't not complete the hazard modelling procedure, the epistemic uncertainties was not included yet, but was strongly recommended to each modeller involved on the present effort to enumerate their uncertainties to be argued collectively on one of the project phases.


### Calculation setting and PSHA code used
Despite some early tries to build a brazilian hazard model was started on Crisis, they are strongly encouraged to implement this map under OpenQuake.

(Please make comments on it !!!)
