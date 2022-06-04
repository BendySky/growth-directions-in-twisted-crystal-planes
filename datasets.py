import operator
import pandas as pd


class datasets:

    def __init__(self, direc, direcList, direcNew, maxVal, maxKey):
        self.direc = direc
        # self.direc1 = direc1
        # self.listDirec = listDirec
        self.direcList = direcList
        self.direcNew = direcNew
        self.maxVal = maxVal
        self.maxKey = maxKey

    # if-else statement is probably bad practice; is there a better way to edit this code??
    # instead of replacing labels, maybe I should have the program determine by "columns"
    # i.e. i=-4 vs i=-3
    def imgOrPlot(self, direc):
        dir_new = set()
        if direc[1].find('plot') != -1:
            for i in direc:
                newLab = i.replace('_waxs_stitched_plot.txt', '')
                dir_new.add(newLab)

        else:
            for i in direc:
                newLab = i.replace('_waxs_stitched.tiff', '')
                dir_new.add(newLab)
        dir_new = list(dir_new)
        return dir_new

    def txtConvert(self, direc):

        direc.sort_direcList(direc, i=-4)
        return direc

    def tiffConvert(self, direc):

        direc.sort_direcList(direc, i=-3)
        return direc

    # invalid operation performed
    def invalid_op(self, x):
        raise Exception("Invalid Operation")

    # determines whether to use txtConvert or tiffConvert method
    def txtOrtiff(self, direc, chosenOP, operationArgs=None):

        operationArgs = operationArgs or {}

        vals = {'_waxs_stitched_plot.txt': direc.txtConvert,
                '_waxs_stitched.tiff': direc.tiffConvert
                }

        imgOrCSV_determ = vals.get(chosenOP, self.invalid_op)

    # sorts the list of filenames by job number
    def sort_direcList(self, direcList, i):

        """takes the created list and sorts the files by job number
        direcList: path to directory stored as a list
        i: column separation between '_' values"""

        direcList.sort(key=lambda x: int(x.split('_')[i]))
        return direcList

    def df_to_dict(self, direc, direcList, peakIntensity, scanAngles):

        """
        :param direc: filenames stored as a list
        :param direcList: filenames converted to a nested dataframe
        :param peakIntensity: stores the peak intensity of each of the scans
        :param scanAngles: stores the range of angles of the detector as a dataframe
        :return:
        """

        key = list(range(len(direc)))
        for i in direc:
            direcList.append(pd.read_csv(i, delimiter=' ', header=None))

        direcList = dict(zip(key, direcList))
        for i in direcList:
            peakIntensity.append(direcList[i][1])
            scanAngles.append(direcList[i][0])

        global final
        final = dict(zip(key, peakIntensity))
        for i in range(len(direcList)):
            val = 'spec' + str(i + 1)
            final[val] = final[i]
        # return final

    def getMaxPeak(self, maxVal, maxKey, dataFn):

        for i in range(len(dataFn)):
            maxVal.append(max(final[i]))
            maxKey.append(max(final[i].items(), key=operator.itemgetter(1))[0])
