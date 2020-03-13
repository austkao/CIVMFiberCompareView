# New class definition of a data package
# Author: Austin Kao

import os
import re

class DataPackage:
  #Contains several useful dictionaries
  #volDict: Key is string ID, value is a tuple of (filepath, node, filename)
  #tractDict: Key is ROI number, value is a tuple of (filepath, node, region name)
  #transformList: List of each transform that needs to be used for the specimen
  #labelDict: Key is ROI number, value is a tuple of (region name, number 1, number 2, number 3)
  #The three numbers that are contained within the tuple are the numeric values found in the lookup table
  #tractDict node is vtkMRMLFiberBundleNode class
  #use GetLineDisplayNode() and GetTubeDisplayNode() to get vtkMRMLFiberBundleLineDisplayNode and vtkMRMLFiberBundleTubeDisplayNode
  
  def __init__(self, packName, labelPath):
    self.packName = packName
    self.volDict = dict()
    self.tractDict = dict()
    self.transformList = []
    self.labelDict = dict()
    transformExts='[.](h5|mat|txt)'
    packDir='/Users/ak457/DiffusionDisplayTestData/'
    #packDir='/Volumes/ak457/DiffusionDisplayTestData/'
  
    # packDir should be full of independent collections of data (RUNNO's at civm)
    # strList is a listing of things in packDir
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
    # Should return ... things? maybe list of volumeNodes?
    #fiberNodes=Set([])
    #dataPacks=Set([])
    #dataDict=dict()
    # if we've got dir info coded into strList we gotta clean that out.
    dataPak=os.path.join(packDir, packName)
    if not os.path.isdir(dataPak):
      print("Bad pak specified"+dataPak)
      return
  
    txt = open(os.path.join(packDir, labelPath))
    for line in txt:
      words = line.split(' ')
      if words[0] is not "#" and len(words) > 1:
        self.labelDict[int(words[0])] = (words[1],words[2],words[3],words[4])
    # in many cases this will just be re-assigning the same thing back to the var
    packName=os.path.basename(dataPak)
  
    # check if we have a transform dir and bail if we asked for one but didnt find
    trLinkD=os.path.join(dataPak,"transforms")
    if not os.path.isdir(trLinkD):
      print("Missing requested transform dir",trLinkD)
  
    # get any track dirs
    trkD=os.path.join(dataPak,"trk")
    packTrks= os.listdir(trkD)
    #print(packTrks)
    if len(packTrks)==0:
      print("No trk files in "+trkD+" cannot continue!")
      return
    packTrk=packTrks[0]
    # print("trk sel:"+packTrk)
    packTrk=os.path.join(trkD,packTrk)
    if len(packTrks)>1:
      print("Mutliple trk dirs found! Just using first, We need to do better!")
  

  
    # set trk regex and look for trk, again we should be constrained enough to only find 1.
  

    # find transform file in trk folder to put the trks in alignment with the images
    trk_t = [f for f in os.listdir(packTrk) if re.match(r''+packName+'.*([aA]ffine|[rR]igid.*)?'+transformExts, f)]

    if len(trk_t)>1:
      print("Multi-choice track transforms, We're gonna abort")
      return
    if len(trk_t)==1:
      self.transformList.append((os.path.join(packTrk,trk_t[0]), None))
    # Should check if data are loaded here and skip if they are
    #[loadSuccess, volumeNode]=sutil.loadVolume(os.path.join(dataPak,imgs[0]),True)
  
    #Useful methods: slicer.util.GetNode(), slicer.util.setSliceViewerLayers()
    #print "LoadVol",os.path.join(dataPak,imgs[0])
    volNames = ["fa", "color_nqa", "dwi", "gfa", "nqa"]
    for i in range(len(volNames)):
      imPat=".*_" + str(volNames[i]) + ".*[.]nii([.]gz)?$"
      # set img regex and look for img, we should be constrained enough to only find 1.
      imgs = [f for f in os.listdir(dataPak) if re.match(r''+packName+imPat+'', f)]
      if not (len(imgs) == 1):
        print("Bad data for ",imPat," imgs:",len(imgs))
      print(imPat)
      print(len(imgs))
      if len(imgs) == 1:
        volPath = os.path.join(dataPak,imgs[0])
        fileName = imgs[0].replace(".nii.gz","")
        self.volDict[volNames[i]] = (volPath, None, fileName)
    for N in range(1,167):
      sides=[0,1000]
      for side in sides:
        trkPat=".*ROI_"+str(N+side)+"_.*[.]vtk([.]gz)?$"
        trk = [f for f in os.listdir(packTrk) if re.match(r''+packName+trkPat+'', f)]
        if(len(trk)>1):
          print("More than one track: Size "+str(len(trk)))
        elif(len(trk)==0):
          continue
        trkPath = os.path.join(packTrk,trk[0])
        self.tractDict[N+side] = (trkPath, None, self.labelDict[N+side][0])
      # Simplisitic first version assuming that there is only one transform set FROM our data to someplace else.
      # In the future we can check if atlasTransform is a string, and if it's specifiying our target.
      #print("loading additional transforms from",trLinkD,"\n\tto:");
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
    #print "Load additional link transforms:"
    for tn in range(len(chainTransformLinks)):
      tformName=chainTransformLinks[tn]
      print "  "+tformName
      self.transformList.append((os.path.join(trLinkD,tformName), None))
  
  # Get the name of the package (is equal is packName in the constructor)  
  def getName(self):
    return self.packName
  
  # Get the 3D FA volume node contained in the package  
  def getVolumeNode(self):
    return self.volDict["fa"][1]
  
  def getVolumePath(self):
    return self.volDict["fa"][0]
    
  def getGeneralVolumeNode(self, filename):
    for key in self.volDict:
      if self.volDict[key][2] == filename:
        return self.volDict[key][1]
    return False
  
  def getGeneralVolumePath(self, filename):
    for key in self.volDict:
      if self.volDict[key][2] == filename:
        return self.volDict[key][0]
    return None
  
  def addGeneralVolume(self, volNode, filename):
    for key in self.volDict:
      if self.volDict[key][2] == filename:
        self.volDict[key] = (self.volDict[key][0], volNode, self.volDict[key][2])
  
  def getTractNode(self, trkNum):
    if not self.tractDict.has_key(trkNum):
      return None
    return self.tractDict[trkNum][1]
  
  def getTractPath(self, trkNum):
    if not self.tractDict.has_key(trkNum):
      return None
    return self.tractDict[trkNum][0]
  
  def getTractName(self, trkNum):
    if not self.tractDict.has_key(trkNum):
      return None
    return self.tractDict[trkNum][2]
  
  def getVolumes(self):
    return self.volDict
  
  def getTracts(self):
    return self.tractDict
  
  def getTransforms(self):
    return self.transformList
  
  def getLabels(self):
    return self.labelDict
  
  def addVolume(self, volNode):
    self.volDict["fa"] = (self.volDict["fa"][0], volNode, self.volDict["fa"][2])
  
  def addTract(self, tractNode, roi):
    self.tractDict[roi] = (self.tractDict[roi][0], tractNode, self.tractDict[roi][2])
