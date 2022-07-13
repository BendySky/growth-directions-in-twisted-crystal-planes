import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
import colorcet as cc
import colormaps as cm
from colormaps import scale
from tkinter import filedialog as fd, LabelFrame
from datasets import datasets as ds
import os, os.path

# from datasets import datasets as ds
if __name__ == '__main__':
    window = tk.Tk()

    window.wm_title("WAXS Growth Plane Analysis")
    window.geometry("750x450+550+150")
    #window.resizable(0, 0)
    #window.attributes("-topmost", 1)
    window.attributes('-alpha', .95)

    #custom theme for tkinter app, needs work before it's functional
    style = ttk.Style()
    style.theme_create('appstyle', parent='alt',
                       settings={
                           'TLabelframe': {
                               'configure': {
                                   'background': '#0deae4'
                               }
                           },
                           'TLabelframe.Label': {
                               'configure': {
                                   # 'background': 'red'     uncomment this to make even label red
                               }
                           }
                       }
                       )
    style.theme_use('appstyle')

    def run_prog():
        #print(folderPath.get())
        direc_path = folderPath.get()

        sort_dir = ds.ch_dir(direc_path)
        dfList = ds.df_to_list(sort_dir)
        angleAtPeak = ds.getMaxPeak(dfList)

        if file_var.get() == 1:
            ds.xrd_heatmap(angleAtPeak, savepath=direc_path, IntOrAng=0,
                           plt_size=hm_sz.get(), plotTitle=hm_ti.get(),
                           mapColor=cm.rainbow1)

            ds.xrd_heatmap(angleAtPeak, savepath=direc_path, IntOrAng=1,
                           plt_size=hm_sz.get(), plotTitle=hm_ti.get(),
                           mapColor=cm.rainbow1)

            color.set('')

            ds.contour_plot(angleAtPeak, savepath=direc_path, plot_title=qp_ti.get(),
                            plot_size=qp_sz.get(), trans=True)

            hm_ti.set('')
            hm_sz.set(35)

            qp_ti.set('')
            qp_sz.set(35)


        else:
            print("do nothing")

    def select_folder():
        #folderPath = StringVar()
        direc_path = fd.askdirectory(title='Select Folder Containing Data', initialdir='/')
        direc_path = f'{direc_path}/'
        folderPath.set(direc_path)

    def file_select():
        choice = file_var.get()
        if choice == 1:
            file = 'text'
        elif choice == 2:
            file = 'png'
        elif choice == 3:
            file = 'tiff'
        file_var.set(choice)

    def serp_sel():
        choice=yn.get()
        if choice == 1:
            serp = True
        elif choice == 2:
            serp = False
        yn.set(choice)

    def cm_select():
        choice = color.get()
        if choice == 'Rainbow 1':
            mapColor = cm.rainbow1
        elif choice == 'Rainbow 2':
            mapColor = cm.rainbow2
        elif choice == 'Rainbow 3':
            mapColor = cm.rainbow3
        elif choice == 'Deuroto':
            mapColor = cm.deuroto
        elif choice == 'Red-Blue':
            mapColor = cm.red_blue
        color.set(choice)

    folderPath = StringVar()
    file_var = IntVar()
    yn = IntVar()
    serp = StringVar()
    color = StringVar()
    hm_ti = StringVar()
    hm_sz = IntVar()
    qp_ti = StringVar()
    qp_sz = IntVar()

    frame1 = tk.LabelFrame(window, text='1. Select Folder')
    frame1.grid(row=1, column=0, rowspan=3, sticky='W',
                padx=15, pady=5, ipady=5)

    #browse_entry = Entry(frame1)
    #browse_entry.grid(row=0, column=0, sticky='WE', padx=5, pady=5)
    browse = Button(frame1, text='Browse...', command=select_folder)
    browse.grid(row=1, column=0, sticky='WE', padx=15, pady=5)

    filetype_options = tk.LabelFrame(window, text=' 2. File Type Options')
    filetype_options.grid(row=0, column=1, columnspan=2, rowspan=3,
                          sticky='W', padx=15, pady=5, ipadx=5, ipady=5)

    filetype = tk.LabelFrame(filetype_options, text='File Type')
    filetype.grid(ipadx=15, ipady=4, padx=15, pady=0, row=1, column=0, columnspan=1, rowspan=3, sticky='S')
    Radiobutton(filetype, text="Text", variable=file_var, value=1, command=file_select, pady=5).pack()
    Radiobutton(filetype, text="PNG", variable=file_var, value=2, command=file_select, pady=5).pack()
    Radiobutton(filetype, text="TIFF", variable=file_var, value=3, command=file_select, pady=5).pack()

    plot_options = tk.LabelFrame(filetype_options, text='Plot Options')
    plot_options.grid(ipadx=15, ipady=5, padx=15, pady=0, row=1, column=1, columnspan=3, rowspan=3)

    rows_label = Label(plot_options, text='Rows')
    rows_label.grid(ipadx=4, padx=4, pady=5, row=0, column=1, sticky='W')
    row_entry = Entry(plot_options)
    row_entry.grid(ipadx=0, padx=4, pady=5, row=0, column=2, sticky='W')

    col_label = Label(plot_options, text='Columns')
    col_label.grid(ipadx=4, padx=4, pady=5, row=1, column=1, sticky='W')
    col_entry = Entry(plot_options)
    col_entry.grid(ipadx=0, padx=4, pady=5, row=1, column=2, sticky='W')

    serp_label = Label(plot_options, text='Serpentine')
    serp_label.grid(ipadx=4, padx=4, pady=5, row=2, column=1, sticky='W')
    serp_buttonY = Radiobutton(plot_options, text='Yes', variable=yn,
                               value=1, pady=5).grid(row=2, column=2, sticky='W')
    serp_buttonX = Radiobutton(plot_options, text='No', variable=yn,
                               value=2, pady=5).grid(row=2, column=2, sticky='E')

    plot_data = tk.LabelFrame(window, text=' 3. Plot Data')
    plot_data.grid(row=8, columnspan=7, rowspan=5,
                   sticky='NW', padx=15, pady=15, ipady=5)
    heatmap_options = LabelFrame(plot_data, text='Heatmap Options')
    heatmap_options.grid(padx=0, pady=0, row=2, column=0, columnspan=2)

    hm_options = LabelFrame(plot_data, text='Heatmap Options')
    hm_options.grid(row=0, column=0, padx=15, pady=15, ipady=5, sticky='NW')

    hm_title = Label(hm_options, text='Plot Title')
    hm_title.grid(padx=0, pady=5, row=0, column=0 , sticky='W')
    hm_entry = Entry(hm_options, textvariable=hm_ti)
    hm_entry.grid(ipadx=4, padx=4, pady=5, row=0, column=1)

    plot_size = Label(hm_options, text='Plot Size')
    plot_size.grid(pady=0, row=1, column=0, sticky='W')
    size_entry = Entry(hm_options, textvariable=hm_sz)
    size_entry.insert(0, 35.)
    size_entry.grid(ipadx=4, padx=4, pady=0, row=1, column=1)

    color_scale = Label(hm_options, text='Color Scale')
    color_scale.grid(padx=0, pady=5, row=2, column=0, sticky='W')
    colors = ("Rainbow 1", "Rainbow 2", "Rainbow 3", "Rainbow 4", "Deuroto", "Red-Blue")
    color_entry = OptionMenu(hm_options, color, *colors)
    color_entry.grid(padx=0, pady=5, row=2, column=1, sticky='W')

    qp_options = LabelFrame(plot_data, text='Quiver Plot Options')
    qp_options.grid(row=0, column=1, padx=15, pady=15, ipady=5, sticky='NW')

    qp_title = Label(qp_options, text='Plot Title')
    qp_title.grid(ipadx=4, padx=4, pady=5, row=0, column=1, sticky='W')
    qp_title_entry = Entry(qp_options, textvariable=qp_ti)
    qp_title_entry.grid(ipadx=4, padx=4, pady=5, row=0, column=2, sticky='W')

    qp_size = Label(qp_options, text='Plot Size')
    qp_size.grid(ipadx=4, padx=4, pady=5, row=1, column=1, sticky='W')
    qp_size_entry = Entry(qp_options, textvariable=qp_sz)
    qp_size_entry.insert(0, 35.)
    qp_size_entry.grid(ipadx=4, padx=4, pady=5, row=1, column=2, sticky='W')
    trans = Label(qp_options, text='Transparent')
    trans.grid(ipadx=4, padx=4, pady=5, row=2, column=1, sticky='W')
    #Radiobutton(qp_options, text='Yes', row=2, column=2).pack()

    direc_button = Button(window, text='Run', command=run_prog)
    direc_button.grid(padx=15, row=20, column=0, sticky='W')

    window.mainloop()
