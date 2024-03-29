#Based on code originally written by Alex Sheu
#Modified by Austin Kao


customLayout = ("<layout type=\"horizontal\">"
  " <item>"
  "  <layout type=\"vertical\">"
  "	  <item>"
  " 	<view class=\"vtkMRMLViewNode\" singletontag=\"1\" verticalStretch=\"0\">"
  "    		<property name=\"viewlabel\" action=\"default\">1</property>"
  "  	</view>"
  "   </item>"
  "   <item>"
  "    	<view class=\"vtkMRMLSliceNode\" singletontag=\"1\">"
  "      <property name=\"orientation\" action=\"default\">Coronal</property>"
  "      <property name=\"viewlabel\" action=\"default\">s1</property>"
  "      <property name=\"viewcolor\" action=\"default\">#fffff1</property>"
  "   	</view>"
  "   </item>"
  "  </layout>"
  " </item>"
  " <item>"
  "  <layout type=\"vertical\">"
  "	  <item>"
  " 	<view class=\"vtkMRMLViewNode\" singletontag=\"2\" verticalStretch=\"0\">"
  "    	 <property name=\"viewlabel\" action=\"default\">2</property>"
#  "      <property name=\"viewgroup\" action=\"default\">1</property>"
  "  	</view>"
  "   </item>"
  "   <item>"
  "    <view class=\"vtkMRMLSliceNode\" singletontag=\"2\">"
  "     <property name=\"orientation\" action=\"default\">Coronal</property>"
  "     <property name=\"viewlabel\" action=\"default\">s2</property>"
  "     <property name=\"viewcolor\" action=\"default\">#fffff2</property>"
#  "     <property name=\"viewgroup\" action=\"default\">1</property>"
  "    </view>"
  "   </item>"
  "  </layout>"
  " </item>"
  "</layout>")

customLayoutId=586
TwoStrainView=customLayoutId;
layoutManager = slicer.app.layoutManager()
layoutManager.layoutLogic().GetLayoutNode().AddLayoutDescription(customLayoutId, customLayout)

#layoutManager.setLayout(customLayoutId)
