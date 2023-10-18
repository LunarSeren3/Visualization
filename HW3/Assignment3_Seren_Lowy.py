#!/usr/bin/python

'''
    Skeleton code for a GUI application created by using PyQT and PyVTK
'''


import sys
import math
import random
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
        self.setWindowTitle("COSC 6344 Visualization HW3 - Seren Lowy")
        self.resize(1000,int(self.height()*1.2))
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
        style = vtk.vtkInteractorStyleImage()
        self.iren.SetInteractorStyle(style)
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
        groupBox = Qt.QGroupBox("2D Vector Field Visualization") # Use a group box to group controls
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
      
        
        ''' Add widgets for Color '''
        self.color_scheme = 0
        hbox_colplot = Qt.QHBoxLayout()
        self.color_checkbox = Qt.QCheckBox("Color On")
        self.color_checkbox.setChecked(False)
        self.color_checkbox.toggled.connect(self.on_color_checkbox)
        hbox_colplot.addWidget(self.color_checkbox)
        hbox_colplot.addWidget(Qt.QLabel("Select a color scheme:"))
        self.qt_color_scheme = Qt.QComboBox()
        self.qt_color_scheme.addItem("White Red")
        self.qt_color_scheme.addItem("Blank")
        self.qt_color_scheme.currentIndexChanged.connect(self.select_color_scheme)
        hbox_colplot.addWidget(self.qt_color_scheme)
        
        
        
        col_widget = Qt.QWidget()
        col_widget.setLayout(hbox_colplot)
        self.groupBox_layout.addWidget(col_widget)
        
        
        ''' Add the widgets for arrow plot '''
        sample_groupbox = Qt.QGroupBox("Arrow Options")
        vbox_arrow = Qt.QVBoxLayout()  # New QVBoxLayout for all arrow items
        
        # Arrow scale spinbox
        hbox_arrowplot = Qt.QHBoxLayout()
        # Arrow plot checkbox
        self.qt_arrow_checkbox = Qt.QCheckBox("Arrow Plot ")
        self.qt_arrow_checkbox.setChecked(False)
        self.qt_arrow_checkbox.toggled.connect(self.on_arrow_checkbox_change)
        hbox_arrowplot.addWidget(self.qt_arrow_checkbox)
        
        arrowscaleLabel = Qt.QLabel("Choose arrow scale:")
        hbox_arrowplot.addWidget(arrowscaleLabel)
        self.arrow_scale = Qt.QDoubleSpinBox()
        self.arrow_scale.setValue(0.03)
        self.arrow_scale.setRange(0, 1)
        self.arrow_scale.setSingleStep(0.01)
        hbox_arrowplot.addWidget(self.arrow_scale)
        vbox_arrow.addLayout(hbox_arrowplot)
        
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
        
        sample_groupbox.setLayout(vbox_arrow)
        self.groupBox_layout.addWidget(sample_groupbox)

        ''' Create a new QGroupBox for streamline options '''
        streamline_groupbox = Qt.QGroupBox("Streamline Options")
        vbox_streamline = Qt.QVBoxLayout()
        
        hbox_streamline = Qt.QHBoxLayout()
        self.qt_streamline_checkbox = Qt.QCheckBox("Streamline ")
        self.qt_streamline_checkbox.setChecked(False)
        self.qt_streamline_checkbox.toggled.connect(self.on_streamline_checkbox_change)
        hbox_streamline.addWidget(self.qt_streamline_checkbox) 
        seedLabel = Qt.QLabel("    Set number of seeds:")
        hbox_streamline.addWidget(seedLabel)
        self.number_seeds = Qt.QDoubleSpinBox()
        # set the initial values of some random parameters
        self.number_seeds.setValue(10)
        self.number_seeds.setRange(1, 2000)
        self.number_seeds.setSingleStep(1)
        hbox_streamline.addWidget(self.number_seeds)
        streamline_hwidget = Qt.QWidget()
        streamline_hwidget.setLayout(hbox_streamline)
        vbox_streamline.addWidget(streamline_hwidget)
        
        vbox_seed_strategy = Qt.QVBoxLayout()
        
        # Add radio buttons for the selection of the seed generation strategy
        self.uniform_seed_radio = Qt.QRadioButton("Uniform Seeding")
        self.uniform_seed_radio.setChecked(True)
        self.uniform_seed_radio.toggled.connect(self.on_seeding_strategy)
        vbox_seed_strategy.addWidget(self.uniform_seed_radio)
        
        self.random_seed_radio = Qt.QRadioButton("Random Seeding")
        self.random_seed_radio.setChecked(False)
        self.random_seed_radio.toggled.connect(self.on_seeding_strategy)
        vbox_seed_strategy.addWidget(self.random_seed_radio)
        self.seeding_strategy = 0 # Uniform seeding is the default strategy 
        
        seedingstrategy = Qt.QWidget()
        seedingstrategy.setLayout(vbox_seed_strategy)
        vbox_streamline.addWidget(seedingstrategy)
        
        streamline_groupbox.setLayout(vbox_streamline)
        self.groupBox_layout.addWidget(streamline_groupbox)
        

        ''' Add widgets for LIC '''
        hbox_LIC = Qt.QHBoxLayout()  # Horizontal layout for LIC options
        
        self.LIC_checkbox = Qt.QCheckBox("LIC On")
        self.LIC_checkbox.setChecked(False)
        self.LIC_checkbox.toggled.connect(self.on_LIC_checkbox)
        hbox_LIC.addWidget(self.LIC_checkbox)  # Add the checkbox to the horizontal layout
        
        # Create a QSlider for opacity
        self.LIC_opacity_slider = Qt.QSlider(Qt.Qt.Horizontal)
        self.LIC_opacity_slider.setRange(0, 100)
        self.LIC_opacity_slider.setValue(80)
        self.LIC_opacity_slider.setTickInterval(10)
        self.LIC_opacity_slider.setTickPosition(Qt.QSlider.TicksBelow)
        hbox_LIC.addWidget(self.LIC_opacity_slider)
        
        self.LIC_opacity_label = Qt.QLabel("Opacity: 80%")
        hbox_LIC.addWidget(self.LIC_opacity_label)
        
        LIC_widget = Qt.QWidget()
        LIC_widget.setLayout(hbox_LIC)
        self.groupBox_layout.addWidget(LIC_widget)
        
        # Connect the slider's valueChanged signal to update the label
        self.LIC_opacity_slider.valueChanged.connect(self.update_LIC_opacity_label)
        
    def find_color_scheme(self, i):
        if i == 0:
            return white_red_scale
        elif i == 1:
            return blank_scale
        elif i == 2:
            return gray_scale
        
    def select_color_scheme(self,i):
        self.color_scheme = i
        color_scale_fn = self.find_color_scheme(i)
        self.lut = makeColorTable(256, color_scale_fn)
        self.vtk_poly_mapper.SetLookupTable(self.lut)
        self.vtkWidget.GetRenderWindow().Render()

        # Define the slot to update the label
    def update_LIC_opacity_label(self, value):
        self.LIC_opacity_label.setText(f"Opacity: {value}%")

        
    def on_color_checkbox(self):
        if hasattr(self, 'color_actor'):
            self.ren.RemoveActor(self.color_actor)

        if self.color_checkbox.isChecked() == True:
            self.color_actor = self.map_color()
            self.ren.AddActor(self.color_actor)

        # Re-render the screen
        self.vtkWidget.GetRenderWindow().Render()
        
    
    def map_color(self):
        min_scalar,max_scalar = self.reader.GetOutput().GetPointData().GetArray('angle').GetRange()
        #print(min_scalar,max_scalar)
        vtk_poly_mapper = vtk.vtkPolyDataMapper()
        vtk_poly_mapper.SetInputConnection(self.reader.GetOutputPort())
        color_scale_fn = self.find_color_scheme(self.color_scheme)
        self.lut = makeColorTable(256, color_scale_fn)
        vtk_poly_mapper.SetScalarModeToUsePointData()
        vtk_poly_mapper.SetLookupTable(self.lut)
        vtk_poly_mapper.SetScalarRange(min_scalar, max_scalar)
        vtk_poly_mapper.SelectColorArray('angle');
        
        self.vtk_poly_mapper = vtk_poly_mapper
        
        poly = vtk.vtkActor()
        poly.SetMapper(vtk_poly_mapper)
        return poly


        
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

        '''' TODO (optional) You need to modify the following actors' names based on how you define them!!!!!'''
        if hasattr(self, 'arrow_actor'):
            self.ren.RemoveActor(self.arrow_actor)

        if hasattr(self, 'streamline_actor'):
            self.ren.RemoveActor(self.streamline_actor)

        if hasattr(self, 'lic_actor'):
            self.ren.RemoveActor(self.lic_actor)

        self.seeding_strategy = 0  # Uniform seeding is the default strategy

        self.bounds = self.reader.GetPolyDataOutput().GetBounds()
        length = (self.bounds[1] - self.bounds[0]) / 40.0

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
        
        
        '''Generate image data'''
        
        # Use the ResampleToImage filter
        resampler = vtk.vtkResampleToImage()
        resampler.SetInputConnection(self.reader.GetOutputPort())  
        resampler.SetSamplingDimensions(256, 256, 1)  # 50x50 for 2D data
        resampler.Update()
    
        self.imageData = resampler.GetOutput()
        
        
        self.ren.ResetCamera()
        self.vtkWidget.GetRenderWindow().Render()
        
    def on_arrow_checkbox_change(self, discard=False):
        if hasattr(self, "arrow_actor"):
            self.ren.RemoveActor(self.arrow_actor)
    
        if self.qt_arrow_checkbox.isChecked() == True:            
            # Make sure we use the velocity field
            self.reader.GetOutput().GetPointData().SetActiveVectors("velocity")

            ''' From assignment doc '''
            # Setup mask object
            densityFilter = vtk.vtkMaskPoints()
            densityFilter.SetInputData(self.reader.GetOutput())
            
            # Choose the type of glyphs as arrows
            glyphSource = vtk.vtkGlyphSource2D() 
            glyphSource.SetGlyphTypeToArrow()
            glyphSource.FilledOff()
            
            # Setup glyph object
            glyph2D = vtk.vtkGlyph2D()
            glyph2D.SetSourceConnection(glyphSource.GetOutputPort())
            glyph2D.OrientOn()
            glyph2D.SetScaleModeToScaleByVector()
            glyph2D.SetScaleFactor(self.arrow_scale.value()) # adjust the length of the arrows accordingly
            
            # Read sampling/masking option control
            selected_id = self.arrow_radio_group.checkedId()
            if selected_id == -2:
                print("All grid points is selected.")
                
                # Connect glyph object to reader without density filter if we are not down sampling
                glyph2D.SetInputData(self.reader.GetOutput())
                
            else:
                # Down sample the grid points.
                # TODO: this sometimes increases the number of points if the dataset is not dense?
                densityFilter.SetMaximumNumberOfPoints(500)
                
                # Connect glyph object to density filter if we are down sampling
                glyph2D.SetInputData(densityFilter.GetOutput())
            
                # Select the down sampling type
                if selected_id == -3:
                    print("Uniform Sample is selected.")
                    
                    # This feature is not needed here.
                    
                elif selected_id == -4:
                    print("Random Sample is selected.")
                    densityFilter.RandomModeOn() # enable the random sampling mechanism
                    densityFilter.SetRandomModeType(3) #specify the sampling mode
            
            # Update density filter and glyph object after receiving input data
            densityFilter.Update()
            glyph2D.Update()            

            # Mapper and actor
            arrows_mapper = vtk.vtkPolyDataMapper()
            arrows_mapper.SetInputConnection(glyph2D.GetOutputPort())
            arrows_mapper.ScalarVisibilityOff()
            arrows_mapper.Update()

            self.arrow_actor = vtk.vtkActor()
            self.arrow_actor.SetMapper(arrows_mapper)
            self.arrow_actor.GetProperty().SetColor(0,0,1) # set the color you want
            
            self.ren.AddActor(self.arrow_actor)
            
        # Re-render the screen
        self.vtkWidget.GetRenderWindow().Render()
        
    '''event handle for the radio buttons of seeding strategies
    '''
    def on_seeding_strategy(self):
        if self.uniform_seed_radio.isChecked() == True:
            self.random_seed_radio.setChecked(False)
            self.seeding_strategy = 0
        elif self.random_seed_radio.isChecked() ==  True:
            self.uniform_seed_radio.setChecked(False)
            self.seeding_strategy = 1
            
        # Update the streamline plot now
        if hasattr(self, 'streamline_actor'):
                self.ren.RemoveActor(self.streamline_actor)
                
                self.on_streamline_checkbox_change()
   
    def map_positions_to_data_domain(self, normal_positions):
        xmin, xmax, ymin, ymax, _, _ = self.reader.GetPolyDataOutput().GetBounds()
        width = xmax - xmin
        height = ymax - ymin
        
        positions = [(xmin + np[0] * width, 
                      ymin + np[1] * height) 
                        for np in normal_positions]
                        
        return positions
    
    import math
    
    def uniform_generate_seeds(self):
        num_seeds = int(self.number_seeds.value())
        seedPoints = vtk.vtkPoints()

        # Define parameters for a uniform grid
        linear_dimension = int(math.sqrt(num_seeds))
        linear_dim_fraction = 1.0 / (linear_dimension + 1)
        
        # Generate uniform positions in normal space
        normal_positions = []
        for i in range(linear_dimension):
            for j in range(linear_dimension):
                x = (i + 1) * linear_dim_fraction
                y = (j + 1) * linear_dim_fraction
                
                normal_positions += [(x, y)]
        
        # Map the normal space to the data domain
        positions = self.map_positions_to_data_domain(normal_positions)
                        
        # Create seed points with the computed positions in data space
        for pos in positions:
            seedPoints.InsertNextPoint(pos[0], pos[1], 0)

        # Put the seed points in a vtkPolyData object
        seedPolyData  = vtk.vtkPolyData()
        seedPolyData.SetPoints(seedPoints)
        return seedPolyData

    def random_roll(self):
        random_resolution = 32768.0
        return random.randint(0, int(random_resolution)) / random_resolution
    
    def random_generate_seeds(self):
        num_seeds = int (self.number_seeds.value())
        seedPoints = vtk.vtkPoints()       

        # Generate the random positions in normal space
        normal_positions = []
        for _ in range(num_seeds):
            x = self.random_roll()
            y = self.random_roll()
            
            normal_positions += [(x, y)]
        
        # Map the normal space to the data domain
        positions = self.map_positions_to_data_domain(normal_positions)
        
        # Create seed points with the computed positions in data space
        for pos in positions:
            seedPoints.InsertNextPoint(pos[0], pos[1], 0)

        # Put the seed points in a vtkPolyData object
        seedPolyData  = vtk.vtkPolyData()
        seedPolyData.SetPoints(seedPoints)
        return seedPolyData

    def on_streamline_checkbox_change(self):
        if self.qt_streamline_checkbox.isChecked() == True:
            # Step 1: Create seeding points 
            if self.seeding_strategy == 1: 
                seedPolyData = self.random_generate_seeds() # You also can try generate_seeding_line()
            elif self.seeding_strategy == 0:
                seedPolyData = self.uniform_generate_seeds()
            
            # Step 2: Create a vtkStreamTracer object, set input data and seeding points
            '''From assignment doc'''
            stream_tracer = vtk.vtkStreamTracer()
            stream_tracer.SetInputData(self.reader.GetPolyDataOutput()) # set vector field
            stream_tracer.SetSourceData(seedPolyData) # pass in the seeds


            # Step 3: Set the parameters. 
            # Check the reference https://vtk.org/doc/nightly/html/classvtkStreamTracer.html
            # to have the full list of parameters
            '''From assignment doc'''
            stream_tracer.SetIntegratorTypeToRungeKutta45()
            stream_tracer.SetIntegrationDirectionToBoth()
            
            '''Make integration step 2x finer'''
            init_integrate_step = stream_tracer.GetInitialIntegrationStep()
            min_integrate_step = stream_tracer.GetMinimumIntegrationStep()
            max_integrate_step = stream_tracer.GetMaximumIntegrationStep()
            stream_tracer.SetInitialIntegrationStep(init_integrate_step / 2.0)
            stream_tracer.SetMinimumIntegrationStep(min_integrate_step / 2.0)
            stream_tracer.SetMaximumIntegrationStep(max_integrate_step / 2.0)

            # Step 4: Visualization
            streamline_mapper = vtk.vtkPolyDataMapper()
            streamline_mapper.SetInputConnection(stream_tracer.GetOutputPort())
            streamline_mapper.ScalarVisibilityOff()
            self.streamline_actor = vtk.vtkActor()
            self.streamline_actor.SetMapper(streamline_mapper)
            self.streamline_actor.GetProperty().SetColor(0,0,1)
            self.ren.AddActor(self.streamline_actor)
        
        
        # Turn on the following if you want to disable the streamline visualization
        # But again you need to modify the "streamline_actor" name based on what you use!!!
        else:
            if hasattr(self, 'streamline_actor'):
                self.ren.RemoveActor(self.streamline_actor)
        
           
        # Re-render the screen
        self.vtkWidget.GetRenderWindow().Render()       
                
 
    ''' This function generates a uniform grid for the input data, use it for your uniform streamline seeding
        You can also learn how to map seed point locations for the random seed strategy too! '''
    '''def generate_uniform_grid(self):
        self.vectorFieldPolyData = self.reader.GetPolyDataOutput()
        self.bounds = self.vectorFieldPolyData.GetBounds()
        
        #Create a uniform grid of points to interpolate over
        gridPoints = vtk.vtkPoints()
        
        self.space_x = (self.bounds[1]-self.bounds[0])/(self.IMG_RES-1)
        self.space_y = (self.bounds[3]-self.bounds[2])/(self.IMG_RES-1)
        self.space_z = 0
        for i in range( 0, self.IMG_RES):   
            for j in range( 0, self.IMG_RES):           
                x = self.bounds[0] + i * self.space_x
                y = self.bounds[2] + j * self.space_y
                gridPoints.InsertNextPoint ( x, y, 0)'''
    

    '''TODO: Complete this function to render LIC'''
    def generate_LIC(self):
        #(1) initialize the vtkImageDataLIC2D filter 
        lic_filter = vtk.vtkImageDataLIC2D()
        lic_filter.SetInputData(self.imageData)
        
        #(2) Define the step size, number of steps, and other necessary LIC parameters to ensure a sharp and distinct LIC texture. 
        '''Step size is already relative to the cell width defined in the dataset!
           The default value of 1.0 makes the steps match the cells in the specific dataset.'''
        lic_filter.SetStepSize(0.5) # Default value is 1.0
        lic_filter.SetSteps(30)     # Default value is 20
        lic_filter.SetContext(self.vtkWidget.GetRenderWindow())
        lic_filter.Update()
        
        #(3) Construct a lookup table with a grayscale color scheme to prevent unintended color mappings to LIC values. 
        color_table = makeColorTable(256, gray_scale) # See functions defined below (like hw1)
        
        #(4) Set up a vtkDatasetMapper, connecting it to both the dataset and the lookup table.
        lic_mapper = vtk.vtkDataSetMapper()
        lic_mapper.SetInputData(lic_filter.GetOutput())
        lic_mapper.SetLookupTable(color_table)
        lic_mapper.Update()
        
        #(5) Establish an actor for the mapper. Adjust its opacity in relation to the LIC opacity slider, allowing the underlying color map to be discernible, and then return the actor.
        lic_actor = vtk.vtkActor()
        lic_actor.SetMapper(lic_mapper)
        opacity = self.LIC_opacity_slider.value() / 100.0
        lic_actor.GetProperty().SetOpacity(opacity)
        return lic_actor
    
    def on_LIC_checkbox(self):
        if hasattr(self, 'lic_actor'):
            self.ren.RemoveActor(self.lic_actor)   
        
        if self.LIC_checkbox.isChecked() == True:
            self.lic_actor = self.generate_LIC()
            self.ren.AddActor(self.lic_actor)

        # Re-render the screen
        self.vtkWidget.GetRenderWindow().Render()
     

