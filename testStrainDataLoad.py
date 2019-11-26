
if os.name=='nt':
  packDir='K:\\ProjectSpace\\FiberCompareView\\ex_testdata'
  strList=["N57147","N57149"]
else:
  packDir='/Users/ak457/DiffusionDisplayTestData/'
  strList=["N54781","N54817"]
imPat=".*_fa.*[.]nii([.]gz)?$"
# set up is one roi at a time
#N=76
#N=119
N=38
trkPat=".*ROI_"+str(N)+"_.*[.]vtk([.]gz)?$"
StrainDataLoad(packDir,strList,imPat,trkPat)
SetUpFiberBundle([1,2])
