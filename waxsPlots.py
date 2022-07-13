from mpl_toolkits.axes_grid1 import ImageGrid
from matplotlib import pyplot as plt
import datasets as ds
import seaborn as sns
from PIL import Image
from math import pi
import numpy as np
import os, os.path


class plotscans:

    def __init__(self, peakAngle, savepath='', plot_title='', plot_size=10.):

        self.peakAngle = peakAngle
        self.savepath = savepath
        self.plot_title = plot_title
        self.plot_size = plot_size

    def contour_plot(self, trans=True):

        peakAngle = self.peakAngle
        savepath = self.savepath
        plot_title = self.plot_title
        plot_size = self.plot_size

        mesh = []
        size = int(np.sqrt(len(peakAngle)))

        # convert array into meshgrid and re-arrange order so
        # the quiver plot matches the micrograph, heatmaps etc.
        for i in range(len(peakAngle)):
            mesh.append(peakAngle[i][0])

        mesh.reverse()
        mesh = np.meshgrid(mesh)
        mesh = np.reshape(mesh, (size, size))

        for i in range(len(mesh)):
            mesh[i] = mesh[i][::-1]

        fig, ax = plt.subplots(figsize=(plot_size, plot_size))

        # create empty list for coordinates of quiver plot
        arr = []
        range(int(np.sqrt(len(peakAngle))))
        for i in range(int(np.sqrt(len(peakAngle)))):
            arr.append(i)

        x_pos, y_pos = arr, arr
        '''
            map angles to corresponding locations on sinosoidal plot.
            see the trigonometric circle to get a better understanding
            of what is happening here
        '''
        X, Y = np.cos(mesh * (pi / 180)), np.sin(mesh * (pi / 180))

        # quiver plot
        ax.quiver(x_pos, y_pos, X, Y, pivot='middle')
        ax.title.set_text(plot_title)
        plt.savefig(f'{savepath}/plots/quiver_plot.png', transparent=trans)
        #plt.show()

    def xrd_heatmap(self, IntOrAng=1, mapColor=''):

        peakAngle = self.peakAngle
        savepath = self.savepath
        plot_title = self.plot_title
        plot_size = self.plot_size

        if IntOrAng == 0:
            name = 'Angle'
        else:
            name = 'Intensity'
        reshape = []
        size = int(np.sqrt(len(peakAngle)))

        for i in range(len(peakAngle)):
            reshape.append(peakAngle[i][IntOrAng])

        mapDim = np.reshape(reshape, (size, size))

        plt.figure(figsize=(plot_size, plot_size))
        plt.title(plot_title, fontdict={'fontsize': '35'}, pad='10')
        ax = sns.heatmap(mapDim, cmap=mapColor, annot=True, fmt='0g', square=True)
        plt.savefig(f'{savepath}/plots/{plot_title} {name}_nameplot.png')
        # plt.show()

    def angleVintensity_plots(self, direcList):
        dir_name = self.savepath
        # foldername = os.path.basename(dir_name)
        # path = os.path.join(savepath, foldername)
        # os.mkdir(path)

        for i in range(len(direcList)):
            plt.title(f'XRD_{i}');
            direcList[i].plot(x='Angle', y='Intensity', title=f'XRD_{i}');
            plt.savefig(f'{dir_name}/unstitched_plots/1d_plots_{i}_.png');

    def plot_scans(self, rows_cols=(1, 1), serpentine=False, filetype='text'):

        filePath = self.savepath
        if filetype == 'text':
            grab_path = f'{filePath}/unstitched_plots'
            sort = -2
        elif filetype == 'tiff':
            grab_path = f'{filePath}/raw_data'
            sort = -3
        elif filetype == 'png':
            grab_path = f'{filePath}/raw_data'
            sort = -3

        dir_list = os.listdir(grab_path)

        fs = int(np.sqrt(len(dir_list)))

        dir_list = ds.sort_direcList(dir_list, i=sort)
        dir_list = np.reshape(dir_list, rows_cols)
        if serpentine:
            print("serpentine scans were used; adjusting accordingly")
            dir_list[1::2, :] = dir_list[1::2, ::-1]
        else:
            print("No serpentine scans. plot order unchanged")
        dir_list = np.concatenate(dir_list)
        dir_list = dir_list.tolist()

        imgs = []
        valid_images = ['.png', '.tiff']

        for i in dir_list:
            ext = os.path.splitext(i)[1]
            if ext.lower() not in valid_images:
                continue
            imgs.append(Image.open(os.path.join(grab_path, i)))  # filePath

        fig = plt.figure(figsize=(145., 145.))
        grid = ImageGrid(fig, 111, nrows_ncols=rows_cols, direction='row')

        for ax, im in zip(grid, imgs):
            ax.imshow(im)

        plt.savefig(f'{filePath}/plots/stitched_plot.png')