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

# Usage:

# import colormaps as cm
# in heatmap portion there is a parameter for the color scale called mapColor
# example
# ds.xrd_heatmap(**kwargs, ... , mapColor=cm.rainbow1)
