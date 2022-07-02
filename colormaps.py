import colorcet as cc


def col_pal(color_code):
    col_scale = color_code
    arc_range = col_scale[0:64]
    col_scale.extend(arc_range)

    return col_scale


scale = {"rainbow1": cc.CET_C1s,
         "rainbow2": cc.CET_R3,
         "rainbow3": cc.CET_R4,
         "rainbow4": cc.CET_C8s,
         "workbow": cc.CET_C3,
         "deuroto": cc.CET_CBC1,
         "red_blue": cc.CET_C4s
         }

rainbow1 = col_pal(scale['rainbow1'])
rainbow2 = col_pal(scale['rainbow2'])
rainbow3 = col_pal(scale['rainbow3'])
rainbow4 = col_pal(scale['rainbow4'])
workbow = col_pal(scale['workbow'])
deuroto = col_pal(scale['deuroto'])
red_blue = col_pal(scale['deuroto'])

# Usage:

# import colormaps as cm
# in heatmap portion there is a parameter for the color scale called mapColor
# example
# ds.xrd_heatmap(**kwargs, ... , mapColor=cm.rainbow1)
