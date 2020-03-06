#Function for setting a specific package of tract data into a 3D viewer and its corresponding 2D slice view
#Parameter package is the MRML ID string of the fiber bundle in the data package being used?
#Parameter view is the number of the 3D and 2D view to be used
#setDataPackageInViewers (e.g. set viewers to specific packages)
#Author: Austin Kao

def setPackageInViewer(package, view, show3D=None):
    if(not(type(view) is int)):
        print("Please use an integer for the view")
        return
    scene = slicer.app.mrmlScene()
    #fibString = package.getFibNode()
    #fibNode = scene.GetNodeByID(fibString)
    fibNode=package.getFibNode()
    lineNode = fibNode.GetLineDisplayNode()
    tubeNode = fibNode.GetTubeDisplayNode()
    viewString = "vtkMRMLViewNode"+str(view)
    sliceString = "vtkMRMLSliceNode"+str(view)
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
    
    # this wierd intlist[i]-1 is to is to goto 0 indexing from 1
    # take care, even though i is zero indexed, it wouldn't 
    # necessarily be the right value here.
    #volume = scene.GetNodeByID(package.getVolNode())
    volume=package.getVolNode()
    compNode.SetBackgroundVolumeID(volume.GetID())
    manager = slicer.app.layoutManager()
    manager.resetSliceViews()
    if show3D is not None:
        if type(show3D) is str:
            type(show3D)
            if os.path.isfile(show3D):
                # If we're a file, assume we're a volume property.
                rendPropName=os.path.splitext(os.path.basename(show3D))[0]
                propNodes=scene.GetNodesByName(rendPropName)
                if propNodes.GetNumberOfItems() == 0:
                    ioM=slicer.app.ioManager()
                    loadSuccess=ioM.loadFile(show3D)
                    if not loadSuccess: 
                        print("Error on load volume prop"+show3D)
                        return
                    propNodes=scene.GetNodesByName(rendPropName)
                if propNodes.GetNumberOfItems() != 1:
                    print("Requested volume property but failed to load(or got multiple load results)")
                    return
                show3D=propNodes.GetItemAsObject(0)
        runVolumeRender(volume,i+1,show3D)
        manager.resetThreeDViews()
		

def setPackagesInViewers(packageList, viewerList):
    if len(packageList) != len(viewerList):
        print("Must have a package-viewer pair")
        return
    for i in range(0, len(packageList)):
        setPackageInViewer(packageList[i],viewerList[i])