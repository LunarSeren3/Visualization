#!/usr/bin/python

'''
    Visualization assignment 4: 3D steady vector fields
    Based on skeleton code from class
    Seren Lowy (1449248)
'''


import sys
import math
import random
import vtk
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import Qt
import numpy as np
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor



'''
    The Qt MainWindow class
    A vtk widget and the ui controls will be added to this main window
'''
class MainWindow(Qt.QMainWindow):

    def __init__(self, parent = None):
        Qt.QMainWindow.__init__(self, parent)
        
        ''' Step 1: Initialize the Qt window '''
        self.setWindowTitle("COSC 6344 Visualization HW4 - Seren Lowy")
        self.resize(1200,int(self.height()*1.4))
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
        #vtk.vtkObject.GlobalWarningDisplayOff() #Disable vtkOutputWindow - Comment out this line if you want to see the warning/error messages from vtk
        
        # Create the graphics structure. The renderer renders into the render
        # window. The render window interactor captures mouse events and will
        # perform appropriate camera or actor manipulation depending on the
        # nature of the events.
        self.ren = vtk.vtkRenderer() 
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        # The following set the interactor for 2D image style (i.e., no rotation)
        #style = vtk.vtkInteractorStyleImage()
        #self.iren.SetInteractorStyle(style)
        self.ren.SetBackground(0.8,0.8,0.8) # you can change the background color here

        # Start the vtk screen
        self.ren.ResetCamera()
        self.show()
        self.iren.Initialize()
        self.iren.Start()

    '''
        Add QT controls to the control panel in the righ hand size
    '''
    def add_controls(self):
    
        ''' Add a sample group box '''
        groupBox = Qt.QGroupBox("3D Vector Field Visualization") # Use a group box to group controls
        self.groupBox_layout = Qt.QVBoxLayout() #lines up the controls vertically
        groupBox.setLayout(self.groupBox_layout) 
        self.right_panel_layout.addWidget(groupBox)
  
        ''' Add a textfield ( QLineEdit) to show the file path and the browser button '''
        label = Qt.QLabel("Choose a file (e.g., vtk):")
        self.groupBox_layout.addWidget(label)
        hbox = Qt.QHBoxLayout()
        self.qt_file_name = Qt.QLineEdit()
        hbox.addWidget(self.qt_file_name) 
        self.qt_browser_button = Qt.QPushButton('Browser')
        self.qt_browser_button.clicked.connect(self.on_file_browser_clicked)
        self.qt_browser_button.show()
        hbox.addWidget(self.qt_browser_button)
        file_widget = Qt.QWidget()
        file_widget.setLayout(hbox)
        self.groupBox_layout.addWidget(file_widget)
 
        ''' Add the Open button '''
        self.qt_open_button = Qt.QPushButton('Open')
        self.qt_open_button.clicked.connect(self.open_vtk_file)
        self.qt_open_button.show()
        self.groupBox_layout.addWidget(self.qt_open_button)
        
        ''' Seren modified UI code for arrow options group '''
        ''' Add the widgets for arrow plot '''
        sample_groupbox = Qt.QGroupBox("Arrow Options")
        vbox_arrow = Qt.QVBoxLayout()  # New QVBoxLayout for all arrow items
        vbox_arrow2 = Qt.QVBoxLayout()
        
        # Arrow scale spinbox
        hbox_arrowplot = Qt.QHBoxLayout()
        # Arrow plot checkbox
        self.qt_arrow_checkbox = Qt.QCheckBox("Arrow Plot ")
        self.qt_arrow_checkbox.setChecked(False)
        self.qt_arrow_checkbox.toggled.connect(self.on_arrow_checkbox_change)
        hbox_arrowplot.addWidget(self.qt_arrow_checkbox)
        
        hbox_arrowplot2 = Qt.QHBoxLayout()
        arrowscaleLabel = Qt.QLabel("Choose arrow scale:")
        hbox_arrowplot2.addWidget(arrowscaleLabel)
        self.arrow_scale = Qt.QDoubleSpinBox()
        self.arrow_scale.setValue(0.03)
        self.arrow_scale.setRange(0, 5)
        self.arrow_scale.setSingleStep(0.01)
        hbox_arrowplot2.addWidget(self.arrow_scale)
        
        ''' Add down sampling rate widget '''
        hbox_arrowplot3 = Qt.QHBoxLayout()
        sampleRateLabel = Qt.QLabel("Sampling - Number of arrows: ")
        hbox_arrowplot3.addWidget(sampleRateLabel)
        self.sample_rate = Qt.QSpinBox()
        self.sample_rate.setRange(100, 50000)
        self.sample_rate.setValue(50000)
        self.sample_rate.setSingleStep(100)
        hbox_arrowplot3.addWidget(self.sample_rate)
        
        vbox_arrow.addLayout(hbox_arrowplot)
        vbox_arrow2.addLayout(hbox_arrowplot2)
        vbox_arrow2.addLayout(hbox_arrowplot3)
        ''''''
        
        # Radio buttons for sampling options
        self.radio_all_points = Qt.QRadioButton("All grid points")
        self.radio_all_points.setChecked(True)
        self.radio_uniform_sample = Qt.QRadioButton("Uniform Sample")
        self.radio_random_sample = Qt.QRadioButton("Random Sample")
        
        # Add radio buttons to QButtonGroup
        self.arrow_radio_group = Qt.QButtonGroup()
        self.arrow_radio_group.addButton(self.radio_all_points)
        self.arrow_radio_group.addButton(self.radio_uniform_sample)
        self.arrow_radio_group.addButton(self.radio_random_sample)
        self.arrow_radio_group.buttonClicked.connect(self.on_arrow_checkbox_change)

        vbox_arrow.addWidget(self.radio_all_points)
        vbox_arrow.addWidget(self.radio_uniform_sample)
        vbox_arrow.addWidget(self.radio_random_sample)
        
        hbox_arrow_outer = Qt.QHBoxLayout()
        hbox_arrow_outer.addLayout(vbox_arrow)
        hbox_arrow_outer.addLayout(vbox_arrow2)
        sample_groupbox.setLayout(hbox_arrow_outer)
        self.groupBox_layout.addWidget(sample_groupbox)

        ''' Create a new QGroupBox for streamline options '''
        streamline_groupbox = Qt.QGroupBox("Streamline Options")
        vbox_streamline = Qt.QVBoxLayout()
        
        self.qt_pt_checkbox = Qt.QCheckBox("Show Seed Pts")
        self.qt_pt_checkbox.setChecked(False)
        self.qt_pt_checkbox.toggled.connect(self.on_streamline_checkbox_change)
        
        hbox_streamline = Qt.QHBoxLayout()
        self.qt_streamline_checkbox = Qt.QCheckBox("Streamline ")
        self.qt_streamline_checkbox.setChecked(False)
        self.qt_streamline_checkbox.toggled.connect(self.on_streamline_checkbox_change)
        hbox_streamline.addWidget(self.qt_streamline_checkbox) 

        seedLabel = Qt.QLabel("    Set number of seeds:")
        hbox_streamline.addWidget(seedLabel)
        
        self.number_seeds = Qt.QSpinBox()
        # set the initial values of some random parameters
        self.number_seeds.setValue(27)
        self.number_seeds.setRange(1, 2000)
        self.number_seeds.setSingleStep(1)
        hbox_streamline.addWidget(self.number_seeds)
        streamline_hwidget = Qt.QWidget()
        streamline_hwidget.setLayout(hbox_streamline)
        vbox_streamline.addWidget(streamline_hwidget)
        
        hbox_streamline = Qt.QHBoxLayout()
        self.qt_pt_checkbox = Qt.QCheckBox("Show Seed Points ")
        self.qt_pt_checkbox.setChecked(False)
        self.qt_pt_checkbox.toggled.connect(self.on_represent_style)
        hbox_streamline.addWidget(self.qt_pt_checkbox) 

        seedLabel = Qt.QLabel("    Seed pt radius:")
        hbox_streamline.addWidget(seedLabel)
        
        self.radius_seeds = Qt.QDoubleSpinBox()
        # set the initial values of some random parameters
        self.radius_seeds.setValue(0.06)
        self.radius_seeds.setRange(0.001, 100)
        self.radius_seeds.setSingleStep(0.1)
        hbox_streamline.addWidget(self.radius_seeds)
        streamline_hwidget = Qt.QWidget()
        streamline_hwidget.setLayout(hbox_streamline)
        vbox_streamline.addWidget(streamline_hwidget)
        
        vbox_seed_strategy = Qt.QVBoxLayout()
        l=Qt.QLabel("Select streamline seeding strategy")
        vbox_seed_strategy.addWidget(l)
        
        # Add radio buttons for the selection of the seed generation strategy
        self.uniform_seed_radio = Qt.QRadioButton("Uniform Seeding")
        self.uniform_seed_radio.setChecked(True)
        self.uniform_seed_radio.toggled.connect(self.on_seeding_strategy)
        vbox_seed_strategy.addWidget(self.uniform_seed_radio)
        
        self.random_seed_radio = Qt.QRadioButton("Random Seeding")
        self.random_seed_radio.setChecked(False)
        self.random_seed_radio.toggled.connect(self.on_seeding_strategy)
        vbox_seed_strategy.addWidget(self.random_seed_radio)
        
        self.line_seed_radio = Qt.QRadioButton("Seeding Line Widget")
        self.line_seed_radio.setChecked(False)
        self.line_seed_radio.toggled.connect(self.on_seeding_strategy)
        vbox_seed_strategy.addWidget(self.line_seed_radio)
        self.seeding_strategy = 0 # Uniform seeding is the default strategy 
        
        seedingstrategy = Qt.QWidget()
        seedingstrategy.setLayout(vbox_seed_strategy)
        vbox_streamline.addWidget(seedingstrategy)
        
        vbox_seed_strategy = Qt.QVBoxLayout()
        l=Qt.QLabel("Select streamline rendering representation strategy")
        vbox_seed_strategy.addWidget(l)
        
        # Add radio buttons for the selection of the seed generation strategy
        self.line_rep_radio = Qt.QRadioButton("Line Representation")
        self.line_rep_radio.setChecked(True)
        self.line_rep_radio.toggled.connect(self.on_represent_style)
        vbox_seed_strategy.addWidget(self.line_rep_radio)
        
        self.tube_rep_radio = Qt.QRadioButton("Tube Representation")
        self.tube_rep_radio.setChecked(False)
        self.tube_rep_radio.toggled.connect(self.on_represent_style)
        vbox_seed_strategy.addWidget(self.tube_rep_radio)
        
        self.ribbon_rep_radio = Qt.QRadioButton("Ribbon Representation")
        self.ribbon_rep_radio.setChecked(False)
        self.ribbon_rep_radio.toggled.connect(self.on_represent_style)
        vbox_seed_strategy.addWidget(self.ribbon_rep_radio)
        
        self.surface_rep_radio = Qt.QRadioButton("Surface Representation")
        self.surface_rep_radio.setChecked(False)
        self.surface_rep_radio.toggled.connect(self.on_represent_style)
        vbox_seed_strategy.addWidget(self.surface_rep_radio)
        self.rep_strategy = 0 # Uniform seeding is the default strategy 
        
        seedingstrategy = Qt.QWidget()
        seedingstrategy.setLayout(vbox_seed_strategy)
        vbox_streamline.addWidget(seedingstrategy)
        
        streamline_groupbox.setLayout(vbox_streamline)
        self.groupBox_layout.addWidget(streamline_groupbox)
        

        
    def on_file_browser_clicked(self):
        dlg = Qt.QFileDialog()
        dlg.setFileMode(Qt.QFileDialog.AnyFile)
        dlg.setNameFilter("loadable files (*.vtk)")
        
        if dlg.exec_():
            filenames = dlg.selectedFiles()
            self.qt_file_name.setText(filenames[0])
    
    def open_vtk_file(self):
       
        '''Read and verify the vtk input file '''
        input_file_name = self.qt_file_name.text()

        self.input_type = "vtk"
        original_reader = vtk.vtkDataSetReader()
        original_reader.SetFileName(input_file_name)
        original_reader.Update()
    
        self.reader = original_reader
            

        # Some initialization to remove actors that are created previously

        if hasattr(self, 'outline'):
            self.ren.RemoveActor(self.outline)

        if hasattr(self, 'arrow_actor'):
           self.ren.RemoveActor(self.arrow_actor)
        
        if hasattr(self, 'sphere_actor'):
           self.ren.RemoveActor(self.sphere_actor)

        if hasattr(self, 'streamline_actor'):
           self.ren.RemoveActor(self.streamline_actor)

        self.seeding_strategy = 0  # Uniform seeding is the default strategy

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
        self.vtkWidget.GetRenderWindow().Render()

    '''                         '''
    ''' Question 2. Arrow Plot  '''
    '''                         '''
    def on_arrow_checkbox_change(self, discard=False):
        if hasattr(self, 'arrow_actor'):
                self.ren.RemoveActor(self.arrow_actor)
    
        if self.qt_arrow_checkbox.isChecked() == True:
            # Make sure we use the velocity field
            self.reader.GetOutput().GetPointData().SetActiveVectors("velocity")

            ''' Based on similar section from HW3 '''
            # Setup mask object
            densityFilter = vtk.vtkMaskPoints()
            densityFilter.SetInputData(self.reader.GetOutput())
                    
            sample = self.sample_rate.value()
            densityFilter.SetMaximumNumberOfPoints(sample)
            
            # Choose the type of glyphs as arrows
            arrowSource = vtk.vtkArrowSource()
            
            # Setup glyph object
            glyph3D = vtk.vtkGlyph3D()
            glyph3D.SetSourceConnection(arrowSource.GetOutputPort())
            glyph3D.OrientOn()
            glyph3D.SetScaleModeToScaleByVector()
            glyph3D.SetScaleFactor(self.arrow_scale.value()) # adjust the length of the arrows accordingly
        
            selected_id = self.arrow_radio_group.checkedId()
            if selected_id == -2:
                print("All grid points is selected.")
                
                # Connect glyph object to reader without density filter if we are not down sampling
                glyph3D.SetInputData(self.reader.GetOutput())
                
            else:
                # Connect glyph object to density filter if we are down sampling
                glyph3D.SetInputData(densityFilter.GetOutput())
                densityFilter.RandomModeOn()
                
                if selected_id == -3:
                    print("Uniform Sample is selected.")
                    
                    # UNIFORM_SPATIAL_BOUNDS random mode
                    densityFilter.SetRandomModeType(3)
                
                elif selected_id == -4:
                    print("Random Sample is selected.")
                    
                    # RANDOM_SAMPLING random mode
                    densityFilter.SetRandomModeType(1)
                
                # Update density filter 
                densityFilter.Update()
                
            # Update glyph object after receiving input data
            glyph3D.Update()            

            # Mapper and actor
            arrows_mapper = vtk.vtkPolyDataMapper()
            arrows_mapper.SetInputConnection(glyph3D.GetOutputPort())
            arrows_mapper.ScalarVisibilityOff()
            arrows_mapper.Update()

            self.arrow_actor = vtk.vtkActor()
            self.arrow_actor.SetMapper(arrows_mapper)
            self.arrow_actor.GetProperty().SetColor(0.0,0.5,1.0) # set the color you want
            
            self.ren.AddActor(self.arrow_actor)
            
        # Re-render the screen
        self.vtkWidget.GetRenderWindow().Render()



    '''                         '''
    ''' Question 3. Streamlines '''
    '''                         '''
            
    '''event handle for the radio buttons of seeding strategies
    '''
    def on_seeding_strategy(self):
        if self.uniform_seed_radio.isChecked() == True:
            self.random_seed_radio.setChecked(False)
            self.line_seed_radio.setChecked(False)
            self.seeding_strategy = 0
        elif self.random_seed_radio.isChecked() ==  True:
            self.uniform_seed_radio.setChecked(False)
            self.line_seed_radio.setChecked(False)
            self.seeding_strategy = 1
        elif self.line_seed_radio.isChecked() ==  True:
            self.uniform_seed_radio.setChecked(False)
            self.random_seed_radio.setChecked(False)
            self.seeding_strategy = 2
        
        # Route event to checkbox_change event when done so streamline plot updates
        self.on_streamline_checkbox_change()
            
    def on_represent_style(self):
        if self.line_rep_radio.isChecked() == True:
            self.tube_rep_radio.setChecked(False)
            self.ribbon_rep_radio.setChecked(False)
            self.surface_rep_radio.setChecked(False)
            self.rep_strategy = 0
        elif self.tube_rep_radio.isChecked() ==  True:
            self.line_rep_radio.setChecked(False)
            self.ribbon_rep_radio.setChecked(False)
            self.surface_rep_radio.setChecked(False)
            self.rep_strategy = 1
        elif self.ribbon_rep_radio.isChecked() ==  True:
            self.tube_rep_radio.setChecked(False)
            self.line_rep_radio.setChecked(False)
            self.surface_rep_radio.setChecked(False)
            self.rep_strategy = 2
            
        elif self.surface_rep_radio.isChecked() ==  True:
            self.ribbon_rep_radio.setChecked(False)
            self.tube_rep_radio.setChecked(False)
            self.line_rep_radio.setChecked(False)
            self.rep_strategy = 3
            
        if hasattr(self, 'seedPolyData'):
            self.seed_point_representation()
        
        # Update streamline representation when radio button changes 
        #  (if there are streamlines yet)
        if hasattr(self, 'streamline_mapper'):
            self.streamline_representation()
        

    ''' Same as HW3 '''
    #import math # Already imported above
    
    def map_positions_to_data_domain(self, normal_positions):
        xmin, xmax, ymin, ymax, zmin, zmax = self.reader.GetOutput().GetBounds()
        width = xmax - xmin
        height = ymax - ymin
        depth = zmax - zmin
        
        positions = [(xmin + np[0] * width, 
                      ymin + np[1] * height,
                      zmin + np[2] * depth) 
                        for np in normal_positions]
                        
        return positions
    
    def uniform_generate_seeds(self):
        num_seeds = int (self.number_seeds.value())
        seedPoints = vtk.vtkPoints()     

        
        # Define parameters for a uniform grid
        linear_dimension = int(num_seeds ** (1.0 / 3)) # Cube root
        linear_dim_fraction = 1.0 / (linear_dimension + 1)
        
        # Generate uniform positions in normal space
        normal_positions = []
        for i in range(linear_dimension):
            for j in range(linear_dimension):
                for k in range(linear_dimension):
                    x = (i + 1) * linear_dim_fraction
                    y = (j + 1) * linear_dim_fraction
                    z = (k + 1) * linear_dim_fraction
                
                    normal_positions += [(x, y, z)]
        
        # Map the normal space to the data domain
        positions = self.map_positions_to_data_domain(normal_positions)
                        
        # Create seed points with the computed positions in data space
        for pos in positions:
            seedPoints.InsertNextPoint(pos[0], pos[1], pos[2])
        ''''''
        
        
        # Need to put the seed points in a vtkPolyData object
        seedPolyData = vtk.vtkPolyData()
        seedPolyData.SetPoints(seedPoints)
        return seedPolyData

    ''' Same as HW3 '''
    def random_roll(self):
        random_resolution = 32768.0
        return random.randint(0, int(random_resolution)) / random_resolution
        
    def random_generate_seeds(self):
        num_seeds = int(self.number_seeds.value())
        seedPoints = vtk.vtkPoints()     

        ''' Same as HW3 '''
        # Generate the random positions in normal space
        normal_positions = []
        for _ in range(num_seeds):
            x = self.random_roll()
            y = self.random_roll()
            z = self.random_roll()
            
            normal_positions += [(x, y, z)]
        
        # Map the normal space to the data domain
        positions = self.map_positions_to_data_domain(normal_positions)
        
        # Create seed points with the computed positions in data space
        for pos in positions:
            seedPoints.InsertNextPoint(pos[0], pos[1], pos[2])
        ''''''
        
        # Need to put the seed points in a vtkPolyData object
        seedPolyData = vtk.vtkPolyData()
        seedPolyData.SetPoints(seedPoints)
        return seedPolyData
    
    
    '''  
        TODO: Complete the following function to create the seeding line widget
        for streamline placement
        NOTE: This is the most difficult task in the assignment!
        If you cannot figure out how to create an interactive line widget, then simply implement streamline seeding between two points (place seed points along a line formed by two points in the data set)
    '''
    def generate_seeding_line(self):
        return None


    '''  
        TODO: Complete the following function to create the interactive seeding line widget (Check the line widget documentation page on how to define and use this callback)
        NOTE: This is the most difficult task in the assignment!
        If you cannot figure out how to create an interactive line widget, then skip this callback implementation
    '''
    def GenerateStreamlinesCallBack(self, obj, event):
        pass

        
    ''' 
        TODO: Complete the following function to generate a set of streamlines
        from the above generated uniform or random seeds
    '''
    def seed_point_representation(self):
        if hasattr(self, 'sphere_actor'):
                self.ren.RemoveActor(self.sphere_actor)
                
        if self.qt_pt_checkbox.isChecked() == True:
            sphereSource = vtk.vtkSphereSource()
            
            glyph3D = vtk.vtkGlyph3D()
            glyph3D.SetSourceConnection(sphereSource.GetOutputPort())
            glyph3D.OrientOn()
            
            glyph3D.SetInputData(self.seedPolyData)
            glyph3D.SetScaleFactor(self.radius_seeds.value())
            
            glyph3D.Update()            

            # Mapper and actor
            sphere_mapper = vtk.vtkPolyDataMapper()
            sphere_mapper.SetInputConnection(glyph3D.GetOutputPort())
            sphere_mapper.ScalarVisibilityOff()
            sphere_mapper.Update()

            self.sphere_actor = vtk.vtkActor()
            self.sphere_actor.SetMapper(sphere_mapper)
            self.sphere_actor.GetProperty().SetColor(0.5,1.0,0.0) # set the color you want
            
            self.ren.AddActor(self.sphere_actor)
    
    def streamline_representation(self):
        if self.rep_strategy == 0: 
            print("line representation selected")
            self.streamline_mapper.SetInputConnection(self.stream_tracer.GetOutputPort())
        
        elif self.rep_strategy == 1:
            print("tube representation selected")
            ''' Based on "Office Tube" example by Berk Geveci, Kitware, 2015
            https://gitlab.kitware.com/vtk/vtk/blob/cff62a106f99c9bac3d1bc4a4e449d28b7d94285/Examples/VisualizationAlgorithms/Python/officeTube.py '''
            tube_filter = vtk.vtkTubeFilter()
            tube_filter.SetInputConnection(self.stream_tracer.GetOutputPort())
            
            tube_filter.SetInputArrayToProcess(1, 0, 0, vtk.vtkDataObject.FIELD_ASSOCIATION_POINTS, "vectors")
            tube_filter.SetRadius(0.02)
            tube_filter.SetNumberOfSides(12)
            tube_filter.SetVaryRadiusToVaryRadiusByVector()
            
            self.streamline_mapper.SetInputConnection(tube_filter.GetOutputPort())
            
        elif self.rep_strategy == 2:
            print("ribbon representation selected")
        elif self.rep_strategy == 3:
            print("surface representation selected")
            
        # Re-render the screen
        self.vtkWidget.GetRenderWindow().Render()
    
    def on_streamline_checkbox_change(self):
        if hasattr(self, 'streamline_actor'):
            self.ren.RemoveActor(self.streamline_actor)
    
        if self.qt_streamline_checkbox.isChecked() == True:
            # Step 1: Create seeding points 
            if self.seeding_strategy == 1: 
                self.seedPolyData = self.random_generate_seeds() # You also can try generate_seeding_line()
            elif self.seeding_strategy == 0:
                self.seedPolyData = self.uniform_generate_seeds()
            elif self.seeding_strategy == 2:
                #You need a custom implementation for the interactive line widget
                #Again, if you cannot get the interactive part of this task then implement a static line seeding strategy that places seed point along a diagonal line (or horizontal/vertical line works too) across the data set
                #Example of this static implementation: 
                    #self.seedPolyData = self.generate_seeding_line()
                #note that you will receive point deductions for non-interactivity
                pass
                
            # Step 2: Render the seed point markers
            self.seed_point_representation()
            
            # Step 3: Create a vtkStreamTracer object, set input data and seeding points
            ''' Like hw3 '''
            self.stream_tracer = vtk.vtkStreamTracer()
            self.stream_tracer.SetInputData(self.reader.GetOutput()) # set vector field
            self.stream_tracer.SetSourceData(self.seedPolyData) # pass in the seeds
            

            # Step 4: Set the parameters for streamline tracing. 
            # Check the reference https://vtk.org/doc/nightly/html/classvtkStreamTracer.html
            # to have the full list of parameters
            self.stream_tracer.SetIntegratorTypeToRungeKutta45()
            self.stream_tracer.SetIntegrationDirectionToBoth()
            
            '''Make integration step 2x finer'''
            init_integrate_step = self.stream_tracer.GetInitialIntegrationStep()
            min_integrate_step = self.stream_tracer.GetMinimumIntegrationStep()
            max_integrate_step = self.stream_tracer.GetMaximumIntegrationStep()
            self.stream_tracer.SetInitialIntegrationStep(init_integrate_step / 2.0)
            self.stream_tracer.SetMinimumIntegrationStep(min_integrate_step / 2.0)
            self.stream_tracer.SetMaximumIntegrationStep(max_integrate_step / 2.0)
            
            # Step 5: Map the streamlines to polygon data
            self.streamline_mapper = vtk.vtkPolyDataMapper()
            self.streamline_mapper.ScalarVisibilityOff()
            
            self.streamline_representation()
            
            # Add the actor for streamlines to the scene
            self.streamline_actor = vtk.vtkActor()
            self.streamline_actor.SetMapper(self.streamline_mapper)
            self.streamline_actor.GetProperty().SetColor(0,0.7,1)
            self.ren.AddActor(self.streamline_actor)
           
        # Re-render the screen
        self.vtkWidget.GetRenderWindow().Render()       
        
if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())