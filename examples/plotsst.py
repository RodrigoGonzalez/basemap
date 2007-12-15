from matplotlib.toolkits.basemap import Basemap, NetCDFFile
import pylab, numpy
# read in sea-surface temperature and ice data
# can be a local file, a URL for a remote opendap dataset,
# or (if PyNIO is installed) a GRIB or HDF file.
ncfile = NetCDFFile('http://nomads.ncdc.noaa.gov:8085/thredds/dodsC/oisst/2007/AVHRR/sst4-navy-eot.20071213.nc')
# read sst.  Will automatically create a masked array using
# missing_value variable attribute.
sst = ncfile.variables['sst'][:]
# read ice.
ice = ncfile.variables['ice'][:]
# read lats and lons (representing centers of grid boxes).
lats = ncfile.variables['lat'][:]
lons = ncfile.variables['lon'][:]
# shift lats, lons so values represent edges of grid boxes
# (as pcolor expects).
delon = lons[1]-lons[0]
delat = lats[1]-lats[0]
lons = (lons - 0.5*delon).tolist()
lons.append(lons[-1]+delon)
lons = numpy.array(lons,numpy.float64)
lats = (lats - 0.5*delat).tolist()
lats.append(lats[-1]+delat)
lats = numpy.array(lats,numpy.float64)
# create Basemap instance for mollweide projection.
# coastlines not used, so resolution set to None to skip
# continent processing (this speeds things up a bit)
m = Basemap(projection='moll',lon_0=lons.mean(),lat_0=0,resolution=None)
# compute map projection coordinates of grid.
x, y = m(*numpy.meshgrid(lons, lats))
# draw line around map projection limb.
# color background of map projection region.
# missing values over land will show up this color.
m.drawmapboundary(fill_color='0.3')
# plot ice, then with pcolor
im1 = m.pcolor(x,y,sst,shading='flat',cmap=pylab.cm.jet)
im2 = m.pcolor(x,y,ice,shading='flat',cmap=pylab.cm.gist_gray)
# draw parallels and meridians, but don't bother labelling them.
m.drawparallels(numpy.arange(-90.,120.,30.))
m.drawmeridians(numpy.arange(0.,420.,60.))
# draw horizontal colorbar.
pylab.colorbar(im1,orientation='horizontal')
# display the plot.
pylab.show()