"""

This script is modified from Christan Burlet
24/01/2023: there is a problem in this script. The problem is that the bands are not representing the wavelength.
EDIT 24/01/2023: problem fixed

"""

import xarray as xr
import numpy as np
import skimage.io as skio
import os
import pandas as pd

os.chdir(r"C:\Users\simon\PycharmProjects\automated-mineralogy\libs\Datacubes")
name = "Schm01.tif"
imstack1 = skio.imread(fname = name,
                       plugin = "tifffile")
imstack1 = np.transpose(imstack1, axes=[0, 2, 1])

# If the file originates from a tif file (which is the reason why this script is used :-) )
if name[-3:] == "tif":
    # Find wavelengths for this image
    df = pd.read_excel('Wavelengths_schm01.tif_from_imageJ.xlsx')
    # Convert the wavelengths to an array (in a very non-elegant way)
    wavelengths = df.values.tolist()
    wv = list()
    for w in wavelengths:
        x = str(w[0])
        wv.append(float(x))
    wv = np.array(wv)

# Create a DataArray
# documentation: https://docs.xarray.dev/en/stable/generated/xarray.DataArray.html
if name[-3:] == "tif":
    libs_cube = xr.DataArray(data=imstack1,
                             dims=("bands", "x", "y"),
                             coords = {
                                 "bands": wv
                             })


libs_cube_ds = libs_cube.to_dataset(name='mapping')
print('libs_cube_ds')
print(libs_cube_ds)

libs_cube_ds = libs_cube_ds.mapping.astype('int16')
print('libs_cube_ds')
print(libs_cube_ds)

libs_cube_ds.to_netcdf("Schm01.nc", engine='netcdf4')

