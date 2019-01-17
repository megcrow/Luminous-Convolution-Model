import matplotlib.pyplot as plt
import numpy as np
import os
import math
from os import listdir
from scipy import interpolate

DATA_DIR = './Data/'

# Import galaxy data
def import_data():
    data_list = []
    for item in os.listdir(DATA_DIR):
        if not item.startswith('.'):
            data_list.append(item)
    return data_list


# Load data from files into matrix [[[r values], [yvalues]]]
def get_data(ycol):
    data_matrix = []
    data_list = import_data()
    for file in data_list:
        with open(DATA_DIR + file, 'r') as f:
            next(f)
            x, y = [], []
            for line in f:
                values = [float(s) for s in line.split(   )]
                # Remove gas, bulge data for galaxies with no recorded values
                # if values[ycol] != 0:
                x.append(values[0])
                y.append(values[ycol])
            data_matrix.append([x, y])
    return data_matrix


# Plot raw galaxy data
def plot_raw_data(ycol, xlabel, ylabel, title):
    data_matrix = get_data(ycol)
    plt.clf()
    for i in range(len(data_matrix)):
        x = data_matrix[i][0]
        y = data_matrix[i][1]
        plt.plot(x, y, marker='o', markersize=2)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()


# Scale radius such that 0<r<1. The list scaled_radii preserves groupings
# radii by galaxy. Index [0]-[50] corresponds to the radii of the
# respective file number
def scaled_radii(ycol):
    scaled_radii = []
    ycol_data_matrix = get_data(ycol)
    for i in range(len(ycol_data_matrix)):
        rmax = max(ycol_data_matrix[i][0])
        rscaled_list = []
        for j in range(len(ycol_data_matrix[i][0])):
            rscaled = ycol_data_matrix[i][0][j] / rmax
            rscaled_list.append(rscaled)
        scaled_radii.append(rscaled_list)
    return scaled_radii


# Calculate Luminous Velocity for each galaxy vlum = sqrt(vbulge^2 + vdisk^2 +vgas^2)
def calc_vlum(ycol1, ycol2, ycol3):
    vlum = []
    vdisk_matrix = get_data(ycol1)
    vgas_matrix = get_data(ycol2)
    vbulge_matrix = get_data(ycol3)
    for i in range(len(vdisk_matrix)):
        vlum_list = []
        for j in range(len(vdisk_matrix[i][1])):
            vdisk_sqrd = vdisk_matrix[i][1][j]**2
            vgas_sqrd = vgas_matrix[i][1][j]**2
            vbulge_sqrd = vbulge_matrix[i][1][j]**2
            vlum_val = math.sqrt(vdisk_sqrd + vgas_sqrd + vbulge_sqrd)
            vlum_list.append(vlum_val)
        vlum.append(vlum_list)
    return vlum


# Function to plot VLum data vs. scaled r values
def plot_scaled_data():
    scalrad = scaled_radii(4)
    vlum_vals = calc_vlum(4, 5, 6)
    v = []
    for i in range(len(scalrad)):
        r_obs_scal = scalrad[i]
        v = vlum_vals[i]
        plt.plot(r_obs_scal, v, marker='o', markersize=2)
    plt.xlabel('Radius (scaled)')
    plt.ylabel('Luminous Velocity (km/s)')
    plt.title('Scaled Data')
    plt.show()


# Function to visualize raw data. ycol corresponds to velocity data:
# observed, disk, gas, or bulge.
def visualize_raw_data(ycol, y_label, title):
    x_label = 'Radius (kpc)'
    plot_raw_data(ycol, x_label, y_label, title)


def main():
    # Close all figure windows to free memory before initialization
    plt.close('all')

    visualize_raw_data(2, 'Observed Velocity (km/s)', 'Raw Data: Observed Velocity')
    visualize_raw_data(4, 'Disk Velocity (km/s)', 'Raw Data (Disk Velocity)')
    visualize_raw_data(5, 'Gas Velocity (km/s)', 'Raw Data (Gas Velocity)')
    visualize_raw_data(6, 'Bulge Velocity (km/s)', 'Raw Data (Bulge Velocity)')

    # Scaled luminous velocity data
    plot_scaled_data()


main()
