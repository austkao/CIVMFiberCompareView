# Function to view a specified ROI across the available viewers
# Assumes a predetermined file path
# Code based off of testStrainDataLoad and StrainDataLoad
# Code will load the fiber bundles of a specified ROI first, and then set viewers to accomodate the loaded data
# Author: Austin Kao

#Find the nodes associated with a particular ROI and view them
#Much easier if there is a dictionary of ROI-node pairs to use

def viewAndCompareROI(roi, roiDict=None):
    if(type(roi) is not int):
        print("Please specify an integer ROI")
        return
    if(roi < 0):
        print("ROI cannot be negative")
        return
    scene = slicer.app.mrmlScene()
    if roiDict is not None:
        if(type(roiDict) is not dict):
            print("Please give a valid dictionary")
            return
        if(not roiDict.has_key(roi)):
            print("No such ROI found in dictionary")
            return
        nodeSet=roiDict[roi]
        doneSet=Set([])
        for i in range(1,len(nodeSet)+1):
            package=nodeSet.pop()
            doneSet.add(package)
            fibNode=package.getFibNode()
            lineNode = fibNode.GetLineDisplayNode()
            tubeNode = fibNode.GetTubeDisplayNode()
            viewString = "vtkMRMLViewNode"+str(i)
            sliceString = "vtkMRMLSliceNode"+str(i)
            compString = sliceString.replace("Slice","SliceComposite")
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
            compNode = scene.GetNodeByID(compString)
            volume=package.getVolNode()
            compNode.SetBackgroundVolumeID(volume.GetID())
        roiDict[roi]=doneSet
        manager = slicer.app.layoutManager()
        manager.resetSliceViews()
        manager.resetThreeDViews()
#TODO: load relevant nodes and set the viewers accordingly, assuming no dictionary is available

def viewAndCompareROI_v2(roi, packages):
  if(type(roi) is not int):
    print("Please specify an integer ROI")
    return
  if(roi < 0):
    print("ROI cannot be negative")
    return
  scene = slicer.app.mrmlScene()
  sutil = slicer.util
  if type(packages) is not list:
    print("Please input a list of packages")
    return
  i = 1
  for package in packages:
    tract = package.getTractNode(roi)
    vol = package.getVolumeNode()
    if tract is None:
      if package.getTractPath(roi) is None:
        print("No tract for this ROI")
        return
      [LoadSuccess, tract]=sutil.loadFiberBundle(package.getTractPath(roi),True)
      if LoadSuccess==0:
        print("Error loading tract")
        return
      else:
        package.addTract(tract, roi)
    if vol is None:
      if package.getVolumePath() is None:
        print("No volume available")
        return
      [LoadSuccess, vol]=sutil.loadVolume(package.getVolumePath(),{"Show":False},True)
      if LoadSuccess==0:
        print("Error loading volume")
        return
      else:
        package.addVolume(vol)
    lineNode = tract.GetLineDisplayNode()
    tubeNode = tract.GetTubeDisplayNode()
    viewString = "vtkMRMLViewNode"+str(i)
    sliceString = "vtkMRMLSliceNode"+str(i)
    compString = sliceString.replace("Slice","SliceComposite")
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
    compNode = scene.GetNodeByID(compString)
    compNode.SetBackgroundVolumeID(vol.GetID())
    i = i + 1
  manager = slicer.app.layoutManager()
  manager.resetSliceViews()
  manager.resetThreeDViews()

