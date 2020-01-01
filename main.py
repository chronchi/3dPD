# plot_protein

from bokeh.layouts import row, column, widgetbox
from bokeh.models import CustomJS, ColumnDataSource
from bokeh.plotting import figure, curdoc, output_file, show
from bokeh.models.widgets import TextInput, Button, Dropdown, FileInput

import numpy as np

import os, sys
sys.path.insert(0, os.path.join(os.path.abspath('.')))

from surface3d import Surface3d
import load_data 

# create text input box to get the pdb path
file_input = FileInput(name="Upload csv file", accept=".csv") 

dropdown_dimension = Dropdown(label="Dimension", button_type="success", menu=[("1", "1"), ("2", "2")])

def callback_file(attr, old, new):
    coord_radius = load_data.load_convert_calculate(file_input)
    # get persistence diagram 
    persdiag, vertice_list = load_data.load_format_pd()
    # color for persistence diagram
    color_pd = [1]*np.shape(persdiag)[0]
    # pass data to p1
    s1.data = dict(x=persdiag[:,0], y=persdiag[:,1], color = color_pd)    
    # pass data to p2
    x = coord_radius[:,0]
    y = coord_radius[:,1]
    z = coord_radius[:,2]
    color = [1]*np.shape(x)[0]
    s2.data = dict(x=x, y=y, z=z, color = color)
    # vertices list for optimal cycles
    vert_list = []
    for vertices in vertice_list:
        # get 3d points from gen_protein_i2p.txt
        vert_list.append(load_data.where_is(vertices, coord_radius))
    s4.data = dict(vertices=vert_list)

def callback_file_dropdown(attr, old, new):
    dimension = dropdown_dimension.value
    print(dimension)
    coord_radius = load_data.load_convert_calculate(file_input, dimension=dimension)
    # get persistence diagram 
    persdiag, vertice_list = load_data.load_format_pd(dimension=dimension)
    # color for persistence diagram
    color_pd = [1]*np.shape(persdiag)[0]
    # pass data to p1
    s1.data = dict(x=persdiag[:,0], y=persdiag[:,1], color = color_pd)    
    # pass data to p2
    x = coord_radius[:,0]
    y = coord_radius[:,1]
    z = coord_radius[:,2]
    color = [1]*np.shape(x)[0]
    s2.data = dict(x=x, y=y, z=z, color = color)
    # vertices list for optimal cycles
    vert_list = []
    for vertices in vertice_list:
        # get 3d points from gen_protein_i2p.txt
        vert_list.append(load_data.where_is(vertices, coord_radius))
    s4.data = dict(vertices=vert_list) 

file_input.on_change('value', callback_file)
dropdown_dimension.on_change('value', callback_file_dropdown)

x = [] 
y = [] 
z = [] 
color = []

s1 = ColumnDataSource(data=dict(x=x, y=y, z=z, color=color))
p1 = figure(plot_width=500, plot_height=500, tools="reset, lasso_select, zoom_in, zoom_out", title="Select Here")
p1.circle('x', 'y', source=s1, alpha=0.6)

s2 = ColumnDataSource(data=dict(x=[0], y=[0], z=[0], color=[1]))
p2 = Surface3d(x="x", y="y", z="z", color="color", data_source=s2, width=500, height=500)

s4 = ColumnDataSource(data = {}) 

b = Button(label="Reset selection", button_type="success")
b.js_on_click(CustomJS(args=dict(p1=p1, s1=s1, s2=s2), code="""
    p1.reset.emit()
    var d2 = s2.data;
    for (var i = 0; i < d2['color'].length; i++) {
        d2['color'][i] = 1
    }
    s2.change.emit();
"""))

s1.selected.js_on_change('indices', CustomJS(args=dict(s1=s1, s2=s2, s4=s4), code="""
        var inds = cb_obj.indices;
        var d2 = s2.data;
        var d4 = s4.data;
        for (var i = 0; i < inds.length; i++) {
            var subidx = d4['vertices'][inds[i]]
            for (var j = 0; j < subidx.length; j++){
                d2['color'][subidx[j]] = 2
            }
        }    
        s2.change.emit();
    """)
)

controls=widgetbox([file_input, dropdown_dimension], sizing_mode="stretch_both")

layout = column(controls, b, row(p1, p2))

curdoc().add_root(layout)
