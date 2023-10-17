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
        
    def select_color_scheme(self,i):
        self.color_scheme = i
        MakeLUT(self.color_scheme, self.lut)
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
        self.lut = vtk.vtkLookupTable()
        MakeLUT(self.color_scheme, self.lut)
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
   
    '''         
        TODO: Complete the following function for generate uniform seeds 
        for streamline placement

    '''
    def uniform_generate_seeds(self):
        num_seeds = int(self.number_seeds.value())
        seedPoints = vtk.vtkPoints()

        # Generate the uniformly positioned seeds below!!

        # Need to put the seed points in a vtkPolyData object
        seedPolyData  = vtk.vtkPolyData()
        seedPolyData.SetPoints(seedPoints)
        return seedPolyData

    '''  
        TODO: Complete the following function for generate random seeds 
        for streamline placement
    '''
    def random_generate_seeds(self):
        numb_seeds = int (self.number_seeds.value())
        seedPoints = vtk.vtkPoints()       

        # Generate the random seeds below!!

        # Need to put the seed points in a vtkPolyData object
        seedPolyData  = vtk.vtkPolyData()
        seedPolyData.SetPoints(seedPoints)
        return seedPolyData

        
    ''' 
        TODO: Complete the following function to generate a set of streamlines
        from the above generated uniform or random seeds
    '''
    def on_streamline_checkbox_change(self):
        if self.qt_streamline_checkbox.isChecked() == True:
            # Step 1: Create seeding points 
            if self.seeding_strategy == 1: 
                seedPolyData = self.random_generate_seeds() # You also can try generate_seeding_line()
            elif self.seeding_strategy == 0:
                seedPolyData = self.uniform_generate_seeds()
            
            # Step 2: Create a vtkStreamTracer object, set input data and seeding points


            # Step 3: Set the parameters. 
            # Check the reference https://vtk.org/doc/nightly/html/classvtkStreamTracer.html
            # to have the full list of parameters



            # Step 4: Visualization
        
        
        # Turn on the following if you want to disable the streamline visualization
        # But again you need to modify the "streamline_actor" name based on what you use!!!
        # else:
            # self.ren.RemoveActor(self.streamline_actor)
        
           
        # Re-render the screen
        self.vtkWidget.GetRenderWindow().Render()       
                
 
    ''' This function generates a uniform grid for the input data, use it for your uniform streamline seeding
        You can also learn how to map seed point locations for the random seed strategy too! '''
    def generate_uniform_grid(self):
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
                gridPoints.InsertNextPoint ( x, y, 0)
        
 
    

    '''TODO: Complete this function to render LIC'''
    def generate_LIC(self):
        #(1) initialize the vtkImageDataLIC2D filter 
        
        #(2) Define the step size, number of steps, and other necessary LIC parameters to ensure a sharp and distinct LIC texture. 
        
        #(3) Construct a lookup table with a grayscale color scheme to prevent unintended color mappings to LIC values. 
        
        #(4) Set up a vtkDatasetMapper, connecting it to both the dataset and the lookup table. 
        
        #(5) Establish an actor for the mapper. Adjust its opacity in relation to the LIC opacity slider, allowing the underlying color map to be discernible, and then return the actor. 
        return None
    
    def on_LIC_checkbox(self):
        if hasattr(self, 'lic_actor') and self.lic_actor is not None:
            self.ren.RemoveActor(self.lic_actor)   
        
        if self.LIC_checkbox.isChecked() == True:
            self.lic_actor = self.generate_LIC()
            if self.lic_actor is not None:
                self.ren.AddActor(self.lic_actor)

        # Re-render the screen
        self.vtkWidget.GetRenderWindow().Render()
     

'''Add your own color scheme if you want'''
def MakeLUT(colorScheme, lut):
    # See: [Diverging Color Maps for Scientific Visualization]
    #      (http:#www.kennethmoreland.com/color-maps/)
    
    nc = 256 #interpolate 256 values, increase this to get more colors
    if colorScheme == 0:
        ctf = vtk.vtkColorTransferFunction()

        # Linear mapping from white to red
        ctf.AddRGBPoint(0.0, 1.0, 1.0, 1.0)
        ctf.AddRGBPoint(1.0, 1.0, 0.0, 0.0) 
        
        lut.SetNumberOfTableValues(nc)
        lut.Build()
        for i in range(0, nc):
            rgb = list(ctf.GetColor(float(i) / nc))
            rgb.append(1.0)  # appending alpha for RGBA
            lut.SetTableValue(i, *rgb)

    if colorScheme == 1: # white only
        
        rgb = [1.0, 1.0, 1.0]
        
        for i in range(0, nc):
            s = float(i) / nc
            lut.SetTableValue(i, rgb[0], rgb[1], rgb[2], 1.0)    
        
if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
