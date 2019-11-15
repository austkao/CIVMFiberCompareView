#Code for setting up the Fiber Bundles in Two Strain View layout
#Strain a will be seen on the left side and strain b will be seen on the right side
#Author: Austin Kao
def SetUpFiberBundle(intList,trkFilter):
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
	for i in range(len(intList)):
		lineString = "vtkMRMLFiberBundleLineDisplayNode"+str(intList[i])
		tubeString = "vtkMRMLFiberBundleTubeDisplayNode"+str(intList[i])
		viewString = "vtkMRMLViewNode"+str(viewNum)
		if(viewNum==1):
			sliceString = "vtkMRMLSliceNodeOne"
		elif(viewNum==2):
			layoutManager.setLayout(TwoStrainView)
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
		line1 = scene.GetNodeByID(lineString)
		line1.SetDisplayableOnlyInView(viewString)
		tube1 = scene.GetNodeByID(tubeString)
		tube1.SetDisplayableOnlyInView(sliceString)
		tube1.SetTubeRadius(0.05)
		line1.VisibilityOn()
		tube1.VisibilityOn() #Note that the tube slice will not show up
		viewNum = viewNum+1