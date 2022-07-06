import tkinter as tk
from tkinter import *
import colorcet as cc
from tkinter import filedialog as fd, LabelFrame
from datasets import datasets as ds

# from datasets import datasets as ds
if __name__ == '__main__':
    window = tk.Tk()

    window.wm_title("WAXS Growth Plane Analysis")
    window.geometry("750x450+550+150")
    #window.resizable(0, 0)
    #window.attributes("-topmost", 1)
    #window.attributes('-alpha', 1)

    # noinspection PyTypeChecker

    def run_prog():
        #is this ok???
        direc_path = select_folder()
        #???
        sort_dir = ds.ch_dir(direc_path)
        dfList = ds.df_to_list(sort_dir)
        angleAtPeak = ds.getMaxPeak(dfList)

        return angleAtPeak

    def select_folder():

        direc_path = fd.askdirectory(title='Select Folder Containing Data', initialdir='/')
        direc_path = f'{direc_path}/'

        return direc_path

    def file_select():
        choice = file_var.get()
        if choice == 1:
            file = 'text'
        elif choice == 2:
            file = 'png'
        elif choice == 3:
            file = 'tiff'
        return file

    def serp_sel():
        choice=yn.get()
        if choice == 1:
             serp = True
        elif choice == 2:
            serp = False
        return yn

    #def run_prog():

    #    serp = serp_sel()
    #    ds.xrd_heatmap(angleAtPeak, savepath=direc_path, IntOrAng=0, plt_size=row)

    file_var = IntVar()
    yn = IntVar()
    serp = StringVar()
    color = StringVar()
    qp_ti = StringVar()
    qp_size = StringVar()

    filetype_options = tk.LabelFrame(window, text=' 2. File Type Options')
    filetype_options.grid(row=0, columnspan=2, rowspan=3,
                          sticky='W', padx=15, pady=5, ipady=5)

    filetype = tk.LabelFrame(filetype_options, text='File Type')
    filetype.grid(ipadx=15, ipady=4, padx=15, pady=0, row=1, column=0, columnspan=1, rowspan=3, sticky='S')
    Radiobutton(filetype, text="Text", variable=file_var, value=1, command=file_select, pady=5).pack()
    Radiobutton(filetype, text="PNG", variable=file_var, value=2, command=file_select, pady=5).pack()
    Radiobutton(filetype, text="TIFF", variable=file_var, value=3, command=file_select, pady=5).pack()

    plot_options = tk.LabelFrame(filetype_options, text='Plot Options')
    plot_options.grid(ipadx=15, ipady=5, padx=15, pady=0, row=1, column=1, columnspan=1, rowspan=3)

    rows_label = Label(plot_options, text='Rows')
    rows_label.grid(ipadx=4, padx=4, pady=1, row=0, column=1, sticky='W')
    row_entry = Entry(plot_options)
    row_entry.grid(ipadx=4, padx=4, pady=1, row=0, column=2, sticky='W')

    col_label = Label(plot_options, text='Columns')
    col_label.grid(ipadx=4, padx=4, pady=5, row=1, column=1, sticky='W')
    col_entry = Entry(plot_options)
    col_entry.grid(ipadx=4, padx=4, pady=5, row=1, column=2, sticky='W')

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

    plot_title = Label(hm_options, text='Plot Title')
    plot_title.grid(padx=0, pady=5, row=0, column=0 , sticky='W')
    plot_entry = Entry(hm_options)
    plot_entry.grid(ipadx=4, padx=4, pady=5, row=0, column=1)

    plot_size = Label(hm_options, text='Plot Size')
    plot_size.grid(pady=0, row=1, column=0, sticky='W')
    size_entry = Entry(hm_options)
    size_entry.grid(ipadx=4, padx=4, pady=0, row=1, column=1)

    color_scale = Label(hm_options, text='Color Scale')
    color_scale.grid(padx=0, pady=5, row=2, column=0, sticky='W')
    colors = ("Rainbow 1", "Rainbow 2", "Rainbow 3", "Deuroto", "Red-Blue")
    color_entry = OptionMenu(hm_options, color, *colors)
    color_entry.grid(padx=0, pady=5, row=2, column=1, sticky='W')

    qp_options = LabelFrame(plot_data, text='Quiver Plot Options')
    qp_options.grid(row=0, column=1, padx=15, pady=15, ipady=5, sticky='NW')

    qp_title = Label(qp_options, text='Plot Title')
    qp_title.grid(ipadx=4, padx=4, pady=5, row=0, column=1, sticky='W')
    qp_title_entry = Entry(qp_options)
    qp_title_entry.grid(ipadx=4, padx=4, pady=5, row=0, column=2, sticky='W')

    qp_size = Label(qp_options, text='Plot Size')
    qp_size.grid(ipadx=4, padx=4, pady=5, row=1, column=1, sticky='W')
    qp_size_entry = Entry(qp_options)
    qp_size_entry.grid(ipadx=4, padx=4, pady=5, row=1, column=2, sticky='W')
    trans = Label(qp_options, text='Transparent')
    trans.grid(ipadx=4, padx=4, pady=5, row=2, column=1, sticky='W')
    #Radiobutton(qp_options, text='Yes', row=2, column=2).pack()

    direc_button = Button(window, text='Browse ...', command=select_folder)
    direc_button.grid(padx=15, row=20, column=0, sticky='W')

    #run_button = Button(window, text=' Run ', command=run_prog)
    #run_button.grid(padx=10, row=20, column=0)

    window.mainloop()