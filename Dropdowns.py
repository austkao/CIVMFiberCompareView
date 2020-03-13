#Defines methods and classes for dropdown menus
#Useful methods: slicer.util.getNode(), slicer.util.setSliceViewerLayers()
#Author: Austin Kao

import os
import re
fb_viewr_dir='/Users/ak457/Documents/FiberCompareView/'
#fb_viewr_dir='/Volumes/ak457/Documents/FiberCompareView/'
execfile(fb_viewr_dir+'TwoStrainView.py')
execfile(fb_viewr_dir+'ThreeStrainView.py')
execfile(fb_viewr_dir+'FourStrainView.py')
execfile(fb_viewr_dir+'FiveStrainView.py')

#Method meant to set up and control all the dropdown menus being used
def createDropdowns(dataPackages):
  changeLayout(3)
  viewerCountDropdown(5)
  roiDropdown(dataPackages)
  for i in range(1, 6):
    if i-1 < len(dataPackages):
      specimenDropdown(dataPackages, i, volumeDropdown(dataPackages[i-1], i))
    else:
      specimenDropdown(dataPackages, i)
  changeLayout(0)

# Class for setting up a dropdown menu containing the available ROIs for a set of data packages
class roiDropdown(qt.QComboBox):
  def loadROI(self, name):
    #Find the relevant ROI
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
    #changeLayout(0)
    i = 1
    volList = []
    # Load in the relevant tracts and volumes for the chosen ROI
    for package in self.packages:
      tract, vol = loadVolAndTract(package, roi)
      print(tract.GetID())
      print(vol.GetID())
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
    for j in range(len(volList)):
      compNode = scene.GetNodeByID("vtkMRMLSliceCompositeNode" + str(j+1))
      print(compNode.GetID())
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

class specimenDropdown(qt.QComboBox):
  def __init__(self, dataPackages, num, volDrop = None):
    self.dataPackages = dataPackages
    self.comboBox = qt.QComboBox()
    self.specName = ""
    self.dropdownNum = num
    self.volumeDropdown = volDrop
    qtLayout = slicer.app.layoutManager().sliceWidget(str(num)).layout()
    qtLayout.addWidget(self.comboBox)
    self.comboBox.addItem("None")
    for package in dataPackages:
      self.comboBox.addItem(package.getName())
    self.comboBox.currentTextChanged.connect(self.changeSpecimen)
  
  def changeSpecimen(self, name):
    compString = "vtkMRMLSliceCompositeNode"+str(self.dropdownNum)
    sliceString = "vtkMRMLSliceNode"+str(self.dropdownNum)
    viewString = "vtkMRMLViewNode"+str(self.dropdownNum)
    compNode = slicer.app.mrmlScene().GetNodeByID(compString)
    if name == "None":
      compNode.SetBackgroundVolumeID("None")
    for package in self.dataPackages:
      if package.getName() == self.specName:
        for roi in package.getTracts():
          tract = package.getTractNode(roi)
          if tract is not None and tract.GetLineDisplayNode().IsDisplayableInView(viewString):
              tract.GetLineDisplayNode().VisibilityOff()
              tract.GetTubeDisplayNode().VisibilityOff()
      if package.getName() == name:
        vol = package.getVolumeNode()
        if vol is not None:
          compNode.SetBackgroundVolumeID(package.getVolumeNode().GetID())
        for roi in package.getTracts():
          tract = package.getTractNode(roi)
          if tract is not None:
            tract.GetLineDisplayNode().SetDisplayableOnlyInView(viewString)
            tract.GetTubeDisplayNode().SetDisplayableOnlyInView(sliceString)
            tract.GetLineDisplayNode().VisibilityOn()
            tract.GetTubeDisplayNode().VisibilityOn()
    self.specName = name
    if self.volumeDropdown is not None and self.specName is not "None":
      for package in self.dataPackages:
        if package.getName() == self.specName:
          self.volumeDropdown.swapPackage(package)

class volumeDropdown(qt.QComboBox):
  def __init__(self, dataPackage, num):
    self.dataPackage = dataPackage
    self.comboBox = qt.QComboBox()
    self.specName = ""
    self.dropdownNum = num
    qtLayout = slicer.app.layoutManager().sliceWidget(str(num)).layout()
    qtLayout.addWidget(self.comboBox)
    volDict = dataPackage.getVolumes()
    for key in volDict:
      self.comboBox.addItem(volDict[key][2])
    self.specName = str(self.comboBox.currentText)
    self.comboBox.currentTextChanged.connect(self.changeVolume)
  
  def swapPackage(self, dataPackage):
    self.comboBox.currentTextChanged.connect(self.doNothing)
    for i in range(self.comboBox.count):
      self.comboBox.removeItem(0)
    self.dataPackage = dataPackage
    volDict = dataPackage.getVolumes()
    for key in volDict:
      self.comboBox.addItem(volDict[key][2])
    self.comboBox.currentTextChanged.connect(self.changeVolume)
  
  def doNothing(self, name):
    print(name)
    return
  
  def changeVolume(self, name):
    compString = "vtkMRMLSliceCompositeNode"+str(self.dropdownNum)
    sliceString = "vtkMRMLSliceNode"+str(self.dropdownNum)
    compNode = slicer.app.mrmlScene().GetNodeByID(compString)
    volNode = self.dataPackage.getGeneralVolumeNode(name)
    if volNode is None:
      volPath = self.dataPackage.getGeneralVolumePath(name)
      if volPath is not None:
        [LoadSuccess, volNode]=slicer.util.loadVolume(volPath,{"Show":False},True)
        if LoadSuccess==0:
          print("Error loading volume")
          return
        else:
          self.dataPackage.addGeneralVolume(volNode, name)
          applyTransforms(self.dataPackage.getTransforms(), volNode, None)
    if volNode is not False:
      compNode.SetBackgroundVolumeID(volNode.GetID())
    return


def loadVolAndTract(package, roi):
  sutil = slicer.util
  tract = package.getTractNode(roi)
  vol = package.getVolumeNode()
  noTract = tract is None
  noVol = vol is None
  if noTract:
    if package.getTractPath(roi) is None:
      print("No tract for this ROI")
    [LoadSuccess, tract]=sutil.loadFiberBundle(package.getTractPath(roi),True)
    if LoadSuccess==0:
      print("Error loading tract")
    else:
      package.addTract(tract, roi)
  if noVol:
    if package.getVolumePath() is None:
      print("No volume available")
    [LoadSuccess, vol]=sutil.loadVolume(package.getVolumePath(),{"Show":False},True)
    if LoadSuccess==0:
      print("Error loading volume")
    else:
      package.addVolume(vol)
  if noTract and noVol:
    print("Applying transforms no vol")
    applyTransforms(package.getTransforms(), vol, tract)
  elif noTract and not noVol:
    print("Applying transforms vol")
    applyTransforms(package.getTransforms(), None, tract)
  return tract, vol  

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
    viewString = "vtkMRMLViewNode"+str(i)
    cam1.SetActiveTag(viewString)
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