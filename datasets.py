import pandas as pd
import os, os.path
import shutil
import glob


def ch_dir(direcPath):

    os.chdir(f'{direcPath}')
    mk_dataspace(direcPath)
    os.chdir(f'{direcPath}/raw_data/')
    sort_direc = os.listdir(f'{direcPath}/raw_data')
    sort_direc = imgOrPlot(sort_direc)

    dfList = df_to_list(sort_direc)
    angleAtPeak = getMaxPeak(dfList)
    #return sort_direc
    return angleAtPeak


def mk_dataspace(direc):

    new_dirs = ['raw_data', 'plots', 'unstitched_plots']

    isdir = os.path.isdir(f'{direc}/{new_dirs[0]}')
    if not isdir:

        print("Directories do not yet exist")
        for items in new_dirs:
            os.mkdir(items)

        mime = os.listdir(direc)
        if mime[1].find(".txt") != -1:
            pattern = "*.txt"
        elif mime[1].find(".png") != -1:
            pattern = "*.png"
        else:
            pattern = "*.tiff"

        files = glob.glob(direc + pattern)

        # moves text files to 'raw_data' folder
        for file in files:
            file_name = os.path.basename(file)
            shutil.move(file, direc + new_dirs[0] + '/' + file_name)
        print("\nInitial files moved to new filepath"
              " at:\n", direc + new_dirs[0])
    else:
        print("Directories already exist")


def sort_direcList(direcList, i):
    direcList.sort(key=lambda x: int(x.split('_')[i]))
    return direcList


def imgOrPlot(direc):
    dir_new = []

    if direc[1].find('plot') != -1:
        for i in direc:
            dir_new = sort_direcList(direc, i=-4)

    else:
        for i in direc:
            dir_new = sort_direcList(direc, i=-3)

    return dir_new


def getMaxPeak(dataFn):
    PeakAngle = []

    for i in range(len(dataFn)):
        PeakAngle.append(dataFn[i].loc[dataFn[i]['Intensity'].idxmax()].tolist())

    return PeakAngle


def df_to_list(dirr):

    key = list(range(len(dirr)))
    col_list = [0, 1]
    rename = ["Angle", "Intensity"]
    direcList = []

    for i in dirr:
        direcList.append(pd.read_csv(i, delimiter=' ', header=None, names=rename, usecols=col_list))

    return direcList
