#!/usr/bin/python

'''
    Name: Seren Lowy
    
    The main script for the HW1 VTK windowed application. Adapted from provided skeleton code.
    
    Sources: 
    [1] assignment sample code
    [3] own work
    
    Load the unstructured/structured grid data with the given file name (and directory) 
    and compute and visualize the iso-contours with the given iso-value.
    
'''


import sys
import vtk
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import Qt
import math


from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from hw1_2 import getColorTable, rainbow_scale, blue_white_red_scale, heat_scale, gray_scale, black, yellow
from hw1_3 import category_scale

'''
    The Qt MainWindow class
    A vtk widget and the ui controls will be added to this main window
'''
class MainWindow(Qt.QMainWindow):   # [1] 
    # Define a palette of color scale functions from hw1_2.py
    color_scale_functions = [rainbow_scale, blue_white_red_scale, heat_scale, gray_scale, category_scale]

    def __init__(self, parent = None): # [1] 
        Qt.QMainWindow.__init__(self, parent)
        
        ''' Step 1: Initialize the Qt window '''
        self.setWindowTitle("COSC 6344 Visualization - Assignment 1, Seren Lowy")
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
        
        ''' Step 3: Add the control panel to the right hand side of the central widget '''
        # Note: To add a widget, we first need to create a widget, then set the layout for it
        self.right_panel_widget = Qt.QWidget() # create a widget
        self.right_panel_layout = Qt.QVBoxLayout() # set layout - lines up the controls vertically
        self.right_panel_widget.setLayout(self.right_panel_layout) #assign the layout to the widget
        self.mainLayout.addWidget(self.right_panel_widget) # now, add it the the central frame
        
        # The controls will be added here
        self.add_controls()
        
    def init_vtk_widget(self): # [1] 
        vtk.vtkObject.GlobalWarningDisplayOff() #Disable vtkOutputWindow
        
        # Create the graphics structure. The renderer renders into the render
        # window. The render window interactor captures mouse events and will
        # perform appropriate camera or actor manipulation depending on the
        # nature of the events.
        self.ren = vtk.vtkRenderer() 
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        colors = vtk.vtkNamedColors()
        self.ren.SetBackground(colors.GetColor3d("Gray")) # you can change the background color here
        
        #Initialize some varibables for vtk to re-render the screen 
        #when the user change the color scheme
        self.vtk_poly_mapper = vtk.vtkPolyDataMapper()
        self.lut = vtk.vtkLookupTable()
        self.color_scheme = 0
        
        
        # Start the vtk screen
        self.ren.ResetCamera()
        
        self.show()
        self.iren.Initialize()
        self.iren.Start()
    
    
    def show_popup_message(self,msg):
        alert = Qt.QMessageBox()
        alert.setText(msg)
        alert.exec_()
    
    '''
        Assignment 2 Task 4
        Add controls to the control panel
        Implement the GUI interface elements
        Complete code where TODO is commented!
    '''
    def add_controls(self): # [1, 3]
        groupBox = Qt.QGroupBox("Iso-Contour Extraction") # Use a group box to group controls
        groupBox_layout = Qt.QVBoxLayout() #lines up the controls vertically
        groupBox.setLayout(groupBox_layout) 
        self.right_panel_layout.addWidget(groupBox)
        
        ''' Add a textfield ( QLineEdit) to show the file path and the browser button '''
        label = Qt.QLabel("Choose a vtk structured/unstructured grid file:")
        groupBox_layout.addWidget(label)
        hbox = Qt.QHBoxLayout()
        self.qt_file_name = Qt.QLineEdit()
        hbox.addWidget(self.qt_file_name) 
        self.qt_browser_button = Qt.QPushButton('Browser')
        self.qt_browser_button.clicked.connect(self.on_file_browser_clicked)
        self.qt_browser_button.show()
        hbox.addWidget(self.qt_browser_button)
        file_widget = Qt.QWidget()
        file_widget.setLayout(hbox)
        groupBox_layout.addWidget(file_widget)
        
        ''' Add the Open button '''
        self.qt_open_button = Qt.QPushButton('Open')
        self.qt_open_button.clicked.connect(self.open_vtk_file)
        self.qt_open_button.show()
        groupBox_layout.addWidget(self.qt_open_button)
        
        ''' Add the color scheme selection '''
        groupBox_layout.addWidget(Qt.QLabel("Select a color scheme:"))
        self.qt_color_scheme = Qt.QComboBox()
        self.qt_color_scheme.addItem("Rainbow")
        self.qt_color_scheme.addItem("BlueWhiteRed")
        self.qt_color_scheme.addItem("Heat")
        self.qt_color_scheme.addItem("Gray")
        self.qt_color_scheme.addItem("Category")

        self.qt_color_scheme.currentIndexChanged.connect(self.select_color_scheme)
        groupBox_layout.addWidget(self.qt_color_scheme)
        
        ''' Add the min, max scalar labels '''
        self.qt_min_lable = Qt.QLabel("Min Scalar: 0")
        self.qt_max_lable = Qt.QLabel("Max Scalar: 0")
        groupBox_layout.addWidget(self.qt_min_lable)
        groupBox_layout.addWidget(self.qt_max_lable)
        
        ''' Add spinbox for scalar threshold selection '''
        groupBox_layout.addWidget(Qt.QLabel("Select the Iso-Contour threhold:"))
        self.qt_threshold = Qt.QDoubleSpinBox()
        groupBox_layout.addWidget(self.qt_threshold)
        
        '''Add the "Show Iso-Contour" button'''
        self.qt_show_isocontour_button = Qt.QPushButton('Show 1 isoContour')
        self.qt_show_isocontour_button.clicked.connect(self.extract_isocontour)
        self.qt_show_isocontour_button.show()
        groupBox_layout.addWidget(self.qt_show_isocontour_button)
        
        ''' Add spinbox for number of contours selection (and label it too)'''
        groupBox_layout.addWidget(Qt.QLabel("Select the number of isocontours:"))
        self.qt_kcontours = Qt.QDoubleSpinBox()
        groupBox_layout.addWidget(self.qt_kcontours)

        '''Add the "Show K Iso-Contours" button'''
        self.qt_show_k_isocontour_button = Qt.QPushButton('Show k isoContours')
        self.qt_show_k_isocontour_button.clicked.connect(self.extract_k_isocontours)
        self.qt_show_k_isocontour_button.show()
        groupBox_layout.addWidget(self.qt_show_k_isocontour_button)
        
        '''Add the "export iso contours" button'''
        self.qt_export_isocontour_button = Qt.QPushButton('Export isoContours')
        self.qt_export_isocontour_button.clicked.connect(self.exportLines)
        self.qt_export_isocontour_button.show()
        groupBox_layout.addWidget(self.qt_export_isocontour_button)

      
        ''' Add the Reset Camera button '''
        self.qt_reset_camera_button = Qt.QPushButton('Reset Camera')
        self.qt_reset_camera_button.clicked.connect(self.reset_camera)
        self.qt_reset_camera_button.show()
        self.right_panel_layout.addWidget(self.qt_reset_camera_button)

    def reset_camera(self): # [1]
        self.camera.SetPosition(self.initial_camera_position)
        self.camera.SetFocalPoint(self.initial_camera_focal_point)
        self.camera.SetViewUp(self.initial_camera_view_up)
        self.camera.Modified()
        self.vtkWidget.GetRenderWindow().Render()

        
    def on_file_browser_clicked(self): # [1]
        dlg = Qt.QFileDialog()
        dlg.setFileMode(Qt.QFileDialog.AnyFile)
        dlg.setNameFilter("VTK files (*.vtk)")
        
        if dlg.exec_():
            filenames = dlg.selectedFiles()
            self.qt_file_name.setText(filenames[0])
    
    def open_vtk_file(self): # [1]
        '''Read and verify the vtk input file '''
        input_file_name = self.qt_file_name.text()
        
        
        self.vtk_reader = vtk.vtkDataSetReader()
        self.vtk_reader.SetFileName(input_file_name)
        self.vtk_reader.Update()
        self.scalar_range=[0,0]
        
        if hasattr(self, 'vtk_k_contour_actor'):
            self.ren.RemoveActor(self.vtk_k_contour_actor)

        if hasattr(self, 'vtk_contour_actor'):
            self.ren.RemoveActor(self.vtk_contour_actor)
        
        # Verify the format of the vtk
        if self.vtk_reader.IsFileStructuredGrid() or self.vtk_reader.IsFileUnstructuredGrid():
            self.show_popup_message('The input file is the vtk unstructured/structured grid data !')
            
            # Use geometry filter to get the geometry representation for vtkStructuredGrid 
            vtk_geometry = vtk.vtkGeometryFilter()
            if self.vtk_reader.IsFileStructuredGrid():
                vtk_geometry.SetInputData(self.vtk_reader.GetStructuredGridOutput())
            elif self.vtk_reader.IsFileUnstructuredGrid:
                vtk_geometry.SetInputData(self.vtk_reader.GetUnstructuredGridOutput())
            vtk_geometry.Update()
            
            # Get the scalar field and update the value ranges 
            scalar_field = "s" # Assume there is a scalar field named "s" in the vtk file
            print(vtk_geometry.GetOutput().GetPointData().GetArray(scalar_field))
            min_scalar,max_scalar = vtk_geometry.GetOutput().GetPointData().GetArray(scalar_field).GetRange()
            self.qt_min_lable.setText("Min Scalar:"+str(min_scalar))
            self.qt_max_lable.setText("Max Scalar:"+str(max_scalar))
            self.qt_threshold.setValue((min_scalar+max_scalar)/2)
            
            self.scalar_range = (min_scalar, max_scalar)
            
            # Set data for the poly data mapper.
            self.vtk_poly_mapper.SetInputData(vtk_geometry.GetOutput()) # You can also use .SetInputConnection and .GetOutputPort() here
            
            #Create vtk color lookup table and use it for the color mapping
            self.color_resolution = 256
            self.lut = getColorTable(self.color_resolution, 
                                     self.color_scale_functions[self.color_scheme])
                                     
            
            self.vtk_poly_mapper.SetScalarModeToUsePointData()
            
            self.vtk_poly_mapper.SetLookupTable(self.lut)
            self.vtk_poly_mapper.SetScalarRange(min_scalar, max_scalar)
            self.vtk_poly_mapper.SelectColorArray(scalar_field);
            
            # Add vtk actor
            vtk_actor = vtk.vtkActor()
            vtk_actor.SetMapper(self.vtk_poly_mapper)
            self.ren.AddActor(vtk_actor)
            
            # Add color legend
            self.add_color_legend()
            
            self.ren.ResetCamera()
            self.vtkWidget.GetRenderWindow().Render()
            
        elif self.vtk_reader.IsFilePolyData(): # [1, 3]
            self.show_popup_message('The input file is the vtk poly data!')

            # Get the scalar field and update the value ranges 
            scalar_field = "s" # Assume there is a scalar field named "s" in the vtk file
            scalar_field_array = self.vtk_reader.GetPolyDataOutput().GetPointData().GetArray(scalar_field)
            
            # Check for categorical data array (CHANGED by Seren)
            if scalar_field_array:
                self.vtk_poly_mapper.SetScalarModeToUsePointData()
                point_data = self.vtk_reader.GetPolyDataOutput().GetPointData()
                point_data.SetActiveScalars(scalar_field)
            else:
                cell_data = self.vtk_reader.GetPolyDataOutput().GetCellData()
                scalar_field_array = cell_data.GetArray(scalar_field)
                cell_data.SetActiveScalars(scalar_field)
                
                # Set scalar mode to use cell data if the dataset is categorical!
                self.vtk_poly_mapper.SetScalarModeToUseCellData()
                
            min_scalar, max_scalar = scalar_field_array.GetRange()
            
            self.qt_min_lable.setText("Min Scalar:"+str(min_scalar))
            self.qt_max_lable.setText("Max Scalar:"+str(max_scalar))
            self.qt_threshold.setValue((min_scalar+max_scalar)/2)
            
            self.scalar_range = (min_scalar, max_scalar)
            
            print(self.scalar_range)
            
            # Set data for the poly data mapper
            self.vtk_poly_mapper.SetInputConnection(self.vtk_reader.GetOutputPort()) # You can also use .SetInputConnection and .GetOutputPort() here
            
            #Create vtk color lookup table and use it for the color mapping
            self.color_resolution = 256
            self.lut = getColorTable(self.color_resolution, 
                                     self.color_scale_functions[self.color_scheme])
            
            self.vtk_poly_mapper.SetLookupTable(self.lut)
            self.vtk_poly_mapper.SetScalarRange(min_scalar, max_scalar)
            self.vtk_poly_mapper.SelectColorArray(scalar_field);
            
            # Add vtk actor
            vtk_actor = vtk.vtkActor()
            vtk_actor.SetMapper(self.vtk_poly_mapper)
            self.ren.AddActor(vtk_actor)
            
            # Add color legend
            self.add_color_legend()
            
            self.ren.ResetCamera()
            self.vtkWidget.GetRenderWindow().Render()
            
        else:
            self.show_popup_message('Cannot read the input file!')
            
        camera = self.ren.GetActiveCamera()
        self.initial_camera_position = camera.GetPosition()
        self.initial_camera_focal_point = camera.GetFocalPoint()
        self.initial_camera_view_up = camera.GetViewUp()
        self.camera = camera
        
    '''
    Assignment 1 Task 4.1
    '''
    def extract_isocontour(self): # [1, 3]
        # Delete the previous iso-contour
        if hasattr(self, 'vtk_contour_actor'):
            self.ren.RemoveActor(self.vtk_contour_actor)
            
        #Create iso-contour here with vtkContourFilter
        self.contour_filter = vtk.vtkContourFilter()
        self.contour_filter.SetInputConnection(self.vtk_reader.GetOutputPort())
        self.contour_filter.SetValue(0, self.qt_threshold.value())
        
        # Create a mapper for the extract contour geometry here
        self.vtk_contour_mapper = vtk.vtkPolyDataMapper()
        self.vtk_contour_mapper.SetInputConnection(self.contour_filter.GetOutputPort())
       
        #Update contour actor   
        self.vtk_contour_actor = vtk.vtkActor()

        # set the mapper for this actor using the above contour mapper here
        self.vtk_contour_actor.SetMapper(self.vtk_contour_mapper)

        # The following set the color and thickness of the contours
        colors = vtk.vtkNamedColors()
        self.vtk_contour_actor.GetProperty().SetColor(black)
        self.vtk_contour_actor.GetProperty().SetLineWidth(2)

        # Add the actor for the contours here
        self.ren.AddActor(self.vtk_contour_actor)
        
        # Re-render the screen
        self.vtkWidget.GetRenderWindow().Render()
        
    '''
    Assignment 1 Task 4.2
    '''
    def extract_k_isocontours(self): # [1, 3]
        # Delete the previous iso-contours
        if hasattr(self, 'vtk_k_contour_actor'):
            self.ren.RemoveActor(self.vtk_k_contour_actor)
            
        #Create iso-contour here with vtkContourFilter
        self.k_contour_filter = vtk.vtkContourFilter()
        self.k_contour_filter.SetInputConnection(self.vtk_reader.GetOutputPort())
        self.k_contour_filter.GenerateValues(int(self.qt_kcontours.value()), self.vtk_reader.GetOutput().GetScalarRange())
        
        # Create a mapper for the extract contour geometry here
        self.vtk_k_contour_mapper = vtk.vtkPolyDataMapper()
        self.vtk_k_contour_mapper.SetInputConnection(self.k_contour_filter.GetOutputPort())

        #Update contour actor   
        self.vtk_k_contour_actor = vtk.vtkActor()

        # set the mapper for this actor using the above contour mapper here
        self.vtk_k_contour_actor.SetMapper(self.vtk_k_contour_mapper)

        # The following set the color and thickness of the contours
        colors = vtk.vtkNamedColors()
        self.vtk_k_contour_actor.GetProperty().SetColor(yellow)
        self.vtk_k_contour_actor.GetProperty().SetLineWidth(2)

         # Add the actor for the contours here
        self.ren.AddActor(self.vtk_k_contour_actor)
        
        # Re-render the screen
        self.vtkWidget.GetRenderWindow().Render()

           
    def select_color_scheme(self, i):
        self.color_scheme = i
        self.color_resolution = 256
        
        self.lut = getColorTable(self.color_resolution, 
                                 self.color_scale_functions[self.color_scheme])
        self.vtk_poly_mapper.SetLookupTable(self.lut)
        self.color_legend.SetLookupTable(self.lut)
        self.vtkWidget.GetRenderWindow().Render()
        
    def add_color_legend(self):
        # Remove previous color legend if there is
        if hasattr(self, 'color_legend'):
            self.ren.RemoveActor(self.color_legend)
    
        # Add scalar bar
        self.color_legend = vtk.vtkScalarBarActor()
        self.color_legend.SetLookupTable(self.vtk_poly_mapper.GetLookupTable())
        self.color_legend.SetNumberOfLabels(4);
        self.color_legend.SetBarRatio(0.1)
        self.color_legend.SetUnconstrainedFontSize(True) # The font size of title and labels is relative to the size of the bar
        self.color_legend.SetMaximumHeightInPixels(100) # Set the height of the bar
        self.ren.AddActor2D(self.color_legend);
        
    '''
    TODO: export the iso contour lines using vtkPolyDataWriter
    you can consult this example: https://stackoverflow.com/q/59301207
    1. create a new vtkPolyDataWriter object
    2. set the writer's InputData to the iso contour mapper's input 
    3. set the writer's file nam
    4. Write()
    '''
    def exportLines(self):

        pass

'''
    Assignment 2 Task 2
'''
### Please see the file hw1_2.py
      

if __name__ == "__main__": # [1]
    app = Qt.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())

