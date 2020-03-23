#!/bin/bash

now=`date +%Y%m%d`
if [ -d data ]; then
    mkdir data
fi
cd data
# ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod/rtofs.20200229/
for comp in u v; do
   for ts in 024 048; do
       wget ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod/rtofs.${now}/rtofs_glo_3dz_f${ts}_daily_3z${comp}io.nc
   done
done
