# Test script for dropdowns
# To run, type execfile("/Users/ak457/Documents/FiberCompareView/Test_Script_Dropdown.py")
# Author: Austin Kao

execfile("/Users/ak457/Documents/FiberCompareView/DataPackage.py")
execfile("/Users/ak457/Documents/FiberCompareView/Dropdowns.py")
#from sets import Set
strList = ["DB2/N54781","BTBR/N54817"]
labelPaths = ["DB2/N54781/labels_N54781/WHS_heritability/N54781_DB2_symmetric_R_labels_RAS_lookup.txt", "BTBR/N54811/labels_N54811/WHS_heritability/N54811_BTBR_symmetric_R_labels_RAS_lookup.txt"]
packageList= [DataPackage(strList[0], labelPaths[0]), DataPackage(strList[1], labelPaths[1])]
createDropdowns(packageList)

