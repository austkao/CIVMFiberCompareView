execfile("/Users/ak457/Documents/FiberCompareView/DataPackage.py")
execfile("/Users/ak457/Documents/FiberCompareView/Dropdowns.py")
import os
import re
from sets import Set
strList = ["DB2/N54781","BTBR/N54817"]
labelPaths = ["BTBR/N54811/labels_N54811/WHS_heritability/N54811_BTBR_symmetric_R_labels_RAS_lookup.txt", "DB2/N54781/labels_N54781/WHS_heritability/N54781_DB2_symmetric_R_labels_RAS_lookup.txt"]
packageList= [loadDataPackage(strList[0], labelPaths[0]), loadDataPackage(strList[1], labelPaths[1])]
roiDropdown(packageList)

