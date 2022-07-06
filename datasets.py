from mpl_toolkits.axes_grid1 import ImageGrid
from matplotlib import pyplot as plt
from math import log, pi
from PIL import Image
import seaborn as sns
import pandas as pd
import os, os.path
import numpy as np
import shutil
import glob


class datasets:

    def __init__(self, direc, direcPath, data_direc, direcList, direcNew, PeakAngle, IntOrAng):
        self.direc = direc
        self.direcPath = direcPath
        self.data_direc = data_direc
        self.direcList = direcList
        self.direcNew = direcNew
        self.PeakAngle = PeakAngle
        self.IntOrAng = IntOrAng

    def ch_dir(direcPath):

        '''
        :param direc: stores all filenames in a directory as a list
        :param direcPath: folder path specified outside of class; describes location of data
        '''

        os.chdir(f'{direcPath}')
        datasets.mk_dataspace(direcPath)
        os.chdir(f'{direcPath}/raw_data/')
        direc = os.listdir(f'{direcPath}/raw_data')
        sort_direc = datasets.imgOrPlot(direc)

        return sort_direc

    def mk_dataspace(data_direc):

        '''
        :param direcPath: folder path specified outside of class; describes location of data
        '''

        new_dirs = ['raw_data', 'plots', 'unstitched_plots']

        # tells if the string 'raw_data' exists in the current directory
        isdir = os.path.isdir(f'{data_direc}/{new_dirs[0]}')
        if isdir == False:

            print("Directories do not yet exist")
            for items in new_dirs:
                os.mkdir(items)

                # merge current directory with new folder 'raw_data'
            new_direc = os.path.join(data_direc, new_dirs[0])

            mime = os.listdir(data_direc)
            if mime[1].find(".txt") != -1:
                pattern = "*.txt"
            elif mime[1].find(".png") != -1:
                pattern = "*.png"
            else:
                pattern = "*.tiff"

            files = glob.glob(data_direc + pattern)

            # moves text files to 'raw_data' folder
            for file in files:
                file_name = os.path.basename(file)
                shutil.move(file, data_direc + new_dirs[0] + '/' + file_name)
            print("\nInitial files moved to new filepath"
                  "at:\n", data_direc + new_dirs[0])
        else:
            print("Directories already exist")

    # sorts the list of filenames by job number
    def sort_direcList(direcList, i):

        """takes the created list and sorts the files by job number
        direcList: path to directory stored as a list
        i: column separation between '_' values"""

        direcList.sort(key=lambda x: int(x.split('_')[i]))
        return direcList

        # if-else statement is probably bad practice; is there a better way to edit this code??

    def imgOrPlot(direc):
        dir_new = []
        # dir_new = set()
        if direc[1].find('plot') != -1:
            for i in direc:
                dir_new = datasets.sort_direcList(direc, i=-4)
                # newLab = i.replace('_waxs_stitched_plot.', '')
                # dir_new.add(newLab)

        else:
            for i in direc:
                dir_new = datasets.sort_direcList(direc, i=-3)
                # newLab = i.replace('_waxs_stitched.tiff', '')
                # dir_new.add(newLab)
        # dir_new = list(dir_new)
        return dir_new

    def df_to_list(direc, direcList):

        '''
        :param direc: filenames stored in a list
        :direcList: filenames converted into a nested dataframe.
                    standard deviations are dropped as they are not needed
        '''

        key = list(range(len(direc)))
        col_list = [0, 1]
        rename = ["Angle", "Intensity"]

        for i in direc:
            direcList.append(pd.read_csv(i, delimiter=' ', header=None, names=rename, usecols=col_list))

        direcList = dict(zip(key, direcList))

    def logInt(PeakAngle):

        # calculates the log10 value of the intensity
        # and returns it in the same list
        for i in range(len(PeakAngle)):
            PeakAngle[i][1] = log(PeakAngle[i][1])

        return PeakAngle

    def getMaxPeak(dataFn, PeakAngle):

        # map max intensity to corresponding angle
        for i in range(len(dataFn)):
            PeakAngle.append(dataFn[i].loc[dataFn[i]['Intensity'].idxmax()].tolist())

        # use logInt method to convert intensity to log(intensity)
        datasets.logInt(PeakAngle)

    def contour_plot(PeakAngle, savepath='', plot_title='', plot_size=15., trans = True):

        mesh = []
        size = int(np.sqrt(len(PeakAngle)))

        # convert array into meshgrid and re-arrange order so
        # the quiver plot matches the micrograph, heatmaps etc.
        for i in range(len(PeakAngle)):
            mesh.append(PeakAngle[i][0])

        mesh.reverse()
        mesh = np.meshgrid(mesh)
        mesh = np.reshape(mesh, (size, size))

        for i in range(len(mesh)):
            mesh[i] = mesh[i][::-1]

        fig, ax = plt.subplots(figsize=(plot_size, plot_size))

        # create empty list for coordinates of quiver plot
        arr = []
        range(int(np.sqrt(len(PeakAngle))))
        for i in range(int(np.sqrt(len(PeakAngle)))):
            arr.append(i)

        x_pos, y_pos = arr, arr

        # map angles to corresponding locations on sinosoidal plot.
        # see the trigonometric circle to get a better understanding
        # of what is happening here
        X, Y = np.cos(mesh * (pi / 180)), np.sin(mesh * (pi / 180))

        # quiver plot
        ax.quiver(x_pos, y_pos, X, Y, pivot='middle')
        ax.title.set_text(plot_title)
        plt.savefig(f'{savepath}/plots/quiver_plot.png', transparent=trans)
        plt.show()

    def xrd_heatmap(PeakAngle, savepath='', IntOrAng=1, plt_size=1.0, plotTitle='', mapColor=''):

        reshape = []
        size = int(np.sqrt(len(PeakAngle)))

        for i in range(len(PeakAngle)):
            reshape.append(PeakAngle[i][IntOrAng])

        mapDim = np.reshape(reshape, (size, size))

        plt.figure(figsize=(plt_size, plt_size))
        plt.title(plotTitle, fontdict={'fontsize': '35'}, pad='10')
        ax = sns.heatmap(mapDim, cmap=mapColor, annot=True, fmt='0g', square=True)
        plt.savefig(f'{savepath}/plots/{plotTitle}.png')
        plt.show()

    def angleVintensity_plots(direcList, dir_name='current_dataset'):

        # foldername = os.path.basename(dir_name)
        # path = os.path.join(savepath, foldername)
        # os.mkdir(path)

        for i in range(len(direcList)):
            plt.title(f'XRD_{i}');
            direcList[i].plot(x='Angle', y='Intensity', title=f'XRD_{i}');
            plt.savefig(f'{dir_name}/unstitched_plots/1d_plots_{i}_.png');

    def plot_scans(filePath, rows_cols=(1, 1), serpentine=False, filetype='text'):

        if filetype == 'text':
            grab_path = f'{filePath}/unstitched_plots'
            sort = -2
        elif filetype == 'tiff':
            grab_path = f'{filePath}/raw_data'
            sort = -3
        elif filetype == 'png':
            grab_path = f'{filePath}/raw_data'
            sort = -3

        direc = os.listdir(grab_path)

        fs = int(np.sqrt(len(direc)))

        direc = datasets.sort_direcList(direc, i=sort)
        direc = np.reshape(direc, rows_cols)
        if serpentine:
            print("serpentine scans were used; adjusting accordingly")
            direc[1::2, :] = direc[1::2, ::-1]
        else:
            print("No serpentine scans. plot order unchanged")
        direc = np.concatenate(direc)
        direc = direc.tolist()

        imgs = []
        valid_images = ['.png', '.tiff']

        for i in direc:
            ext = os.path.splitext(i)[1]
            if ext.lower() not in valid_images:
                continue
            imgs.append(Image.open(os.path.join(grab_path, i)))  # filePath

        fig = plt.figure(figsize=(145., 145.))
        grid = ImageGrid(fig, 111, nrows_ncols=rows_cols, direction='row')

        for ax, im in zip(grid, imgs):
            ax.imshow(im)

        plt.savefig(f'{filePath}/plots/stitched_plot.png')