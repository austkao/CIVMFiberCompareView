# Script to load data in orderded fashino for SetUpFiberBundle
# james cook
def StrainDataLoad(packDir,strList,imPat,trkPat):
  # packDir should be full of independent collections of data (RUNNO's at civm)
  # strList is a listing of things in packDir
  #
  # if your structure is more complicated slip additional path levels into strList	
  # eg, N1235, N2345 becomes StrainA/N1235, StrainB/N2345
  # imPat is a regular expression to match the images
  # trkPat is a regular expression to match the tracks to load.
  #
  # Tracks are stored beneath the strListdir in trk/ATLASNAME
  # AtlasName is WHS for now but will change, so we should use first found dir for now
  # we'll probably add it as an input option later.
  # 
  # This whole mess is begging to have an actual object defined, detailing what a
  # bundle of data is, which would containe the selection machinery.
  
  # hints
  # dir listing
  # files = [f for f in os.listdir('.') if re.match(r'[0-9]+.*\.jpg', f)]
  # dir listing 2
  # relevant_path = "[path to folder]"
  # included_extensions = ['jpg','jpeg', 'bmp', 'png', 'gif']
  # file_names = [fn for fn in os.listdir(relevant_path)
  #               if any(fn.endswith(ext) for ext in included_extensions)]
  
  # Input Checking
  if not os.path.isdir(packDir):
    return
  # in case of madness cleanup packDir
  # .replace() all backslashes with forwardslashes
  #packDir=packDir.replace("\\\\","\\")
  #packDir=packDir.replace("\\","/")
  # This windowify your path when on widnows, which you might think is good, however, varios py code fails with win style paths... Seriously.
  # packDir=os.path.normpath(packDir)
  
  sutil = slicer.util
  import re
  
  for packName in strList:
    # if we've got dir info coded into strList we gotta clean that out.
    dataPak=os.path.join(packDir, packName)#.replace("\\","/")
    if not os.path.isdir(dataPak):
      print("Bad pak specified"+dataPak)
      return
    # in many cases this will just be re-assigning the same thing back to the var
    packName=os.path.basename(dataPak)
    
    # get any track dirs
    trkD=os.path.join(dataPak,"trk")#.replace("\\","/")
    packTrks= os.listdir(trkD)
    if len(packTrks)==0:
      print("No trk files in "+trkD+" cannot continue!")
      return
    packTrk=packTrks[0]
    print("trk sel:"+packTrk)
    packTrk=os.path.join(trkD,packTrk)
    if len(packTrks)>1:
      print("Mutliple trk dirs found! Just using first, We need to do better!")
    
    # set img regex and look for img, we should be constrained enough to only find 1.
    imgs = [f for f in os.listdir(dataPak) if re.match(r''+packName+imPat+'', f)]
    
    # set trk regex and look for trk, again we should be constrained enough to only find 1.
    trks = [f for f in os.listdir(packTrk) if re.match(r''+packName+trkPat+'', f)]

    # find transform file in trk folder to put the trks in alignment with the images
    trk_t = [f for f in os.listdir(packTrk) if re.match(r''+packName+'.*([aA]ffine|[rR]igid.*)?[.](h5|mat|txt)', f)]

    if not (len(imgs) == 1) and not (len(trks) == 1):
      print("Bad data for "+packName+" imgs:"+len(imgs)+" trks:"+len(trks))

    if len(trk_t)>1:
      print("Multi-choice track transforms, We're gonna abort")
      return
    
    sutil.loadVolume(os.path.join(dataPak,imgs[0]))
    sutil.loadFiberBundle(os.path.join(packTrk,trks[0]))
    if len(trk_t)==1:
      sutil.loadTransform(os.path.join(packTrk,trk_t[0]))
  
  return
  #sutil.loadVolume("/Users/ak457/DiffusionDisplayTestData/BTBR_N54811/N54811_fa_RAS.nii.gz")
  #sutil.loadVolume("/Users/ak457/DiffusionDisplayTestData/C57_N54790/N54790_fa_RAS.nii.gz")
  #sutil.loadFiberBundle("/Users/ak457/DSI studio testing/DSI studio BAD/N54790_C57/N54790_C57_symmetric_R_labels_RAS_121.vtk")
  #sutil.loadFiberBundle("/Users/ak457/DSI studio testing/DSI studio BAD/N54811_BTBR/N54811_BTBR_symmetric_R_labels_RAS_121.vtk")
  
  #sutil.loadScene("/Users/ak457/Documents/2019-10-29-Scene.mrml")
  #sutil.loadTransform("/Users/ak457/Documents/LinearTransform_3.h5")