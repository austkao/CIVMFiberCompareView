# Function to create a dropdown and populate it
# Will connect one dropdown to number of viewers
# Will connect dropdown to function to change ROIs being displayed on screen
#Useful methods: slicer.util.getNode(), slicer.util.setSliceViewerLayers()

fb_viewr_dir='/Users/ak457/Documents/FiberCompareView/'
#fb_viewr_dir='/Volumes/ak457/Documents/FiberCompareView/'
execfile(fb_viewr_dir+'TwoStrainView.py')
execfile(fb_viewr_dir+'ThreeStrainView.py')
execfile(fb_viewr_dir+'FourStrainView.py')
execfile(fb_viewr_dir+'FiveStrainView.py')


class roiDropdown(qt.QComboBox):
  def loadROI(self, name):
    roi = -1
    for key in self.trkDict:
      if self.trkDict[key] == name:
        roi = key
        break
    if roi == -1:
      print("Error finding correct ROI")
      return
    scene = slicer.app.mrmlScene()
    sutil = slicer.util
    #Clear the 3D and 2D scenes
    composites = slicer.util.getNodesByClass("vtkMRMLSliceCompositeNode")
    for c_node in composites:
      c_node.SetBackgroundVolumeID("None")
    fibers = slicer.util.getNodesByClass("vtkMRMLFiberBundleNode")
    for f_node in fibers:
      l_node = f_node.GetLineDisplayNode()
      t_node = f_node.GetTubeDisplayNode()
      l_node.VisibilityOff()
      t_node.VisibilityOff()
    changeLayout(0)
    i = 1
    volList = []
    for package in self.packages:
      tract = package.getTractNode(roi)
      vol = package.getVolumeNode()
      noTract = tract is None
      noVol = vol is None
      if noTract:
        if package.getTractPath(roi) is None:
          print("No tract for this ROI")
          continue
        [LoadSuccess, tract]=sutil.loadFiberBundle(package.getTractPath(roi),True)
        if LoadSuccess==0:
          print("Error loading tract")
          continue
        else:
          package.addTract(tract, roi)
      if noVol:
        if package.getVolumePath() is None:
          print("No volume available")
          continue
        [LoadSuccess, vol]=sutil.loadVolume(package.getVolumePath(),{"Show":False},True)
        if LoadSuccess==0:
          print("Error loading volume")
          continue
        else:
          package.addVolume(vol)
      if noTract and noVol:
        applyTransforms(package.getTransforms(), vol, tract)
      if noTract and not noVol:
        applyTransforms(package.getTransforms(), None, tract)
      #print(tract.GetID())
      #print(vol.GetID())
      volList.append(vol)
      lineNode = tract.GetLineDisplayNode()
      tubeNode = tract.GetTubeDisplayNode()
      viewString = "vtkMRMLViewNode"+str(i)
      sliceString = "vtkMRMLSliceNode"+str(i)
      #compString = sliceString.replace("Slice","SliceComposite")
      sliceNode = scene.GetNodeByID(sliceString)
      sliceNode.SetSliceResolutionMode(0)
      lineNode.SetDisplayableOnlyInView(viewString)
      tubeNode.SetDisplayableOnlyInView(sliceString)
      tubeNode.SetTubeRadius(0.05)
      lineNode.VisibilityOn()
      tubeNode.VisibilityOn()
      lineNode.SetColorModeToPointFiberOrientation()
      tubeNode.SetColorModeToPointFiberOrientation()
      tubeNode.SetSliceIntersectionVisibility(1)
      #compNode = scene.GetNodeByID(compString)
      #print("Setting " + compString + " to " + vol.GetID())
      #compNode.SetBackgroundVolumeID(vol.GetID())
      i = i + 1
      #print(i)
    for j in range(len(volList)):
      compNode = scene.GetNodeByID("vtkMRMLSliceCompositeNode" + str(j+1))
      compNode.SetBackgroundVolumeID(volList[j].GetID())
    resetViews()

  def __init__(self, dataPackages):
    super(qt.QComboBox, self).__init__()
    self.packages = dataPackages
    self.trkDict = dict()
    qtLayout = slicer.app.layoutManager().threeDWidget(0).layout()
    qtLayout.addWidget(self)
    for package in self.packages:
      packageDict = package.getTracts()
      if packageDict is None:
        print("No dictionary present")
        continue
      for trkNum in packageDict:
        if not self.trkDict.has_key(trkNum) and package.getTractName(trkNum) is not None:
          #print(package.getTractName(trkNum))
          self.addItem(package.getTractName(trkNum))
          self.trkDict[trkNum] = package.getTractName(trkNum)
    #print(len(self.trkDict))
    self.currentTextChanged.connect(self.loadROI)

def viewerCountDropdown(num):
  cb = qt.QComboBox()
  qtLayout = slicer.app.layoutManager().threeDWidget(0).layout()
  qtLayout.addWidget(cb)
  for i in range(2, num+1):
    cb.addItem(i)
  cb.currentIndexChanged.connect(changeLayout)
  
def changeLayout(i):
  layoutManager = slicer.app.layoutManager()
  layoutManager.setLayout(586+i)
  cam1 = slicer.util.getNode("vtkMRMLCameraNode1")
  for i in range(2, i+3):
    cam1.SetActiveTag("vtkMRMLViewNode"+str(i))
  resetViews()

def resetViews():
  manager = slicer.app.layoutManager()
  manager.resetSliceViews()
  manager.resetThreeDViews()

def applyTransforms(transformList, vol, tract):
  sutil = slicer.util
  for tn in range(len(transformList)):
    transform = transformList[tn]
    transformName = transform[0]
    print(transformName)
    if transform[1] is None:
      [loadSuccess, transformNode]=sutil.loadTransform(transformName, True)
      if loadSuccess == 0:
        print("Failed to load transform")
        return
      transformList[tn] = (transformName, transformNode)
    if tn == 0:
      if tract is not None:
        tract.SetAndObserveTransformNodeID(transformList[tn][1].GetID())
      continue
    #print("Applying transform to older transform...")
    transformList[tn-1][1].SetAndObserveTransformNodeID(transformList[tn][1].GetID())
    if vol is not None and tn == 1:
      #print("Applying transform " + str(tn) + " first time")
      vol.SetAndObserveTransformNodeID(transformList[tn][1].GetID())