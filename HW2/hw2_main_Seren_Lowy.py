# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 11:53:41 2020

@author: Guoning Chen, modified by Duong Nguyen
"""


import sys
import vtk
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import Qt

from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


'''
    The Qt MainWindow class
    A vtk widget and the ui controls will be added to this main window
'''
class MainWindow(Qt.QMainWindow):

    def __init__(self, parent = None):
        Qt.QMainWindow.__init__(self, parent)
        
        ''' Step 1: Initialize the Qt window '''
        self.setWindowTitle("COSC 6344 Visualization, Assignment 2, Seren Lowy")
        self.resize(1000,self.height())
        self.frame = Qt.QFrame() # Create a main window frame to add ui widgets
        self.mainLayout = Qt.QHBoxLayout()  # Set layout - Lines up widgets horizontally
        self.frame.setLayout(self.mainLayout)
        self.setCentralWidget(self.frame)
        
        ''' Step 2: Add a vtk widget to the central widget '''
        # As we use QHBoxLayout, the vtk widget will be automatically moved to the left
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.mainLayout.addWidget(self.vtkWidget)
        
        #Initialize the vtk variables for the visualization tasks
        self.init_vtk_widget()
        
        # Add an object to the rendering window
        # self.add_vtk_object()
        
        ''' Step 3: Add the control panel to the right hand side of the central widget '''
        # Note: To add a widget, we first need to create a widget, then set the layout for it
        self.right_panel_widget = Qt.QWidget() # create a widget
        self.right_panel_layout = Qt.QVBoxLayout() # set layout - lines up the controls vertically
        self.right_panel_widget.setLayout(self.right_panel_layout) #assign the layout to the widget
        self.mainLayout.addWidget(self.right_panel_widget) # now, add it to the central frame
        
        # The controls will be added here
        self.add_controls()
                
 
    '''
        Initialize the vtk variables for the visualization tasks
    '''    
    def init_vtk_widget(self):
        vtk.vtkObject.GlobalWarningDisplayOff() #Disable vtkOutputWindow - Comment out this line if you want to see the warning/error messages from vtk
        
        # Create the graphics structure. The renderer renders into the render
        # window. The render window interactor captures mouse events and will
        # perform appropriate camera or actor manipulation depending on the
        # nature of the events.
        self.ren = vtk.vtkRenderer() 
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        colors = vtk.vtkNamedColors()
        self.ren.SetBackground(0.8,0.8,0.8) # you can change the background color here

        # Start by creating a black/white lookup table.
        self.bwLut = vtk.vtkLookupTable()
        # YOU need adjust the following range to address the dynamic range issue!
        self.bwLut.SetTableRange(0, 2)
        self.bwLut.SetSaturationRange(0, 0)
        self.bwLut.SetHueRange(0, 0)
        self.bwLut.SetValueRange(0, 1)
        self.bwLut.Build()  # effective built
 

        # Start the vtk screen
        self.ren.ResetCamera()
        self.show()
        self.iren.Initialize()
        self.iren.Start()

    ''' 
        Show a popup message 
    '''
    def show_popup_message(self,msg):
        alert = Qt.QMessageBox()
        alert.setText(msg)
        alert.exec_()
        
    def re_render(self):
        self.vtkWidget.GetRenderWindow().Render()
    
    '''
        Add QT controls to the control panel in the righ hand size
    '''
    def add_controls(self):
    
        ''' Add a sample group box '''
        groupBox = Qt.QGroupBox("3D Scalar Field Visualization") # Use a group box to group controls
        groupBox_layout = Qt.QVBoxLayout() #lines up the controls vertically
        groupBox.setLayout(groupBox_layout) 
        self.right_panel_layout.addWidget(groupBox)
  
        ''' Add a textfield ( QLineEdit) to show the file path and the browser button '''
        label = Qt.QLabel("Choose a file (e.g., vtk):")
        groupBox_layout.addWidget(label)
        hbox = Qt.QHBoxLayout()
        self.ui_file_name = Qt.QLineEdit()
        hbox.addWidget(self.ui_file_name) 
        self.ui_browser_button = Qt.QPushButton('Browser')
        self.ui_browser_button.clicked.connect(self.on_file_browser_clicked)
        self.ui_browser_button.show()
        hbox.addWidget(self.ui_browser_button)
        file_widget = Qt.QWidget()
        file_widget.setLayout(hbox)
        groupBox_layout.addWidget(file_widget)
 
        ''' Add the Open button '''
        self.ui_open_button = Qt.QPushButton('Open')
        self.ui_open_button.clicked.connect(self.open_vtk_file)
        self.ui_open_button.show()
        groupBox_layout.addWidget(self.ui_open_button)
  
        ''' Add the min, max scalar labels '''
        self.ui_min_label = Qt.QLabel("Min Scalar: 0")
        self.ui_max_label = Qt.QLabel("Max Scalar: 0")
        groupBox_layout.addWidget(self.ui_min_label)
        groupBox_layout.addWidget(self.ui_max_label)
        
        #Add spin box for table range
        table_range_label = Qt.QLabel("Select the scalar range for color table")
        groupBox_layout.addWidget(table_range_label)
        hbox =  Qt.QHBoxLayout()
        
        self.ui_min_range = Qt.QDoubleSpinBox()
        hbox.addWidget(self.ui_min_range)
        self.ui_min_range.valueChanged.connect(self.on_dynamic_min_spinbox_change)
        self.label_min_range = Qt.QLabel("Min Range")
        hbox.addWidget(self.label_min_range)
        
        self.ui_max_range = Qt.QDoubleSpinBox()
        hbox.addWidget(self.ui_max_range)
        self.ui_max_range.valueChanged.connect(self.on_dynamic_max_spinbox_change)
        self.label_max_range = Qt.QLabel("Max Range")
        hbox.addWidget(self.label_max_range)
        
        tablerange_hwidget = Qt.QWidget()
        tablerange_hwidget.setLayout(hbox)
        groupBox_layout.addWidget(tablerange_hwidget)


        ''' Add spinbox for scalar threshold selection '''
        hbox =  Qt.QHBoxLayout()
        self.ui_isoSurf_checkbox = Qt.QCheckBox("Show iso-surface (select threshold)")
        hbox.addWidget(self.ui_isoSurf_checkbox)
        self.ui_isoSurf_checkbox.setChecked(False)
        self.ui_isoSurf_checkbox.toggled.connect(self.on_checkbox_change)
        self.ui_iso_threshold = Qt.QDoubleSpinBox()
        hbox.addWidget(self.ui_iso_threshold)
        self.ui_iso_threshold.valueChanged.connect(self.on_iso_threshold_spinbox_change)

        ''' Add the Show Iso-Surface button '''
        self.ui_show_iso_button = Qt.QPushButton('Show')
        self.ui_show_iso_button.clicked.connect(self.extract_one_isosurface)
        self.ui_show_iso_button.show()
        hbox.addWidget(self.ui_show_iso_button)
        isoSurf_hwidget = Qt.QWidget()
        isoSurf_hwidget.setLayout(hbox)
        groupBox_layout.addWidget(isoSurf_hwidget)

        hbox =  Qt.QHBoxLayout()
        self.ui_opacity_slider = Qt.QSlider(QtCore.Qt.Horizontal)
        self.ui_opacity_slider.setRange(0, 100)
        self.ui_opacity_slider.setValue(100)
        self.ui_opacity_slider.valueChanged.connect(self.change_opacity)
        hbox.addWidget(self.ui_opacity_slider)
        self.label_opacity_slider = Qt.QLabel()
        self.label_opacity_slider.setText("Opacity:"+str(self.ui_opacity_slider.value()/100.0))
        hbox.addWidget(self.label_opacity_slider)
        opacity_slider_widget = Qt.QWidget()
        opacity_slider_widget.setLayout(hbox)
        groupBox_layout.addWidget(opacity_slider_widget)


        groupBox_layout.addWidget(Qt.QLabel("3D cut planes:"))
        ''' Add a slider bar for XY slicing plane '''
        hbox =  Qt.QHBoxLayout()
        self.ui_xy_plane_checkbox = Qt.QCheckBox("Show XY Cut Plane")
        self.ui_xy_plane_checkbox.setChecked(False)
        self.ui_xy_plane_checkbox.toggled.connect(self.on_checkbox_change)
        hbox.addWidget(self.ui_xy_plane_checkbox)
        self.ui_zslider = Qt.QSlider(QtCore.Qt.Horizontal)
        self.ui_zslider.valueChanged.connect(self.on_zslider_change)
        hbox.addWidget(self.ui_zslider)
        self.label_zslider = Qt.QLabel()
        hbox.addWidget(self.label_zslider)
        self.label_zslider.setText("Z index:"+str(self.ui_zslider.value()))
        z_slider_widget = Qt.QWidget()
        z_slider_widget.setLayout(hbox)
        groupBox_layout.addWidget(z_slider_widget)
        
        ''' Add the sliders for the other two cut planes '''
        # ''' Add a slider bar for XZ slicing plane '''
        hbox =  Qt.QHBoxLayout()
        self.ui_xz_plane_checkbox = Qt.QCheckBox("Show XZ Cut Plane")
        self.ui_xz_plane_checkbox.setChecked(False)
        self.ui_xz_plane_checkbox.toggled.connect(self.on_checkbox_change)
        hbox.addWidget(self.ui_xz_plane_checkbox)
        self.ui_yslider = Qt.QSlider(QtCore.Qt.Horizontal)
        self.ui_yslider.valueChanged.connect(self.on_yslider_change)
        hbox.addWidget(self.ui_yslider)
        self.label_yslider = Qt.QLabel()
        hbox.addWidget(self.label_yslider)
        self.label_yslider.setText("Y index:"+str(self.ui_yslider.value()))
        y_slider_widget = Qt.QWidget()
        y_slider_widget.setLayout(hbox)
        groupBox_layout.addWidget(y_slider_widget)

             # ''' Add a slider bar for YZ slicing plane '''
        hbox =  Qt.QHBoxLayout()
        self.ui_yz_plane_checkbox = Qt.QCheckBox("Show YZ Cut Plane")
        self.ui_yz_plane_checkbox.setChecked(False)
        self.ui_yz_plane_checkbox.toggled.connect(self.on_checkbox_change)
        hbox.addWidget(self.ui_yz_plane_checkbox)
        self.ui_xslider = Qt.QSlider(QtCore.Qt.Horizontal)
        self.ui_xslider.valueChanged.connect(self.on_xslider_change)
        hbox.addWidget(self.ui_xslider)
        self.label_xslider = Qt.QLabel()
        hbox.addWidget(self.label_xslider)
        self.label_xslider.setText("X index:"+str(self.ui_xslider.value()))
        x_slider_widget = Qt.QWidget()
        x_slider_widget.setLayout(hbox)
        groupBox_layout.addWidget(x_slider_widget)


        groupBox_layout.addWidget(Qt.QLabel("Raycasting:"))
        
        hbox =  Qt.QHBoxLayout()
        self.ui_dvr_checkbox = Qt.QCheckBox("Show Volume Rendering: ")
        self.ui_dvr_checkbox.setChecked(False)
        self.ui_dvr_checkbox.toggled.connect(self.on_checkbox_change)
        hbox.addWidget(self.ui_dvr_checkbox)             
        ui_volWidget = Qt.QWidget()
        ui_volWidget.setLayout(hbox)
        
        self.ui_lcp_button = Qt.QPushButton('Load Control Points')
        self.ui_lcp_button.clicked.connect(self.comp_raycasting)
        self.ui_lcp_button.show()
        hbox.addWidget(self.ui_lcp_button)

        groupBox_layout.addWidget(ui_volWidget)
        
        
    def on_file_browser_clicked(self):
        dlg = Qt.QFileDialog()
        dlg.setFileMode(Qt.QFileDialog.AnyFile)
        dlg.setNameFilter("loadable files (*.vtk *.mhd)")
        
        if dlg.exec_():
            filenames = dlg.selectedFiles()
            self.ui_file_name.setText(filenames[0])
        
    def fix_dynamic_range_inner_bounds(self):
        self.ui_min_range.setMaximum(self.dynamic_max_scalar)
        self.ui_max_range.setMinimum(self.dynamic_min_scalar)
        
    def fix_iso_threshold_bounds(self):
        self.ui_iso_threshold.setMinimum(self.dynamic_min_scalar)
        self.ui_iso_threshold.setMaximum(self.dynamic_max_scalar)
    
    def open_vtk_file(self):
        '''Read and verify the vtk input file '''
        input_file_name = self.ui_file_name.text()
        
        if ".mhd" in input_file_name: #The input file is MetaImageData
            self.input_type = "mhd"
            self.reader = vtk.vtkMetaImageReader()
            self.reader.SetFileName(input_file_name)
            self.reader.Update()
        elif ".vtk" in input_file_name: # The input file is VTK
            self.input_type = "vtk"
            self.reader = vtk.vtkDataSetReader()
            self.reader.SetFileName(input_file_name)
            self.reader.Update()
            self.reader.GetOutput().GetPointData().SetActiveScalars('s')
                  
        # Some initialization to remove actors that are created previously
        if hasattr(self, 'isoSurf_actor'):
            self.ren.RemoveActor(self.isoSurf_actor)  

        if hasattr(self, 'outline'):
            self.ren.RemoveActor(self.outline) 
        
        if hasattr(self, 'xy_plane'):
            self.ren.RemoveActor(self.xy_plane)
            
        if hasattr(self, 'xz_plane'):
            self.ren.RemoveActor(self.xz_plane)
            
        if hasattr(self, 'yz_plane'):
            self.ren.RemoveActor(self.yz_plane)
            
        if hasattr(self, 'isoSurf_actor'):
            self.ren.RemoveActor(self.isoSurf_actor)

        # You probably need to remove additional actors below...
            
        # Setup full scalar range
        self.scalar_range = [self.reader.GetOutput().GetScalarRange()[0], self.reader.GetOutput().GetScalarRange()[1]]
        
        self.ui_min_label.setText("Min Scalar:"+str(self.scalar_range[0]))
        self.ui_max_label.setText("Max Scalar:"+str(self.scalar_range[1]))
        
        # Setup dynamic scalar range
        self.dynamic_min_scalar = self.scalar_range[0]
        self.dynamic_max_scalar = self.scalar_range[1]
        
        self.ui_min_range.setMinimum(self.dynamic_min_scalar)
        self.ui_min_range.setValue(self.dynamic_min_scalar)
        
        self.ui_max_range.setMaximum(self.dynamic_max_scalar)
        self.ui_max_range.setValue(self.dynamic_max_scalar)
        
        self.fix_dynamic_range_inner_bounds()
        
        #Update the lookup table
        # YOU NEED TO UPDATE THE FOLLOWING RANGE BASED ON THE LOADED DATA!!!!
        self.bwLut.SetTableRange(self.dynamic_min_scalar, self.dynamic_max_scalar/2.)
        self.bwLut.SetSaturationRange(0, 0)
        self.bwLut.SetHueRange(0, 0)
        self.bwLut.SetValueRange(0, 1)
        self.bwLut.Build()  # effective built
        
        self.dim = self.reader.GetOutput().GetDimensions()
                
        # set the range for the iso-surface spinner
        self.ui_iso_threshold.setRange(self.dynamic_min_scalar,self.dynamic_max_scalar)
        self.iso_threshold_scalar = (self.dynamic_min_scalar+self.dynamic_max_scalar)/2
        self.ui_iso_threshold.setValue(self.iso_threshold_scalar)
        self.fix_iso_threshold_bounds()
       
        # set the range for the XY cut plane range 
        self.ui_xslider.setRange(0, self.dim[0]-1)
        
        ''' Seren Lowy: added these lines '''
        self.ui_yslider.setRange(0, self.dim[1]-1)
        self.ui_zslider.setRange(0, self.dim[2]-1)
        ''''''

        # Get the data outline
        outlineData = vtk.vtkOutlineFilter()
        outlineData.SetInputConnection(self.reader.GetOutputPort())
        outlineData.Update()

        mapOutline = vtk.vtkPolyDataMapper()
        mapOutline.SetInputConnection(outlineData.GetOutputPort())

        self.outline = vtk.vtkActor()
        self.outline.SetMapper(mapOutline)
        colors = vtk.vtkNamedColors()
        self.outline.GetProperty().SetColor(colors.GetColor3d("Black"))
        self.outline.GetProperty().SetLineWidth(2.)
        
        self.ren.AddActor(self.outline)
        self.ren.ResetCamera()
        self.re_render()   
        
    def change_opacity(self, opacity):
        ''' Seren Lowy added these lines '''
        if hasattr(self, 'isoSurf_actor'):
            zero_one_opacity = opacity / 100.0
        
            self.isoSurf_actor.GetProperty().SetOpacity(zero_one_opacity)
            
            self.label_opacity_slider.setText("Opacity:"+str(zero_one_opacity))
            
            # Re-render the screen
            self.re_render()
       
    def extract_one_isosurface(self):
        # Don't render if there is no data loaded
        if not hasattr(self, 'reader'):
            return
    
        if hasattr(self, 'isoSurf_actor'):
            self.ren.RemoveActor(self.isoSurf_actor)
            
        if self.ui_isoSurf_checkbox.isChecked() == True:            
            self.isoSurfExtractor = vtk.vtkMarchingCubes()
            
            ''' Seren Lowy added these lines '''
            self.isoSurfExtractor.SetInputConnection(self.reader.GetOutputPort())
            self.isoSurfExtractor.SetValue(0, self.iso_threshold_scalar)
            
            self.isoSurfStripper = vtk.vtkStripper()
            self.isoSurfStripper.SetInputConnection(self.isoSurfExtractor.GetOutputPort())
            self.isoSurfStripper.Update()
            
            self.isoSurfMapper = vtk.vtkPolyDataMapper()
            self.isoSurfMapper.ScalarVisibilityOff()
            self.isoSurfMapper.SetInputConnection(self.isoSurfStripper.GetOutputPort())
            
            self.isoSurf_actor = vtk.vtkActor()
            self.isoSurf_actor.SetMapper(self.isoSurfMapper)
            self.ren.AddActor(self.isoSurf_actor)
            ''''''
       
        # Re-render the screen
        self.re_render()
        
    '''Seren Lowy added these functions'''
    def update_xy_plane(self, current_zID):
        self.xy_plane.SetDisplayExtent(0, self.dim[0], 0, self.dim[1], current_zID, current_zID) # Z
        
    def update_xz_plane(self, current_yID):
        self.xz_plane.SetDisplayExtent(0, self.dim[0], current_yID, current_yID, 0, self.dim[2]) # Y
    
    def update_yz_plane(self, current_xID):
        self.yz_plane.SetDisplayExtent(current_xID, current_xID, 0, self.dim[1], 0, self.dim[2]) # Y
    
    def add_xy_plane(self):
        # Don't render if there is no data loaded
        if not hasattr(self, 'reader'):
            return
            
        xy_plane_Colors = vtk.vtkImageMapToColors()
        xy_plane_Colors.SetInputConnection(self.reader.GetOutputPort())        
        
        xy_plane_Colors.SetLookupTable(self.bwLut)
        xy_plane_Colors.Update()
    
        if hasattr(self, 'xy_plane'):
            self.ren.RemoveActor(self.xy_plane)

        self.xy_plane = vtk.vtkImageActor()
        self.xy_plane.GetMapper().SetInputConnection(xy_plane_Colors.GetOutputPort())
        current_zID = int(self.ui_zslider.value())
        self.update_xy_plane(current_zID)
        
        self.ren.AddActor(self.xy_plane)
        
        # Re-render the screen
        self.re_render()
        
    def add_xz_plane(self):
        # Don't render if there is no data loaded
        if not hasattr(self, 'reader'):
            return
    
        xz_plane_Colors = vtk.vtkImageMapToColors()
        xz_plane_Colors.SetInputConnection(self.reader.GetOutputPort())
        
        xz_plane_Colors.SetLookupTable(self.bwLut)
        xz_plane_Colors.Update()
    
        if hasattr(self, 'xz_plane'):
            self.ren.RemoveActor(self.xz_plane)

        self.xz_plane = vtk.vtkImageActor()
        self.xz_plane.GetMapper().SetInputConnection(xz_plane_Colors.GetOutputPort())
        current_yID = int(self.ui_yslider.value())
        self.update_xz_plane(current_yID)
        
        self.ren.AddActor(self.xz_plane)
        
        # Re-render the screen
        self.re_render()
        
    def add_yz_plane(self):
        # Don't render if there is no data loaded
        if not hasattr(self, 'reader'):
            return
    
        # Initialize the color mapping for the cut plane
        yz_plane_Colors = vtk.vtkImageMapToColors()
        yz_plane_Colors.SetInputConnection(self.reader.GetOutputPort())
        
        yz_plane_Colors.SetLookupTable(self.bwLut)
        yz_plane_Colors.Update()
    
        if hasattr(self, 'yz_plane'):
            self.ren.RemoveActor(self.yz_plane)

        self.yz_plane = vtk.vtkImageActor()
        self.yz_plane.GetMapper().SetInputConnection(yz_plane_Colors.GetOutputPort())
        current_xID = int(self.ui_xslider.value())
        self.update_yz_plane(current_xID)
        
        self.ren.AddActor(self.yz_plane)
        
        # Re-render the screen
        self.re_render()
    ''''''
     

    ''' Cut Planes functions. Seren Lowy added y and x versions
    '''
    def on_zslider_change(self, value):
        self.label_zslider.setText("Z index:"+str(self.ui_zslider.value()))
        current_zID = int(self.ui_zslider.value())
        
        if self.ui_xy_plane_checkbox.isChecked() == True:            
            # Change plane location
            self.update_xy_plane(current_zID)
            
            # Re-render the screen
            self.re_render() 

    def on_yslider_change(self, value):
        self.label_yslider.setText("Y index:"+str(self.ui_yslider.value()))
        current_yID = int(self.ui_yslider.value())
        
        if self.ui_xz_plane_checkbox.isChecked() == True:           
            # Change plane location
            self.update_xz_plane(current_yID)
            
            # Re-render the screen
            self.re_render() 
    
    def on_xslider_change(self, value):
        self.label_xslider.setText("X index:"+str(self.ui_xslider.value()))
        current_xID = int(self.ui_xslider.value())
        
        if self.ui_yz_plane_checkbox.isChecked() == True:
            # Change plane location
            self.update_yz_plane(current_xID)
            
            # Re-render the screen
            self.re_render()

           
    ''' Handle the click event for the submit button  '''
    def on_submit_clicked(self):
        self.show_popup_message(self.ui_textfield.text())
    
    ''' Handle the dynamic range spinbox events '''
    def on_dynamic_min_spinbox_change(self, value):
        # Receive changed value
        self.dynamic_min_scalar = value
        
        # Apply safety constraints on scalar range bounds
        self.fix_dynamic_range_inner_bounds()
        self.fix_iso_threshold_bounds()
        
        # Update range state
        self.bwLut.SetTableRange(self.dynamic_min_scalar, self.dynamic_max_scalar/2.)
        
        # Re-render the screen
        self.re_render()
    
    def on_dynamic_max_spinbox_change(self, value):
        # Receive changed value
        self.dynamic_max_scalar = value
        
        # Apply safety constraints on scalar range bounds
        self.fix_dynamic_range_inner_bounds()
        self.fix_iso_threshold_bounds()
        
        # Update range state
        self.bwLut.SetTableRange(self.dynamic_min_scalar, self.dynamic_max_scalar/2.)
        
        # Re-render the screen
        self.re_render()
        
    def on_iso_threshold_spinbox_change(self, value):
        # Receive changed value
        self.iso_threshold_scalar = value
        
        # Re-render the screen
        self.re_render()
            

    '''TODO: You need to complete the following for Raycasting '''
    def comp_raycasting(self):
        # Don't render if the show checkbox is not checked
        if self.ui_dvr_checkbox.isChecked() == False:
            return
            
        # Don't render if there is no data loaded
        if not hasattr(self, 'reader'):
            return
    
        # Remove previous result
        if hasattr(self, 'volume'):
            self.ren.RemoveViewProp(self.volume)
    
        # Load the rendering configuration file that contains
        # control points for color and opacity transfer function
        self.load_color_transfer_values()
        
        # The volume will be displayed by ray-cast alpha compositing.
        # A ray-cast mapper is needed to do the ray-casting.
        volumeMapper = vtk.vtkSmartVolumeMapper()
        volumeMapper.SetInputConnection(self.reader.GetOutputPort())

        # The following added the control points to the color transfer function
        # The control points are loaded from a file
        volumeColor = vtk.vtkColorTransferFunction()
        for colorMap in self.volume_colors:
            volumeColor.AddRGBPoint(colorMap[0], colorMap[1], colorMap[2], colorMap[3])
        
    
        # The following added the control points to the opacity transfer function
        # The control points are loaded from a file
        volumeScalarOpacity = vtk.vtkPiecewiseFunction()
        for opacityMap in self.volume_opacity:
            volumeScalarOpacity.AddPoint(opacityMap[0], opacityMap[1])

    
        # Use gradient information to enhanced DVR
        volumeGradientOpacity = vtk.vtkPiecewiseFunction()
        for opacityMap in self.volume_gradient_opacity:
            volumeGradientOpacity.AddPoint(opacityMap[0], opacityMap[1])    
        
        # Next, you should set the volume property
        volumeProperty = vtk.vtkVolumeProperty()
        volumeProperty.SetColor(volumeColor)
        volumeProperty.SetScalarOpacity(volumeScalarOpacity)
        volumeProperty.SetGradientOpacity(volumeGradientOpacity)
        volumeProperty.SetInterpolationTypeToLinear()
    
        # Create a vtkVolume object 
        # set its mapper created above and its property.
        self.volume = vtk.vtkVolume()
        self.volume.SetMapper(volumeMapper)
        self.volume.SetProperty(volumeProperty)
    
        # Finally, add the volume to the renderer
        self.ren.AddViewProp(self.volume)
        
        # Re-render the screen after any change
        self.re_render()
        
     
    ''' Handle the checkbox button event '''
    def on_checkbox_change(self):
        if self.ui_xy_plane_checkbox.isChecked() == False:
            # Remove cut plane actor    
            if hasattr(self, 'xy_plane'):
                self.ren.RemoveActor(self.xy_plane)
            
        ''' Seren Lowy added these lines '''
        if self.ui_xz_plane_checkbox.isChecked() == False:
            # Remove cut plane actor   
            if hasattr(self, 'xz_plane'):
                self.ren.RemoveActor(self.xz_plane)
        
        if self.ui_yz_plane_checkbox.isChecked() == False:
            # Remove cut plane actor
            if hasattr(self, 'yz_plane'):
                self.ren.RemoveActor(self.yz_plane)
            
        if self.ui_xy_plane_checkbox.isChecked() == True:
            # Add cut plane actor
            self.add_xy_plane()
            
        if self.ui_xz_plane_checkbox.isChecked() == True:  
            # Add cut plane actor
            self.add_xz_plane()
        
        if self.ui_yz_plane_checkbox.isChecked() == True:   
            # Add cut plane actor
            self.add_yz_plane()
                
        ''''''
           
        if self.ui_isoSurf_checkbox.isChecked() == False:
            if hasattr(self, 'isoSurf_actor'):
                self.ren.RemoveActor(self.isoSurf_actor)
            

        if self.ui_dvr_checkbox.isChecked() == False:
            if hasattr(self, 'volume'):
                self.ren.RemoveViewProp(self.volume)
            
        else:
            if hasattr(self, 'volume'):
                self.ren.RemoveViewProp(self.volume)
            self.comp_raycasting()
            
            
        # Re-render the screen after any change
        self.re_render()
            
    '''
        Load the color and opacity transfer values from the configuration file
        The default file name is "rendering_config.txt"
        Here is a sample configuration file:
            #Color
            0, 0.0, 0.0, 0.0
            500, 1.0, 0.5, 0.3
            1000, 1.0, 0.5, 0.3
            1150, 1.0, 1.0, 0.9

            #Opacity
            0, 0.00
            500, 0.15
            1000, 0.15
            1150, 0.85
    '''
    
    ''' Seren Lowy modified this function to accept gradient opacity data from the config text file. '''
    def load_color_transfer_values(self):
        fileName = "rendering_config.txt"
        self.volume_colors = []
        self.volume_opacity = []
        self.volume_gradient_opacity = []
        with open(fileName, 'r') as f:
            isLoadColor = False
            isLoadOpacity = False
            isLoadGradientOpacity = False
            for line in f:    
                if len(line)>1:
                    if "#Color" in line:
                        isLoadColor = True
                        continue
                    if "#Opacity" in line:
                        isLoadColor = False
                        isLoadOpacity = True
                        continue
                    if "#GradientOpacity" in line:
                        isLoadColor = False
                        isLoadOpacity = False
                        isLoadGradientOpacity = True
                        continue
                    
                    line = line.replace("\n",'')
                    line = line.replace(" ",'')
                    line = line.split(",")
                    if isLoadColor:
                        scalar_value = float(line[0])
                        r = float(line[1])
                        g = float(line[2])
                        b = float(line[3])
                        self.volume_colors.append([scalar_value,r,g,b])
                        
                    if isLoadOpacity:
                        scalar_value = float(line[0])
                        opacity = float(line[1])
                        self.volume_opacity.append([scalar_value,opacity])
                        
                    if isLoadGradientOpacity:
                        scalar_value = float(line[0])
                        opacity = float(line[1])
                        self.volume_gradient_opacity.append([scalar_value,opacity])
                        
        # Re-render the screen after any change
        self.re_render()

        
if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())