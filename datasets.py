from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import operator


class datasets:

    def __init__(self, direc, direcList, direcNew, maxInt, maxAngle, IntOrAng):
        self.direc = direc
        self.direcList = direcList
        self.direcNew = direcNew
        self.maxInt = maxInt
        self.maxAngle = maxAngle
        self.IntOrAng = IntOrAng

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

        for i in direc:
            direcList.append(pd.read_csv(i, delimiter=' ', header=None, usecols=col_list))
        direcList = dict(zip(key, direcList))

    def getMaxPeak(dataFn, maxInt, maxAngle):

        for i in range(len(dataFn)):
            maxInt.append(max(dataFn[i][1]))
            maxAngle.append(max(dataFn[i][1].items(), key=operator.itemgetter(1))[0])

    def xrd_heatmap(IntOrAng, plt_size=1.0, plotTitle='', mapColor=''):

        size = int(np.sqrt(len(IntOrAng)))
        mapDim = np.reshape(IntOrAng, (size, size))

        plt.figure(figsize=(plt_size, plt_size))
        plt.title(plotTitle, fontdict={'fontsize': '20'}, pad='10')
        ax = sns.heatmap(mapDim, cmap=mapColor, annot=True, fmt='0g', square=True)
        plt.show()
