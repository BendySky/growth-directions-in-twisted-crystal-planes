from mpl_toolkits.axes_grid1 import ImageGrid
from matplotlib import pyplot as plt
from PIL import Image
import seaborn as sns
import pandas as pd
import os, os.path
import numpy as np
import operator
import shutil
import glob


class datasets:

    def __init__(self, data_direc, direc, direcList, direcNew, maxVal, maxKey, IntOrAng):
        self.direc = direc
        self.data_direc = data_direc
        self.direcList = direcList
        self.direcNew = direcNew
        self.maxInt = maxInt
        self.maxAngle = maxAngle
        self.IntOrAng = IntOrAng

    def mk_dataspace(data_direc):

        new_dirs = ['raw_data', 'plots', 'unstitched_plots']

        # tells if the string 'raw_data' exists in the current directory
        isdir = os.path.isdir(f'{data_direc}/{new_dirs[0]}')
        if isdir == False:

            print("Directories do not yet exist")
            for items in new_dirs:
                os.mkdir(items)

                # merge current directory with new folder 'raw_data'
            new_direc = os.path.join(data_direc, new_dirs[0])

            pattern = '*.txt'
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
                dir_new = datasets.sort_direcList(direc, i=3)
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
            direcList.append(pd.read_csv(i, delimiter=' ', header=None,
                                         names=rename, usecols=col_list))

        direcList = dict(zip(key, direcList))

    def getMaxPeak(dataFn, maxIntAngle):

        for i in range(len(dataFn)):
            # maxInt.append(max(dataFn[i]['Intensity']))
            # maxAngle.append(max(dataFn[i]['Intensity'].items(), key=operator.itemgetter(1))[0])
            maxIntAngle.append(dataFn[i].loc[dataFn[i]['Intensity'].idxmax()].tolist())

    def xrd_heatmap(PeakAngle, IntOrAng=1, plt_size=1.0, plotTitle='', mapColor=''):

        reshape = []
        size = int(np.sqrt(len(PeakAngle)))

        for i in range(len(PeakAngle)):
            reshape.append(PeakAngle[i][IntOrAng])

        mapDim = np.reshape(reshape, (size, size))

        plt.figure(figsize=(plt_size, plt_size))
        plt.title(plotTitle, fontdict={'fontsize': '20'}, pad='10')
        ax = sns.heatmap(mapDim, cmap=mapColor, annot=True, fmt='0g', square=True)
        plt.show()

    def angleVintensity_plots(direcList, dir_name='current_dataset', savepath='path'):

        foldername = os.path.basename(dir_name)

        path = os.path.join(savepath, foldername)
        os.mkdir(path)

        for i in range(len(direcList)):
            plt.title(f'XRD_{i}');
            direcList[i].plot(x='Angle', y='Intensity', title=f'XRD_{i}');
            plt.savefig(f'{path}/1d_plots_{i}_.png');

    def plot_scans(direc, filePath, serpentine=False):

        fs = int(np.sqrt(len(direc)))

        direc = datasets.sort_direcList(direc, i=-2)
        direc = np.reshape(direc, (fs, fs))
        if serpentine == True:
            print("serpentine scans were used; adjusting accordingly")
            direc[1::2, :] = direc[1::2, ::-1]
        else:
            print("No serpentine scans. plot order unchanged")
        direc = np.concatenate(direc)
        direc = direc.tolist()

        imgs = []
        valid_images = ['.png', '.jpeg', '.tiff']

        for i in direc:
            ext = os.path.splitext(i)[1]
            if ext.lower() not in valid_images:
                continue
            imgs.append(Image.open(os.path.join(filePath, i)))

        fig = plt.figure(figsize=(145., 145.))
        grid = ImageGrid(fig, 111, nrows_ncols=(fs, fs), direction='row')

        for ax, im in zip(grid, imgs):
            ax.imshow(im)