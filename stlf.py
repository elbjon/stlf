import streamlit as st
import folium
from streamlit_folium import st_folium, folium_static
st.write('Some Random Square Grids')
# Create a map using the Map() function and the coordinates for Boulder, CO
m = folium.Map(location=[52.8, 10.8], tiles="cartodb positron", zoom_start=5)

#add polygons
locations = [[[40, 32], [41, 32], [41, 33], [40, 33]], [[50, 58], [51, 58], [51, 59], [50, 59]], [[-3, 34], [-2, 34], [-2, 35], [-3, 35]], [[36, 34], [37, 34], [37, 35], [36, 35]], [[40, 67], [41, 67], [41, 68], [40, 68]], [[59, 63], [60, 63], [60, 64], [59, 64]], [[40, 63], [41, 63], [41, 64], [40, 64]], [[28, 31], [29, 31], [29, 32], [28, 32]], [[13, 36], [14, 36], [14, 37], [13, 37]], [[47, 55], [48, 55], [48, 56], [47, 56]], [[-2, 41], [-1, 41], [-1, 42], [-2, 42]], [[3, 37], [4, 37], [4, 38], [3, 38]], [[40, 43], [41, 43], [41, 44], [40, 44]], [[16, 48], [17, 48], [17, 49], [16, 49]], [[-8, 52], [-7, 52], [-7, 53], [-8, 53]], [[8, 58], [9, 58], [9, 59], [8, 59]], [[11, 62], [12, 62], [12, 63], [11, 63]], [[-4, 40], [-3, 40], [-3, 41], [-4, 41]], [[44, 57], [45, 57], [45, 58], [44, 58]], [[37, 63], [38, 63], [38, 64], [37, 64]], [[56, 44], [57, 44], [57, 45], [56, 45]], [[10, 41], [11, 41], [11, 42], [10, 42]], [[19, 60], [20, 60], [20, 61], [19, 61]], [[46, 39], [47, 39], [47, 40], [46, 40]], [[56, 37], [57, 37], [57, 38], [56, 38]], [[3, 49], [4, 49], [4, 50], [3, 50]], [[40, 51], [41, 51], [41, 52], [40, 52]], [[25, 64], [26, 64], [26, 65], [25, 65]], [[31, 30], [32, 30], [32, 31], [31, 31]], [[-2, 65], [-1, 65], [-1, 66], [-2, 66]], [[9, 62], [10, 62], [10, 63], [9, 63]], [[60, 29], [61, 29], [61, 30], [60, 30]], [[5, 41], [6, 41], [6, 42], [5, 42]], [[42, 50], [43, 50], [43, 51], [42, 51]], [[-4, 57], [-3, 57], [-3, 58], [-4, 58]], [[15, 57], [16, 57], [16, 58], [15, 58]], [[41, 51], [42, 51], [42, 52], [41, 52]], [[42, 46], [43, 46], [43, 47], [42, 47]], [[56, 58], [57, 58], [57, 59], [56, 59]], [[12, 39], [13, 39], [13, 40], [12, 40]], [[35, 64], [36, 64], [36, 65], [35, 65]], [[28, 62], [29, 62], [29, 63], [28, 63]], [[36, 56], [37, 56], [37, 57], [36, 57]], [[54, 51], [55, 51], [55, 52], [54, 52]], [[46, 60], [47, 60], [47, 61], [46, 61]], [[21, 67], [22, 67], [22, 68], [21, 68]], [[15, 37], [16, 37], [16, 38], [15, 38]], [[44, 43], [45, 43], [45, 44], [44, 44]], [[30, 43], [31, 43], [31, 44], [30, 44]], [[25, 51], [26, 51], [26, 52], [25, 52]], [[40, 36], [41, 36], [41, 37], [40, 37]], [[35, 32], [36, 32], [36, 33], [35, 33]], [[6, 28], [7, 28], [7, 29], [6, 29]], [[41, 39], [42, 39], [42, 40], [41, 40]], [[25, 58], [26, 58], [26, 59], [25, 59]], [[-9, 54], [-8, 54], [-8, 55], [-9, 55]], [[52, 62], [53, 62], [53, 63], [52, 63]], [[50, 35], [51, 35], [51, 36], [50, 36]], [[24, 37], [25, 37], [25, 38], [24, 38]], [[-1, 59], [0, 59], [0, 60], [-1, 60]], [[40, 49], [41, 49], [41, 50], [40, 50]], [[16, 38], [17, 38], [17, 39], [16, 39]], [[4, 31], [5, 31], [5, 32], [4, 32]], [[12, 30], [13, 30], [13, 31], [12, 31]], [[28, 63], [29, 63], [29, 64], [28, 64]], [[25, 29], [26, 29], [26, 30], [25, 30]], [[16, 52], [17, 52], [17, 53], [16, 53]], [[46, 28], [47, 28], [47, 29], [46, 29]], [[7, 44], [8, 44], [8, 45], [7, 45]], [[1, 29], [2, 29], [2, 30], [1, 30]], [[21, 38], [22, 38], [22, 39], [21, 39]], [[12, 56], [13, 56], [13, 57], [12, 57]], [[57, 49], [58, 49], [58, 50], [57, 50]], [[36, 52], [37, 52], [37, 53], [36, 53]], [[23, 33], [24, 33], [24, 34], [23, 34]], [[-7, 53], [-6, 53], [-6, 54], [-7, 54]], [[31, 46], [32, 46], [32, 47], [31, 47]], [[4, 37], [5, 37], [5, 38], [4, 38]], [[39, 34], [40, 34], [40, 35], [39, 35]], [[41, 56], [42, 56], [42, 57], [41, 57]], [[10, 27], [11, 27], [11, 28], [10, 28]], [[18, 30], [19, 30], [19, 31], [18, 31]], [[50, 38], [51, 38], [51, 39], [50, 39]], [[56, 31], [57, 31], [57, 32], [56, 32]], [[12, 56], [13, 56], [13, 57], [12, 57]], [[35, 49], [36, 49], [36, 50], [35, 50]], [[49, 29], [50, 29], [50, 30], [49, 30]], [[-5, 51], [-4, 51], [-4, 52], [-5, 52]], [[15, 46], [16, 46], [16, 47], [15, 47]], [[6, 61], [7, 61], [7, 62], [6, 62]], [[31, 41], [32, 41], [32, 42], [31, 42]], [[11, 39], [12, 39], [12, 40], [11, 40]], [[-1, 46], [0, 46], [0, 47], [-1, 47]], [[33, 46], [34, 46], [34, 47], [33, 47]], [[19, 34], [20, 34], [20, 35], [19, 35]], [[18, 53], [19, 53], [19, 54], [18, 54]], [[60, 63], [61, 63], [61, 64], [60, 64]], [[54, 31], [55, 31], [55, 32], [54, 32]], [[53, 28], [54, 28], [54, 29], [53, 29]], [[-4, 48], [-3, 48], [-3, 49], [-4, 49]]]

#For Polygon description etc look into the file from raspberry pi
folium.Polygon(
    locations=locations,
    color="blue",
    weight=1,
    fill_color="blue",
    fill_opacity=0.5,
    fill=True,
    popup="First Poly",
    tooltip="Click me!",
).add_to(m)

folium.Marker(
    [52.8, 10.8], popup="HELLO", tooltip="HELLOHELLO"
).add_to(m)

folium_static(m)
