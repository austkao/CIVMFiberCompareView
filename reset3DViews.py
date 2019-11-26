def reset3DViews(self):
# Reset focal view around volumes
manager = slicer.app.layoutManager()
for i in range(0, manager.threeDViewCount):
  manager.threeDWidget(i).threeDView().resetFocalPoint()
  rendererCollection = manager.threeDWidget(i).threeDView().renderWindow().GetRenderers()
  for i in range(0, rendererCollection.GetNumberOfItems()):
	rendererCollection.GetItemAsObject(i).ResetCamera()
#self.viewScaler()
