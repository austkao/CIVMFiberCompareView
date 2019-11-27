#Code for setting up the Fiber Bundles in Fiber Compare Views
#Input intList is a list of the fiber bundle numbers to display from left to right
#e.g. list [1,2] displays FiberBundle1 in View 1 (left side) and FiberBundle2 in View 2 (right side)
#
#Note that it is necessary to exec a FiberCompareView first before executing code
#e.g. exec FiveStrainView.py first before giving input list of length five
#Note that the code assumes that MRML IDs for the FA and Fiber Bundle Nodes share the same number
#Author: Austin Kao
def SetUpFiberBundle(intList,trkFilter=None,show3D=None):
	if(not(type(intList) is list)):
		print(type(intList))
		print("Please use a list as an input")
		return
	if(not len(intList) >= 2):
		print("Too few elements in list")
		return
	viewNum = 1 #Variable representing the view number
	sliceString = "" #Variable representing the slice node ID string
	scene = slicer.app.mrmlScene()
	volumes = scene.GetNodesByClass("vtkMRMLScalarVolumeNode")
	#TODO: Ensure volume count is same as intList length
	layoutManager.setLayout(TwoStrainView)
	for i in range(len(intList)):
		#fib = scene.GetNodeByID("vtkMRMLFiberBundleNode"+str(intList[i]))
		#fib.SetColorModeToMeanFiberOrientation()
		# use trk filter to find only mess with proper track here?
		lineString = "vtkMRMLFiberBundleLineDisplayNode"+str(intList[i])
		tubeString = "vtkMRMLFiberBundleTubeDisplayNode"+str(intList[i])
		viewString = "vtkMRMLViewNode"+str(viewNum)
		if(viewNum==1):
			sliceString = "vtkMRMLSliceNodeOne"
		elif(viewNum==2):
			sliceString = "vtkMRMLSliceNodeTwo"
		elif(viewNum==3):
			layoutManager.setLayout(ThreeStrainView)
			sliceString = "vtkMRMLSliceNodeThree"
		elif(viewNum==4):
			layoutManager.setLayout(FourStrainView)
			sliceString = "vtkMRMLSliceNodeFour"
		elif(viewNum==5):
			layoutManager.setLayout(FiveStrainView)
			sliceString = "vtkMRMLSliceNodeFive"
		compString = sliceString.replace("Slice","SliceComposite")
		print(compString)
		sliceNode = scene.GetNodeByID(sliceString)
		sliceNode.SetSliceResolutionMode(0)
	    #compString = sliceString.replace("Slice","SliceComposite")
		#compNode = scene.GetNthNodeByClass(i, "vtkMRMLSliceCompositeNode")
		#volume = volumes.GetItemAsObject(intList[i]-1)
		#compNode.SetBackgroundVolumeID(volume.GetID())
		#print(compString)
		line1 = scene.GetNodeByID(lineString)
		line1.SetDisplayableOnlyInView(viewString)
		tube1 = scene.GetNodeByID(tubeString)
		tube1.SetDisplayableOnlyInView(sliceString)
		tube1.SetTubeRadius(0.05)
		line1.VisibilityOn()
		tube1.VisibilityOn() #Note that the tube slice will not show up
		line1.SetColorModeToPointFiberOrientation()
		tube1.SetColorModeToPointFiberOrientation()
		tube1.SetSliceIntersectionVisibility(1)
		#compNode = scene.GetNodeByID(compString)
		#compNode.SetBackgroundVolumeID(volume.GetID())
		compNode = scene.GetNodeByID(compString)
		volume = volumes.GetItemAsObject(intList[i]-1)
		compNode.SetBackgroundVolumeID(volume.GetID())
		viewNum = viewNum+1
		#>>> manager.resetThreeDViews()
		manager = slicer.app.layoutManager()
		manager.resetSliceViews()
		if show3D is not None:
			runVolumeRender(volume,i+1)
			manager.resetThreeDViews()
			#reset3DView(i+1)

