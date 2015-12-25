"""Contains all the scripts for plotting data.  Plotting package use is matplotlib, available at 
http://matplotlib.org/.  Every script should accept any number of data sets in implicitly paired lists, such that
data at index i in the xdata list should correspond to data at index i in the ydata list."""

#Global
import matplotlib.pyplot as plt
import numpy as np
#Local

def plot_hist(xdata, ylabel):
    """Plots a histogram of n data sets where n == len(xdata) == len(ydata)"""
    fig = plt.figure(figsize=(6,3))
    #plt.hist(xdata, 2, normed=True)
    #plt.show()

    ##weights = np.ones_like(xdata)/float(len(xdata))
    ##plt.hist(xdata, bins=100, weights=weights)
    ##plt.show()
    density, bins = np.histogram(xdata, bins=100, density=True)
    unity_density = density/density.sum()
    bincenters = 0.5*(bins[1:]+bins[:-1])
    plt.plot(bincenters, unity_density)
    plt.show()

if __name__ == "__main__":
    print("This file defines plotting scripts using the matplotlib plotting library")
