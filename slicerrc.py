#fb_viewr_dir='K:/ProjectSpace/austin_py_2019118/'
fb_viewr_dir='/Users/ak457/Documents/FiberCompareView'
execfile(fb_viewr_dir+'TwoStrainView.py')
execfile(fb_viewr_dir+'ThreeStrainView.py')
execfile(fb_viewr_dir+'FourStrainView.py')
execfile(fb_viewr_dir+'FiveStrainView.py')
execfile(fb_viewr_dir+'FiberBundle_Setup.py')
execfile(fb_viewr_dir+'findNode.py')

# This is per study really... Gotta do better than this in the future.
slicer.util.loadTransform("k:/ProjectSpace/austin_py_2019118/trk_to_vol_space.h5")

