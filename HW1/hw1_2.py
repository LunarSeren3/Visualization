# -*- coding: utf-8 -*-
"""
HW1: Problem 2. Display a VTK plot of a scalar field using a smooth color scale.

Sources: 
    [1] assignment sample code
    [2] common knowledge
    [3] own work

Created on Thu Sep 14 16:20:44 2023

@author: Seren
"""

import vtk

'''VTK interfacing'''
def getColorTable(color_resolution, color_scale_fn): # [1, 3]
    # Initialize color table
    colorTable = vtk.vtkLookupTable()
    colorTable.SetNumberOfTableValues(color_resolution)
    
    # Assign colors into table
    for i in range(0, color_resolution):
        # Get interpolated color
        scale_key = float(i) / color_resolution
        color = color_scale_fn(scale_key)
        
        # Append opacity information to the RGB color
        opaque_color = color + [1.0]
        
        # Load the color in the table
        colorTable.SetTableValue(i, *opaque_color)
        
    # Build table
    colorTable.Build()
    
    return colorTable

''' Color scale functions '''
import math

def linear_interpolate(key_range, val_range, key): # [2, 3]
    key_range_width = key_range[1] - key_range[0]
    key_relative_normal = (key - key_range[0]) / key_range_width
    
    val_range_width = val_range[1] - val_range[0]
    return val_range[0] + key_relative_normal * val_range_width

def linear_interpolate_color(key_range, start_color, end_color, key): # [3]
    return [linear_interpolate(key_range, val_range, key)
            for val_range in zip(start_color, end_color)]

# colors should be a tuple of at least 2 elements
def color_scale(colors, key): # [1]
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
crimson = (0.5, 0.0, 0.0)
cyan = (0.0, 1.0, 1.0)
deep_blue = (0.0, 0.0, 1.0)
metal_blue = (0.25, 0.25, 1.0)
metal_red = (1.0, 0.25, 0.25)
green = (0.0, 1.0, 0.0)
red = (1.0, 0.0, 0.0)
white = (1.0, 1.0, 1.0)
yellow = (1.0, 1.0, 0.0)

def rainbow_scale(key): # [2, 3]
    return color_scale([deep_blue, cyan, green, yellow, red], key)

def blue_white_red_scale(key): # [2, 3]
    return color_scale([metal_blue, white, metal_red], key)

def heat_scale(key): # [2, 3]
    return color_scale([black, red, yellow, white], key)

def gray_scale(key): # [2, 3]
    return color_scale([black, white], key)

