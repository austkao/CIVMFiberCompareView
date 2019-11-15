# slicer rc 
# cobbled together from initial work of austin kao
# adapted to be marginally cross platform

import os

# haphazardly force win paths vs dev user
if os.name=='nt':
  fb_viewr_dir='K:/ProjectSpace/FiberCompareView/'
else:
  fb_viewr_dir='/Users/ak457/Documents/FiberCompareView'
  
execfile(fb_viewr_dir+'TwoStrainView.py')
execfile(fb_viewr_dir+'ThreeStrainView.py')
execfile(fb_viewr_dir+'FourStrainView.py')
execfile(fb_viewr_dir+'FiveStrainView.py')
execfile(fb_viewr_dir+'FiberBundle_Setup.py')
execfile(fb_viewr_dir+'findNode.py')


slicer.util.loadScene(fb_viewr_dir+"/TemplateScene.mrml")
# This is per study really... Gotta do better than this in the future.
slicer.util.loadTransform(fb_viewr_dir+"trk_to_vol_space.h5")

