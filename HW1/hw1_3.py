"""
HW1: Problem 3. Display a VTK plot of a categorical field using an appropriate, discrete color scale.

Sources: 
    [1] assignment sample code
    [2] common knowledge
    [3] own work

Created on Mon Sep 18 2023

@author: Seren
"""

'''More_custom_colors as HSV''' # [3]
hsl_black_pink = (220,240,80)
hsl_black_sea_green = (100,240,80)
hsl_dark_red = (0,120,160)
hsl_dark_gold = (40,120,160)
hsl_dark_green = (80,120,160)
hsl_dark_cyan = (120,120,160)
hsl_dark_blue = (160,120,160)
hsl_dark_violet = (200,120,160)
hsl_deep_orange = (20,180,200)
hsl_deep_lime = (60,180,200)
hsl_deep_sea_green = (100,180,200)
hsl_deep_lapis_lazuli = (140,180,200)
hsl_deep_indigo = (180,180,200)
hsl_deep_pink = (220,180,200)
hsl_vivid_red = (0,240,240)
hsl_vivid_orange = (20,240,240)
hsl_vivid_gold = (40,240,240)
hsl_vivid_lime = (60,240,240)
hsl_vivid_green = (80,240,240)
hsl_vivid_sea_green = (100,240,240)
hsl_vivid_cyan = (120,240,240)
hsl_vivid_lapis_lazuli = (140,240,240)
hsl_vivid_blue = (160,240,240)
hsl_vivid_indigo = (180,240,240)
hsl_vivid_purple = (200,240,240)
hsl_vivid_pink = (220,240,240)
hsl_light_orange = (20,200,240)
hsl_light_lime = (60,200,240)
hsl_light_sea_green = (100,200,240)
hsl_light_lapis_lazuli = (140,200,240)
hsl_light_indigo = (180,200,240)
hsl_light_pink = (220,200,240)
hsl_pale_red = (0,160,240)
hsl_pale_gold = (40,160,240)
hsl_pale_green = (80,160,240)
hsl_pale_cyan = (120,160,240)
hsl_pale_blue = (160,160,240)
hsl_pale_violet = (200,160,240)
hsl_white_orange = (20,80,240)
hsl_white_lapis_lazuli = (140,80,240)

category_colors = (
    hsl_black_sea_green,
    hsl_dark_red,
    hsl_dark_gold,
    hsl_dark_green,
    hsl_dark_cyan,
    hsl_dark_blue,
    hsl_dark_violet,
    hsl_deep_orange,
    hsl_deep_lime,
    hsl_deep_sea_green,
    hsl_deep_lapis_lazuli,
    hsl_deep_indigo,
    hsl_deep_pink,
    hsl_vivid_red,
    hsl_vivid_orange,
    hsl_vivid_gold,
    hsl_vivid_lime,
    hsl_vivid_green,
    hsl_vivid_sea_green,
    hsl_vivid_cyan,
    hsl_vivid_lapis_lazuli,
    hsl_vivid_blue,
    hsl_vivid_indigo,
    hsl_vivid_purple,
    hsl_vivid_pink,
    hsl_light_orange,
    hsl_light_lime,
    hsl_light_sea_green,
    hsl_light_lapis_lazuli,
    hsl_light_indigo,
    hsl_light_pink,
    hsl_pale_red,
    hsl_pale_gold,
    hsl_pale_green,
    hsl_pale_cyan,
    hsl_pale_blue,
    hsl_pale_violet,
    hsl_white_orange,
    hsl_white_lapis_lazuli
)

from vtk import vtkMath

''' Get a list of RGB triads from the HSV color constants given here'''
def get_category_colors_as_RGB(): # [3]
    colors = []
    rgb = [0.0, 0.0, 0.0]
    vtkm = vtkMath()
    
    # Convert the HSV colors to RGB one by one, since the HSVToRGB function relies on mutable arguments
    for hsv_color in category_colors:
        standard_hsv_color = [(component / 240) for component in hsv_color]
        vtkm.HSVToRGB(standard_hsv_color, rgb)
        colors += [tuple(rgb)]
        
    return colors
    
from hw1_2 import color_scale

def category_scale(key): # [3]
    return color_scale(get_category_colors_as_RGB(), key)