'''Color table builder using easy custom color scales'''
def makeColorTable(color_resolution, color_scale_fn): # [1, 3]
    # Initialize color table
    color_table = vtk.vtkLookupTable()
    color_table.SetNumberOfTableValues(color_resolution)
    
    # Assign colors into table
    for i in range(0, color_resolution):
        # Get interpolated color
        scale_key = float(i) / color_resolution
        color = color_scale_fn(scale_key)
        
        # Append opacity information to the RGB color
        opaque_color = color + [1.0]
        
        # Load the color in the table
        color_table.SetTableValue(i, *opaque_color)
        
    # Build table
    color_table.Build()
    
    return color_table

''' Color scale functions '''
import math

def linear_interpolate(key_range, val_range, key):
    key_range_width = key_range[1] - key_range[0]
    key_relative_normal = (key - key_range[0]) / key_range_width
    
    val_range_width = val_range[1] - val_range[0]
    return val_range[0] + key_relative_normal * val_range_width

def linear_interpolate_color(key_range, start_color, end_color, key):
    return [linear_interpolate(key_range, val_range, key)
            for val_range in zip(start_color, end_color)]

# colors should be a tuple of at least 2 elements
def color_scale(colors, key):
    # Locate which subrange the key is located in (for a scale with > 2 colors)
    #  Assumes that subranges are equal width.
    num_subranges = len(colors) - 1
    subrange_index = math.floor(key * num_subranges) 
            
    # Select the interpolation colors based on the subrange location
    start_color = colors[subrange_index]
    end_color = colors[subrange_index + 1]
    
    # Extract the subrange boundaries based on the subrange location and default boundaries
    subrange_width = 1.0 / num_subranges
    key_range = [subrange_index * subrange_width, 
                 (subrange_index + 1) * subrange_width]
    
    # Interpolate the color
    color = linear_interpolate_color(key_range, start_color, end_color, key)
    return color

'''Custom color scales'''
black = (0.0, 0.0, 0.0)
red = (1.0, 0.0, 0.0)
white = (1.0, 1.0, 1.0)

def white_red_scale(key):
    return color_scale([white, red], key)

def gray_scale(key):
    return color_scale([black, white], key)    

def blank_scale(key):
    return color_scale([white, white], key)
        
if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
