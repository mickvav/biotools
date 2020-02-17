#!/usr/bin/env python3
"""
Some docstring
"""
import netCDF4
import numpy as np
from functools import lru_cache
from math import radians, degrees, sin, cos, asin, acos, sqrt


fu = netCDF4.Dataset('../rtofs_glo_3dz_f024_daily_3zuio.nc')
fv = netCDF4.Dataset('../rtofs_glo_3dz_f024_daily_3zvio.nc')


fu_x = fu.variables['X']
print("FU:")
print(
    fu.variables['X'].shape[0],
    fu.variables['Y'].shape[0],
    fu.variables['Depth'].shape[0],
    fu.variables['Latitude'].shape[0],
    fu.variables['Latitude'].shape[1],
)
print("FV:")
print(
    fv.variables['X'].shape[0],
    fv.variables['Y'].shape[0],
    fv.variables['Depth'].shape[0]
)

def great_circle(lon1, lat1, lon2, lat2):
    """
    credit - https://medium.com/@petehouston/calculate-distance-of-two-locations-on-earth-using-python-1501b1944d97
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    return 6371 * (
        acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon1 - lon2))
    )

@lru_cache(maxsize=300)
def find_stupid(lat, lng, depth, step):
    d0=100000
    ds=0
    dis = 0
    for di in range(0,fu.variables['Depth'].shape[0]):
        d = fu.variables['Depth'][di]
        if abs(depth - d) < d0:
            d0=abs(depth - d)
            ds=d
            dis = di
    Distance = 100000000
    xs = 0
    ys = 0
    lats = 0
    lngs = 0
    xmax = fu.variables['Latitude'].shape[0]
    ymax = fu.variables['Latitude'].shape[1]
    for x in range(0,xmax,step):
        for y in range(0,ymax,step):
            ilat = fu.variables['Latitude'][x,y]
            ilng = fu.variables['Longitude'][x,y]
            D1 = great_circle(lng,lat, ilng, ilat)
            if D1 < Distance:
                Distance = D1
                xs = x
                ys = y
                lats = 0
                lngs = 0
    s2=int(step/2)
    x_range = list(range(max(xs-s2,0),min(xs+s2,xmax)))
    if(xs<s2):
        x_range += list(range(xmax+xs-s2, xmax))
    if(xs>xmax-s2):
        x_range += list(range(0, xmax-xs))
    y_range = list(range(max(ys-s2,0),min(y+s2,ymax)))
    if(ys<s2):
        y_range += list(range(ymax+ys-s2, ymax))
    if(ys>ymax-s2):
        y_range += list(range(0, ymax-ys))

    for x in x_range:
        for y in y_range:
            ilat = fu.variables['Latitude'][x,y]
            ilng = fu.variables['Longitude'][x,y]
            D1 = great_circle(lng,lat, ilng, ilat)
            if D1 < Distance:
                Distance = D1
                xs = x
                ys = y
                lats = 0
                lngs = 0
    return (dis, xs, ys, ds, lats, lngs, Distance )

f=open("SraRunTable.txt_filtered.txt", "r")
g=open("SraRunTable.txt_filtered_added_uv.txt", "w")
header = f.readline().strip().split(",")
new_header = header + ["Depth_uv","Lat_uv","Lng_uv", "Distance", "u", "v"]
g.write(",".join(new_header) + "\n")

for line in f.readlines():
    d = {h : v for h,v in zip(header, line.strip().split(","))}
    try:
        (dis, xs, ys, ds, lats, lngs, Distance) = find_stupid(
            lat=float(d["Latitude_Start"]),
            lng=float(d["Longitude_Start"]),
            depth=float(d["Depth"]),
            step=64
        )
    except ValueError as e:
        print(f"Error: {e}. Skipping line {line}")
        continue
    u=fu.variables['u'][0,dis,xs,ys]
    v=fv.variables['v'][0,dis,xs,ys]
    d["Depth_uv"] = str(fu.variables["Depth"][dis])
    d["Lat_uv"] = str(lats)
    d["Lng_uv"] = str(lngs)
    d["Distance"] = str(Distance)
    d["u"] = str(u)
    d["v"] = str(v)
    line1 = ",".join([d[i] for i in new_header]) + "\n"
    print(line1)
    g.write(line1)

    
