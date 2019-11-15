import re
def findNode(string):
	regex = re.compile(".*"+string+".*")
	thenodes=slicer.mrmlScene.GetNodes()
	limit = thenodes.GetNumberOfItems()
	res = 0
	for i in range(0, limit):
		node = thenodes.GetItemAsObject(i)
		print(node.GetID()+regex)
		mat=regex.search(node.GetID())
		if mat:
			print("Found at index {}".format(i))
			res = node
			return res
	return res