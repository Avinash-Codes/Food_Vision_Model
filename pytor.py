from mayavi import mlab
import numpy as np
import scipy.interpolate as interp

def make_simple_3Dplot( data2plot, xVals, yVals, zVals, N_contLevels=8, fname_plot='' ):

    contLevels  = np.linspace( np.amin(data2plot), 
                               np.amax(data2plot),
                               N_contLevels)[1:].tolist()
    fig1    = mlab.figure( bgcolor=(1,1,1), fgcolor=(0,0,0),size=(800,600))

    XX, YY, ZZ = np.meshgrid(xVals, yVals, zVals, indexing='ij' )
    contPlot = mlab.contour3d( XX, YY, ZZ, 
                               data2plot, contours=contLevels,
                               transparent=True, opacity=.4,
                               figure=fig1
                             )
    mlab.xlabel('x')
    mlab.ylabel('y')
    mlab.zlabel('z')
    mlab.zlabel('data')

    mlab.show()

# define original coordinates
x_min, y_min, z_min = 0, 0, 0
x_max, y_max, z_max = 10, 10, 10
Nx, Ny, Nz = 20, 30, 40
x_arr = np.linspace(x_min, x_max, Nx)
y_arr = np.linspace(y_min, y_max, Ny)
z_arr = np.linspace(z_min, z_max, Nz)

# center of circle
xc, yc, zc = 3, 5, 7

# radius of circle
rc = 2

# define original data
data_3D_original = np.zeros( (Nx, Ny, Nz) )
for ii in range(Nx):
    for jj in range(Ny):
        for kk in range(Nz):
            if np.sqrt((x_arr[ii]-xc)**2 + (y_arr[jj]-yc)**2 + (z_arr[kk]-zc)**2) < rc:
                data_3D_original[ii,jj,kk] = 1.

make_simple_3Dplot( data_3D_original, x_arr, y_arr, z_arr )

# spatial coordinates for interpolation
step_size = np.mean(np.diff(x_arr))/5.
x_interp = np.arange(x_arr[0], x_arr[-1], step_size ) 
y_interp = np.arange(y_arr[0], y_arr[-1], step_size )
z_interp = np.arange(z_arr[0], z_arr[-1], step_size )

# make interpolation function
func_interp = interp.RegularGridInterpolator( (x_arr, y_arr, z_arr), data_3D_original )

# make coordinates for interpolation, first transform vectors for coordinates
# into column vectors and then stack them together 
points = np.hstack( (x_interp[...,None], y_interp[...,None], z_interp[...,None]) )

data_3D_interp = func_interp(points)

print(data_3D_interp.shape, x_interp.shape, y_interp.shape, z_interp.shape)
