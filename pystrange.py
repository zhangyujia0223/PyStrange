"""
Program:     PyStrange
Description: search for random strange attractors
             and plot them with matplotlib
Author:      Anton Neururer - jupiter-online.net
External libraries:
             numpy, matplotlib
License:

PyStrange is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License version 2 as published by
the Free Software Foundation.

PyStrange is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

# import modules
import numpy as np
import matplotlib.pyplot as plt
import random
import sys
import argparse
import re
from mpl_toolkits.mplot3d import Axes3D
import plotly
import plotly.graph_objs as go
from scipy.interpolate import InterpolatedUnivariateSpline

# use syle seaborn
plt.style.use('seaborn')

description=\
'''
Use PyStrange to plot 2D or 3D attractors in Random Search
Mode or Single Search Mode. You can choose between two quadratic
and two cubic maps/flows and one quartic map/flow ("2d_12", "3d_30", "2d_20", "3d_60", "3d_105").
It is recommended to use large values for option "-n", especially
if maps with 30 or 60 coefficients are used.
To use Single Search Mode you can use a specific parameter set (option "-s") in the form
of a character string (12, 20, 30 or 60 capital letters).
Parameters for the coefficients of the quadratic and cubic functions
range from -1.2 (letter A) to + 1.3 (Letter Z).
If option "-s" is passed, option "-n" will be ignored.
Attractors can be exported in three different formats (option "-o"):
"png" (via matplotlib), "html" (via plotly) or "obj" (wavefront).
3D Plots via plotly will produce interactive Javascript visualizations.
The wavefront format can be used to import points clouds to Blender.
You can specify multiple output formats, for example "-o png html".
Set the number of points to calculated with option "-p".
You can specify to plot only every n'th point with option "-j".
You can start plotting at a certain index with option "-f".
You can define a time intervall with option "-t" (only available for 3D output)
'''

epilog=\
'''
I am strangely attracted to strangely attractive strange attractors.
'''

# map letters to coefficients
coeff = {'A': -1.2, 'B': -1.1, 'C': -1.0,
         'D': -0.9, 'E': -0.8, 'F': -0.7,
         'G': -0.6, 'H': -0.5, 'I': -0.4,
         'J': -0.3, 'K': -0.2, 'L': -0.1,
         'M':  0.0, 'N':  0.1, 'O':  0.2,
         'P':  0.3, 'Q':  0.4, 'R':  0.5,
         'S':  0.6, 'T':  0.7, 'U':  0.8,
         'V':  0.9, 'W':  1.0, 'X':  1.1,
         'Y':  1.2, 'Z':  1.3}


# calculate coordinates of a quadratic map with 12 coefficients (2 dimensions)
def map_2d_12(x, y, c):

    x_next = c[0] + c[1] * x + c[2] * x * x + c[3] * x * y + c[4] * y + c[5] * y * y
    y_next = c[6] + c[7] * x + c[8] * x * x + c[9] * x * y + c[10] * y + c[11] * y * y

    return x_next, y_next


# calculate coordinates of a cubic map with 20 coefficients (2 dimensions)
def map_2d_20(x, y, c):

    x_next = c[0] + c[1]*x + c[2]*x*x + c[3]*x*x*x + c[4]*x*x*y \
             + c[5]*x*y + c[6]*x*y*y + c[7]*y + c[8]*y*y + c[9]*y*y*y
    y_next = c[10] + c[11]*x + c[12]*x*x + c[13]*x*x*x + c[14]*x*x*y \
             + c[15]*x*y + c[16]*x*y*y + c[17]*y + c[18]*y*y + c[19]*y*y*y

    return x_next, y_next


# calculate coordinates of a quadratic map/flow with 30 coefficients (3 dimensions)
def map_3d_30(x, y, z, c):

    x_next = c[0] + c[1]*x + c[2]*x*x + c[3]*x*y + c[4]*x*z \
             + c[5]*y + c[6]*y*y + c[7]*y*z + c[8]*z + c[9]*z*z
    y_next = c[10] + c[11]*x + c[12]*x*x + c[13]*x*y + c[14]*x*z \
             + c[15]*y + c[16]*y*y + c[17]*y*z + c[18]*z + c[19]*z*z
    z_next = c[20] + c[21]*x + c[22]*x*x + c[23]*x*y + c[24]*x*z \
             + c[25]*y + c[26]*y*y + c[27]*y*z + c[28]*z + c[29]*z*z

    return x_next, y_next, z_next


# calculate coordinates of a cubic map/flow with 60 coefficients (3 dimensions)
def map_3d_60(x, y, z, c):

    x_next = c[0] + c[1]*x + c[2]*x*x + c[3]*x*x*x + c[4]*x*x*y \
             + c[5]*x*x*z + c[6]*x*y + c[7]*x*y*y + c[8]*x*y*z + c[9]*x*z \
             + c[10]*x*z*z + c[11]*y + c[12]*y*y + c[13]*y*y*y + c[14]*y*y*z \
             + c[15]*y*z + c[16]*y*z*z + c[17]*z + c[18]*z*z + c[19]*z*z*z
    y_next = c[20] + c[21]*x + c[22]*x*x + c[23]*x*x*x + c[24]*x*x*y \
             + c[25]*x*x*z + c[26]*x*y + c[27]*x*y*y + c[28]*x*y*z + c[29]*x*z \
             + c[30]*x*z*z + c[31]*y + c[32]*y*y + c[33]*y*y*y + c[34]*y*y*z \
             + c[35]*y*z + c[36]*y*z*z + c[37]*z + c[38]*z*z + c[39]*z*z*z
    z_next = c[40] + c[41]*x + c[42]*x*x + c[43]*x*x*x + c[44]*x*x*y \
             + c[45]*x*x*z + c[46]*x*y + c[47]*x*y*y + c[48]*x*y*z + c[49]*x*z \
             + c[50]*x*z*z + c[51]*y + c[52]*y*y + c[53]*y*y*y + c[54]*y*y*z \
             + c[55]*y*z + c[56]*y*z*z + c[57]*z + c[58]*z*z + c[59]*z*z*z

    return x_next, y_next, z_next


# calculate coordinates of a quartic map/flow with 105 coefficients (3 dimensions)
def map_3d_105(x, y, z, c):

    x_next = c[0] + c[1]*x + c[2]*x*x +c[3]*x*x*x + c[4]*x*x*x*x + c[5]*x*x*x*y \
             + c[6]*x*x*x*z + c[7]*x*x*y + c[8]*x*x*y*y  + c[9]*x*x*y*z + c[10]*x*x*z \
             + c[11]*x*x*z*z + c[12]*x*y + c[13]*x*y*y + c[14]*x*y*y*y + c[15]*x*y*y*z \
             + c[16]*x*y*z + c[17]*x*y*z*z + c[18]*x*z + c[19]*x*z*z + c[20]*x*z*z*z \
             + c[21]*y + c[22]*y*y + c[23]*y*y*y + c[24]*y*y*y*y + c[25]*y*y*y*z \
             + c[26]*y*y*z + c[27]*y*y*z*z + c[28]*y*z + c[29]*y*z*z + c[30]*y*z*z*z \
             + c[31]*z + c[32]*z*z + c[33]*z*z*z + c[34]*z*z*z*z
    y_next = c[35] + c[36]*x + c[37]*x*x +c[38]*x*x*x + c[39]*x*x*x*x + c[40]*x*x*x*y \
             + c[41]*x*x*x*z + c[42]*x*x*y + c[43]*x*x*y*y  + c[44]*x*x*y*z + c[45]*x*x*z \
             + c[46]*x*x*z*z + c[47]*x*y + c[48]*x*y*y + c[49]*x*y*y*y + c[50]*x*y*y*z \
             + c[51]*x*y*z + c[52]*x*y*z*z + c[53]*x*z + c[54]*x*z*z + c[55]*x*z*z*z \
             + c[56]*y + c[57]*y*y + c[58]*y*y*y + c[59]*y*y*y*y + c[60]*y*y*y*z \
             + c[61]*y*y*z + c[62]*y*y*z*z + c[63]*y*z + c[64]*y*z*z + c[65]*y*z*z*z \
             + c[66]*z + c[67]*z*z + c[68]*z*z*z + c[69]*z*z*z*z
    z_next = c[70] + c[71]*x + c[72]*x*x +c[73]*x*x*x + c[74]*x*x*x*x + c[75]*x*x*x*y \
             + c[76]*x*x*x*z + c[77]*x*x*y + c[78]*x*x*y*y  + c[79]*x*x*y*z + c[80]*x*x*z \
             + c[81]*x*x*z*z + c[82]*x*y + c[83]*x*y*y + c[84]*x*y*y*y + c[85]*x*y*y*z \
             + c[86]*x*y*z + c[87]*x*y*z*z + c[88]*x*z + c[89]*x*z*z + c[90]*x*z*z*z \
             + c[91]*y + c[92]*y*y + c[93]*y*y*y + c[94]*y*y*y*y + c[95]*y*y*y*z \
             + c[96]*y*y*z + c[97]*y*y*z*z + c[98]*y*z + c[99]*y*z*z + c[100]*y*z*z*z \
             + c[101]*z + c[102]*z*z + c[103]*z*z*z + c[104]*z*z*z*z

    return x_next, y_next, z_next


# get all coefficients for parameter string
def get_coefficient(parameter_string, coefficients):
    return [coefficients[value] for value in parameter_string]


# create a random string with n capital letters
def get_random_string(coefficients, n):
    return ''.join(random.choice(list(coefficients.keys())) for i in range(n))


# plot point cloud according to output_mode (png, html, obj)
def plot_point_cloud(px, py, pz, dim, output_mode, parameter_string, subtitle_string):

    # output mode matplotlib
    if output_mode == 'png':

        if dim == '2d':
            plt.scatter(px, py, c='#4c72b0', marker='.', s=0.1)
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title('2D Attractor {}\n{}'.format(parameter_string, subtitle_string))
            plt.savefig('2D Attractor {} {} Vertices.png'.format(parameter_string, len(px)))

        elif dim == '3d':
            fig = plt.figure()
            ax = fig.gca(projection='3d')
            ax.scatter(px, py, pz, s=0.1)
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_zlabel('z')
            ax.set_title('3D Attractor {}\n{}'.format(parameter_string, subtitle_string))
            plt.savefig('3D Attractor {} {} Vertices.png'.format(parameter_string, len(px)))
            
        plt.close('all')    
        print('attractor {} saved to .png file ({} vertices)'.format(parameter_string, len(px)))

    # output mode plotly
    elif output_mode =='html':

        if dim == '2d':

            trace = go.Scatter(x=px, y=py, mode='markers', marker=dict(size=1, colorscale='Viridis', opacity=1.0))
            layout = go.Layout(margin=dict(l=0, r=0, b=0, t=0))
            fig = go.Figure(data=[trace], layout=layout)
            plotly.offline.plot(fig, auto_open=False, filename='2D Attractor {} {} Vertices.html'.format(parameter_string, len(px)))

        elif dim=='3d':

            trace = go.Scatter3d(x=px, y=py, z=pz, marker=dict(size=1, colorscale='Viridis', opacity=1.0), line=dict(color='#1f77b4', width=1))
            layout = go.Layout(margin=dict(l=0, r=0, b=0, t=0))
            fig = go.Figure(data=[trace], layout=layout)
            plotly.offline.plot(fig, auto_open=False, filename='3D Attractor {} {} Vertices.html'.format(parameter_string, len(px)))

        print('attractor {} saved to .html file ({} vertices)'.format(parameter_string, len(px)))
        
    # output mode wavefront
    elif output_mode == 'obj':

        if dim == '2d':
            
            with open("{}.obj".format(parameter_string), "w") as outfile:
                outfile.write("o attractor\n")
                for i in range(len(px)):
                    outfile.write("v {} {} {}\n".format(px[i], py[i], 0))
                    
        elif dim=='3d':
            
            with open("{}.obj".format(parameter_string), "w") as outfile:
                outfile.write("o attractor\n")
                for i in range(len(px)):
                    outfile.write("v {} {} {}\n".format(px[i]*10, py[i]*10, pz[i]*10))
                
        print('attractor {} saved to .obj file ({} vertices)'.format(parameter_string, len(px)))


# check for fixed points and oscillation
def check_histogram(dim, x, y, z, parameter_string, threshold=50):

    if dim == 3:

        lastx = np.round(x, 3)
        lasty = np.round(y, 3)
        lastz = np.round(z, 3)
        histx, binx = np.histogram(lastx, len(lastx))
        histy, biny = np.histogram(lasty, len(lasty))
        histz, binz = np.histogram(lastz, len(lastz))
        diff_valx = np.greater(histx, 0).astype(int).sum()
        diff_valy = np.greater(histy, 0).astype(int).sum()
        diff_valz = np.greater(histz, 0).astype(int).sum()

        if diff_valx < threshold and diff_valy < threshold and diff_valz < threshold:
            print('attractor {} low diversity of last {} points: x[{}] y[{}] z[{}]'\
                .format(parameter_string, len(x), diff_valx, diff_valy, diff_valz))

            return False

    elif dim == 2:

        lastx = np.round(x, 3)
        lasty = np.round(y, 3)
        histx, binx = np.histogram(lastx, len(lastx))
        histy, biny = np.histogram(lasty, len(lasty))
        diff_valx = np.greater(histx, 0).astype(int).sum()
        diff_valy = np.greater(histy, 0).astype(int).sum()

        if diff_valx < threshold and diff_valy < threshold:
            print('attractor {} low diversity of last {} points: x[{}] y[{}]'\
                .format(parameter_string, len(x), diff_valx, diff_valy))
                
            return False

    return True


# search and plot 2d attractor
def get_attractor_2d_map(parameter_string, num_points, subtitle_string, output_modes, sieve, plot_offset, map_function):

    x = np.empty(num_points + plot_offset)
    y = np.empty(num_points + plot_offset)

    c = get_coefficient(parameter_string, coeff)

    # initialize start values
    x[0], y[0] = 0.1, 0.1

    # calculate all x and y coordinates
    for i in range(num_points + plot_offset - 1):

        x_cur, y_cur = x[i], y[i]
        x_new, y_new = map_function(x_cur, y_cur, c)

        x[i + 1], y[i + 1] = x_new, y_new

        # values out of bounds -> abort
        if abs(x_new) > 10 or abs(y_new) > 10:
            print('attractor', parameter_string, 'out of bounds at iteration', i, '-', x_new, y_new)
            return False

        # check histogram of points at index 100 to 199
        if i == 300:
            if check_histogram(2, x[i-100:i], y[i-100:i], 0, parameter_string) == False:
                return False

    # plot 2d attractor            
    for output_mode in output_modes:
        plot_point_cloud(x[plot_offset::sieve],
                        y[plot_offset::sieve],
                        0,
                        '2d',
                        output_mode,
                        parameter_string,
                        subtitle_string)

    # return success
    return True


# search and plot 3d attractor flow mode
def get_attractor_3d_flow(parameter_string, time, num_points, subtitle_string, output_modes, sieve, plot_offset, map_function, interpolate):

    x = np.empty(num_points + plot_offset)
    y = np.empty(num_points + plot_offset)
    z = np.empty(num_points + plot_offset)

    c = get_coefficient(parameter_string, coeff)

    # initialize start values
    x[0], y[0], z[0] = 0.1, 0.1, 0.1

    # calculate all x and y coordinates
    for i in range(num_points + plot_offset - 1):

        x_cur, y_cur, z_cur = x[i], y[i], z[i]
        x_new, y_new, z_new = map_function(x_cur, y_cur, z_cur, c)
        x_new = x_cur + time*x_new
        y_new = y_cur + time*y_new
        z_new = z_cur + time*z_new

        x[i + 1], y[i + 1], z[i + 1] = x_new, y_new, z_new

        # values out of bounds -> abort
        if abs(x_new) > 10 or abs(y_new) > 10 or abs(z_new) > 10:
            print('attractor', parameter_string, 'out of bounds at iteration', i, '-', x_new, y_new, z_new)
            return False

        # check histogram of points at index 100 to 199
        if i == 300:
            if check_histogram(3, x[i-100:i], y[i-100:i], z[i-100:i], parameter_string) == False:
                return False

    t = np.arange(num_points + plot_offset)
    
    # now let's refine it to 100 points:
    t2 = np.linspace(t.min(), t.max(), num_points*interpolate + plot_offset)  

    x2 = InterpolatedUnivariateSpline(t, x)(t2)
    y2 = InterpolatedUnivariateSpline(t, y)(t2)
    z2 = InterpolatedUnivariateSpline(t, z)(t2)
    
    # plot 3d attractor
    for output_mode in output_modes:
        plot_point_cloud(x2[plot_offset::sieve],
                        y2[plot_offset::sieve],
                        z2[plot_offset::sieve],
                        '3d',
                        output_mode,
                        parameter_string,
                        subtitle_string)

    # return success
    return True


# search and plot 3d attractor map mode
def get_attractor_3d_map(parameter_string, num_points, subtitle_string, output_modes, sieve, plot_offset, map_function):

    x = np.empty(num_points + plot_offset)
    y = np.empty(num_points + plot_offset)
    z = np.empty(num_points + plot_offset)

    c = get_coefficient(parameter_string, coeff)

    # initialize start values
    x[0], y[0], z[0] = 0.1, 0.1, 0.1

    # calculate all x and y coordinates
    for i in range(num_points + plot_offset - 1):

        x_cur, y_cur, z_cur = x[i], y[i], z[i]
        x_new, y_new, z_new = map_function(x_cur, y_cur, z_cur, c)

        x[i + 1], y[i + 1], z[i + 1] = x_new, y_new, z_new

        # values out of bounds -> abort
        if abs(x_new) > 10 or abs(y_new) > 10 or abs(z_new) > 10:
            print('attractor', parameter_string, 'out of bounds at iteration', i, '-', x_new, y_new, z_new)
            return False

        # check histogram of points at index 100 to 199
        if i == 300:
            if check_histogram(3, x[i-100:i], y[i-100:i], z[i-100:i], parameter_string) == False:
                return False

    # plot 3d attractor
    for output_mode in output_modes:
        plot_point_cloud(x[plot_offset::sieve],
                        y[plot_offset::sieve],
                        z[plot_offset::sieve],
                        '3d',
                        output_mode,
                        parameter_string,
                        subtitle_string)

    # return success
    return True


# check user input: number of guesses
def check_num_guesses(number):
    if number < 1:
        sys.exit('error: number of guesses must be at least 1')


# check user input: number of points for plotting
def check_num_points(points):
    if points < 1:
        sys.exit('error: number of points must be at least 1')


# check user input: output file format
def check_output_mode(output):
    if re.match(r'(png|html|obj)', output) is None:
        sys.exit('error: output mode "{}" invalid, expect "png" and/or "html" and/or "obj"'.format(output))


# check user input: 2d/3d maps
def check_map_mode(m):
    if re.match(r'((3d_30)|(3d_60)|(3d_105)|(2d_12)|(2d_20))', m) is None:
        sys.exit('error: map mode must be "3d_30" or "2d_12" or "2d_20"')  


# check user input: parameter string   
def check_parameter_string(string):
    if re.match(r'(([A-Z]{12})|([A-Z]{20})|([A-Z]{30})|([A-Z]{60}))', string) is None:
        sys.exit('Error: parameter string must be 12 or 20 or 30 capital letters')


# check user input: jump
def check_sieve(jump):
    if jump < 1:
        sys.exit('error: jump must be at least 1')
        

# check user input: plot offset
def check_first_point(first):
    if first < 0:
        sys.exit('error: start index for plotting must be at least 0')    


# check user input: output modes
def check_output_modes(outputs):
    for i in outputs:
        check_output_mode(i)


# check user input: time
def check_time(time):
    if not time > 0:
        sys.exit('error: time must be bigger than 0') 


# check user input: mode vs string
def check_string_length(m, s):

    m_length = int(m[3:])
    s_length = len(s)
    if m_length != s_length:
        sys.exit('error: length of string must be "{}" for mode "{}"'.format(m_length, m)) 


# check user input: interpolation factor
def check_interpolate(interpolate):
    if interpolate < 1:
        sys.exit('error: interpolate must be bigger than 0') 


# create random attractors
def get_attractors(num_guesses, parameter_string, num_points, time, output_modes, sieve, plot_offset, m, interpolate):
    found = 0
    map = get_map_function(m)
    subtitle_string = 'created with PyStrange'
    
    # 2d attractor(s)
    if m[0:2] == '2d':
        
        if time != None:
            print('ignoring time intervall for 2D attractors')

        # single search mode
        if parameter_string != '':
            print('Search for attractor {}:'.format(parameter_string), end=' ')
            if get_attractor_2d_map(parameter_string, num_points, 
                                subtitle_string, output_modes, sieve, plot_offset, map):
                found += 1  

        # random search mode
        else:
            # search for random attractors
            for i in range(num_guesses):
                print('Random attractor {} of {}:'.format(i + 1, num_guesses), end=' ')
                if get_attractor_2d_map(get_random_string(coeff, int(m[3:])), num_points, 
                                    subtitle_string, output_modes, sieve, plot_offset, map):
                    found += 1

    # 3d attractor(s)            
    elif m[0:2] == '3d':

        # single search mode
        if parameter_string != '':

            # map mode
            if time == None:
                print('Search for attractor {}:'.format(parameter_string), end=' ')
                if get_attractor_3d_map(parameter_string, num_points, 
                                    subtitle_string, output_modes, sieve, plot_offset, map):
                    found += 1

            # flow mode
            else:
                print('Search for attractor {}:'.format(parameter_string), end=' ')
                if get_attractor_3d_flow(parameter_string, time, num_points, 
                                    subtitle_string, output_modes, sieve, plot_offset, map, interpolate):
                    found += 1

        # random search mode
        else:

            # map mode
            if time == None:
                # search for random attractors
                for i in range(num_guesses):
                    print('Random attractor {} of {}:'.format(i + 1, num_guesses), end=' ')
                    if get_attractor_3d_map(get_random_string(coeff, int(m[3:])), num_points, 
                                        subtitle_string, output_modes, sieve, plot_offset, map):
                        found += 1

            # flow mode
            else:
                # search for random attractors
                for i in range(num_guesses):
                    print('Random attractor {} of {}:'.format(i + 1, num_guesses), end=' ')
                    if get_attractor_3d_flow(get_random_string(coeff, int(m[3:])), time, num_points, 
                                        subtitle_string, output_modes, sieve, plot_offset, map, interpolate):
                        found += 1                        

    # print number of found attractors
    if found == 0:
        print('No attractor has been found - better luck next time!')
    elif found == 1:
        print('One attractor has been found')
    elif found > 1:
        print(found, 'attractors have been found')


# get map function
def get_map_function(m):
    if m == '3d_30':
        return map_3d_30
    elif m == '3d_60':
        return map_3d_60
    elif m == '3d_105':
        return map_3d_105
    elif m == '2d_12':
        return map_2d_12 
    elif m == '2d_20':
        return map_2d_20


# main function
def main():
    
    # create argument parser
    parser = argparse.ArgumentParser(description=description, epilog=epilog)
    
    # define positional argument
    parser.add_argument('m', type=str, 
                        help='map to be used: "3d_30" or "3d_60" or "2d_12" or "2d_20"')
    
    # define optional arguments
    parser.add_argument('-n', '--number', type=int, default=100, 
                        help='number of guesses: integer > 0, default: 100')
    parser.add_argument('-p', '--points', type=int, default=20000, 
                        help='number of points for plot: integer > 0, default: 20000')
    parser.add_argument('-t', '--time', type=float,
                        help='time intervall for flow mode, recommended value: 0.1, ignored for 2D Attractors')
    parser.add_argument('-s', '--string', type=str, default='', 
                        help='parameter string: string with 12 or 30 capital letters, default: "", "-n" will be ignored')
    parser.add_argument('-o', '--output', type=str, default=['png',], nargs='*',
                        help='output format: "png" ( via matplotlib) and/or "html" (via plotly) and/or "obj" (wavefront), default: "png"')
    parser.add_argument('-j', '--jump', type=int, default=1, 
                        help='plot every J\'th point: integer >= 1, default: 1')
    parser.add_argument('-f', '--first', type=int, default=200, 
                        help='start plotting at index F: integer >= 0, default: 200')    
    parser.add_argument('-i', '--interpolate', type=int, default=1, 
                        help='interploation factor, default: 1') 

    # parse arguments
    args = parser.parse_args()
    
    # check user input
    check_num_points(args.points)
    check_output_modes(args.output)
    check_map_mode(args.m)
    check_sieve(args.jump)
    check_first_point(args.first)
    check_interpolate(args.interpolate)

    if args.time != None:
        check_time(args.time)

    if args.string != '':
        check_string_length(args.m, args.string)
        args.number = 1

    # search for attractor(s)
    get_attractors(args.number, args.string, args.points, args.time, args.output, args.jump, args.first, args.m, args.interpolate)
    

# execute only if run as a script
if __name__ == "__main__":
    main()
