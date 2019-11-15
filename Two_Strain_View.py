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
  "    	<view class=\"vtkMRMLSliceNode\" singletontag=\"Red\">"
  "      <property name=\"orientation\" action=\"default\">Axial</property>"
  "      <property name=\"viewlabel\" action=\"default\">R</property>"
  "      <property name=\"viewcolor\" action=\"default\">#f9a99f</property>"
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
  "    <view class=\"vtkMRMLSliceNode\" singletontag=\"Yellow\">"
  "     <property name=\"orientation\" action=\"default\">Axial</property>"
  "     <property name=\"viewlabel\" action=\"default\">Y</property>"
  "     <property name=\"viewcolor\" action=\"default\">#EDD54C</property>"
#  "     <property name=\"viewgroup\" action=\"default\">1</property>"
  "    </view>"
  "   </item>"
  "  </layout>"
  " </item>"
  "</layout>")

customLayoutId=586

layoutManager = slicer.app.layoutManager()
layoutManager.layoutLogic().GetLayoutNode().AddLayoutDescription(customLayoutId, customLayout)                                         
layoutManager.setLayout(customLayoutId)