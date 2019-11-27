# Script to load data in orderded fashino for SetUpFiberBundle
# Not the best name when I think about it,
# Maybe it should be LoadCIVMPackedTrackData ? 
# ... or maybe not.
# james cook
def StrainDataLoad(packDir,strList,imPat,trkPat,atlasTransform=None):
  transformExts='[.](h5|mat|txt)'
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
  
  sutil = slicer.util
  import re
  # Should return ... things? maybe list of volumeNodes?
  volumeNodes=[0 for packName in strList]
  im=0;
  for packName in strList:
    # if we've got dir info coded into strList we gotta clean that out.
    dataPak=os.path.join(packDir, packName)
    if not os.path.isdir(dataPak):
      print("Bad pak specified"+dataPak)
      return
    # in many cases this will just be re-assigning the same thing back to the var
    packName=os.path.basename(dataPak)
    
    # check if we have a transform dir and bail if we asked for one but didnt find
    trLinkD=os.path.join(dataPak,"transforms")
    if atlasTransform is not None and not os.path.isdir(trLinkD):
        print("Missing requested transform dir",trLinkD)
    
    # get any track dirs
    trkD=os.path.join(dataPak,"trk")
    packTrks= os.listdir(trkD)
    if len(packTrks)==0:
      print("No trk files in "+trkD+" cannot continue!")
      return
    packTrk=packTrks[0]
    # print("trk sel:"+packTrk)
    packTrk=os.path.join(trkD,packTrk)
    if len(packTrks)>1:
      print("Mutliple trk dirs found! Just using first, We need to do better!")
    
    # set img regex and look for img, we should be constrained enough to only find 1.
    imgs = [f for f in os.listdir(dataPak) if re.match(r''+packName+imPat+'', f)]
    
    # set trk regex and look for trk, again we should be constrained enough to only find 1.
    trks = [f for f in os.listdir(packTrk) if re.match(r''+packName+trkPat+'', f)]

    # find transform file in trk folder to put the trks in alignment with the images
    trk_t = [f for f in os.listdir(packTrk) if re.match(r''+packName+'.*([aA]ffine|[rR]igid.*)?'+transformExts, f)]

    if not (len(imgs) == 1) or not (len(trks) == 1):
      print("Bad data for ",packName," imgs:",len(imgs)," trks:",len(trks))
      return

    if len(trk_t)>1:
      print("Multi-choice track transforms, We're gonna abort")
      return
    
    # Should check if data are loaded here and skip if they are
    #[loadSuccess, volumeNode]=sutil.loadVolume(os.path.join(dataPak,imgs[0]),True)
    
    #Useful methods: slicer.util.GetNode(), slicer.util.setSliceViewerLayers()
    print "LoadVol",os.path.join(dataPak,imgs[0])
    [loadSuccess,volumeNodes[im]]=sutil.loadVolume(os.path.join(dataPak,imgs[0]),{"Show":False},True)
    [loadSuccess, fiberNode]=sutil.loadFiberBundle(os.path.join(packTrk,trks[0]),True)
    if len(trk_t)==1:
      [loadSuccess, trkToVolTransform]=sutil.loadTransform(os.path.join(packTrk,trk_t[0]), True)
      # fiberNode.ApplyTransformMatrix(trkToVolTransform.GetMatrixTransformToParent())
      fiberNode.SetAndObserveTransformNodeID(trkToVolTransform.GetID())
    if atlasTransform is not None:
      # Simplisitic first version assuming that there is only one transform set FROM our data to someplace else.
      # In the future we can check if atlasTransform is a string, and if it's specifiying our target.
      print("loading additional transforms from",trLinkD,"\n\tto:",atlasTransform);
      chainTransformLinks = [f for f in os.listdir(trLinkD) if re.match(r'^'+packName+'', f)]
      if len(chainTransformLinks)==0:
        print("No transforms packs in "+trLinkD+" cannot continue!")
        return
      elif len(chainTransformLinks)>1:
        print("To many transform packs, Not smart enougth to sort it out")
        return;
      trLinkD=os.path.join(trLinkD,chainTransformLinks[0])
      chainTransformLinks = [f for f in os.listdir(trLinkD) if re.match(r'^_.+'+transformExts, f)]
      chainTransformLinks.sort()
      transformNodes=[0 for tformName in chainTransformLinks]
      print "Load additional link transforms:"
      for tn in range(len(chainTransformLinks)):
        tformName=chainTransformLinks[tn]
        print "  "+tformName
        [loadSuccess, transformNodes[tn]]=sutil.loadTransform(os.path.join(trLinkD,tformName), True)
        if loadSuccess:
          if tn > 0:
            # transformNodes[tn].ApplyTransformMatrix(transformNodes[tn-1].GetMatrixTransformToParent())
            transformNodes[tn-1].SetAndObserveTransformNodeID(transformNodes[tn].GetID())
          else:
            # volumeNodes[im].ApplyTransformMatrix(transformNodes[tn].GetMatrixTransformToParent())
            volumeNodes[im].SetAndObserveTransformNodeID(transformNodes[tn].GetID())
            if len(trk_t)==1:
              # trkToVolTransform.ApplyTransformMatrix(transformNodes[tn].GetMatrixTransformToParent())
              trkToVolTransform.SetAndObserveTransformNodeID(transformNodes[tn].GetID())
            else:
              # fiberNode.ApplyTransformMatrix(transformNodes[tn].GetMatrixTransformToParent())
              fiberNode.SetAndObserveTransformNodeID(transformNodes[tn].GetID())
        else:
          print("error loading ",tformName)
          return
    im+=1
  return volumeNodes
  #sutil.loadVolume("/Users/ak457/DiffusionDisplayTestData/BTBR_N54811/N54811_fa_RAS.nii.gz")
  #sutil.loadVolume("/Users/ak457/DiffusionDisplayTestData/C57_N54790/N54790_fa_RAS.nii.gz")
  #sutil.loadFiberBundle("/Users/ak457/DSI studio testing/DSI studio BAD/N54790_C57/N54790_C57_symmetric_R_labels_RAS_121.vtk")
  #sutil.loadFiberBundle("/Users/ak457/DSI studio testing/DSI studio BAD/N54811_BTBR/N54811_BTBR_symmetric_R_labels_RAS_121.vtk")
  
  #sutil.loadScene("/Users/ak457/Documents/2019-10-29-Scene.mrml")
  #sutil.loadTransform("/Users/ak457/Documents/LinearTransform_3.h5")