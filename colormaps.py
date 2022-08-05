from matplotlib.colors import LinearSegmentedColormap as lsc
import colorcet as cc



def col_pal(color_code):
    col_scale = color_code
    arc_range = col_scale[0:128]
    col_scale.extend(arc_range)

    return col_scale


trig_scale = {"rainbow1": cc.CET_C1s,
              "rainbow2": cc.CET_R3,
              "rainbow3": cc.CET_R4,
              "rainbow4": cc.CET_C8s,
              "workbow": cc.CET_C3,
              "deuroto": cc.CET_CBC1,
              "red_blue": cc.CET_C4s
              }

rainbow1 = col_pal(trig_scale['rainbow1'])
rainbow2 = col_pal(trig_scale['rainbow2'])
rainbow3 = col_pal(trig_scale['rainbow3'])
rainbow4 = col_pal(trig_scale['rainbow4'])
workbow = col_pal(trig_scale['workbow'])
deuroto = col_pal(trig_scale['deuroto'])
red_blue = col_pal(trig_scale['red_blue'])

from matplotlib import pyplot as plt
import matplotlib as mpl
from matplotlib.gridspec import GridSpec


def plot_all_colormaps():
    '''
        This function will only plot the 82 built in colormaps.
    '''
    fig = plt.figure(facecolor='white', figsize=(25, 15), dpi=300)
    grid = GridSpec(7, 1, hspace=.5, wspace=0.9)
    strings = [s for s in plt.colormaps() if "_r" not in s]
    counter = 0
    while counter < 7:
        column = (counter // 7) % 5
        row = counter % 7
        ax = fig.add_subplot(grid[row, column])
        ax.axis('off')
        cmap_str = strings[counter]
        color_map = plt.get_cmap(cmap_str)
        mpl.colorbar.ColorbarBase(ax, cmap=color_map, orientation='horizontal')
        ax.text(-0.02, 0.5, cmap_str, ha='right', va='center', fontsize=15)
        counter += 1
    else:
        fig.savefig('/Users/Teslagon/Documents/My Documents/xrdata/matplotlib colormaps.png',bbox_inches='tight') #uncomment this if you want to save the figure
        return

#plot_all_colormaps()

# Usage:

# import colormaps as cm
# in heatmap portion there is a parameter for the color scale called mapColor
# example
# ds.xrd_heatmap(**kwargs, ... , mapColor=cm.rainbow1)
