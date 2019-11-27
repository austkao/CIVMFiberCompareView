
if os.name=='nt':
  packDir='K:\\ProjectSpace\\FiberCompareView\\ex_testdata'
  strList=["N57147","N57149"]
  packDir='K:\\ProjectSpace\\FiberCompareView\\TestData'
  strList=["DB2\\N54781","BTBR\\N54817"]
else:
  packDir='/Users/ak457/DiffusionDisplayTestData/'
  strList=["DB2/N54781","BRBR/N54817"]
imPat=".*_fa.*[.]nii([.]gz)?$"
# set up is one roi at a time
#N=76
#N=119
N=38
trkPat=".*ROI_"+str(N)+"_.*[.]vtk([.]gz)?$"
volumeNodes=StrainDataLoad(packDir,strList,imPat,trkPat,True)
volProp=os.path.join(packDir,"FARenderVolumeProperty.vp")
if volumeNodes is not None:
  SetUpFiberBundle([1,2],None,volProp)
else:
  print("Trouble loading")

