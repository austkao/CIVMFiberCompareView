def runVolumeRender(volumeNode, view3D):
    # given a mrml volume node and a 3d view number, 
    # checks for volumerenderingnode, and creates if necessary.
    # then displays renderingnode in view
    #
    # not sure if vktMRMLVolumeRenderingDisplayNode takes a N for 
    # setvisibility or just a boolean
    # the original code might have been naughtily clever in hiding that.
    if volumeNode == None:
      return
    volumeRenderingLogic = slicer.modules.volumerendering.logic()
    # Get the first vtkMRMLVolumeRenderingDisplayNode associated to the volume
    displayNode = None
    for i in range(0, volumeNode.GetNumberOfDisplayNodes()):
      displayNode = volumeNode.GetNthDisplayNode(i)
      if displayNode and displayNode.IsA('vtkMRMLVolumeRenderingDisplayNode'):
        break
      else:
        displayNode = None
    if not view3D:
      if displayNode == None:
        return
      displayNode.SetVisibility(0)
    else:
      if displayNode == None:
        displayNode = volumeRenderingLogic.CreateVolumeRenderingDisplayNode()
        slicer.mrmlScene.AddNode(displayNode)
        displayNode.UnRegister(volumeRenderingLogic)
        volumeRenderingLogic.UpdateDisplayNodeFromVolumeNode(displayNode, volumeNode)
        volumeNode.AddAndObserveDisplayNodeID(displayNode.GetID())
      else:
        volumeRenderingLogic.UpdateDisplayNodeFromVolumeNode(displayNode, volumeNode)
      displayNode.SetVisibility(view3D)
