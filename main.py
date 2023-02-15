from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import utils

data = []
#Callbacks
def select_sld():
    filename = filedialog.askopenfilename(title='Select *.sld', filetypes=[('SLD file', '*.sld')])
    lbl_sld.configure(text = filename)
    btn_read['state'] = 'normal'

def read_sld():
    global data
    filename = lbl_sld.cget('text')
    header, time, load, deform = utils.import_data(filename)
    data = utils.prepare_for_csv(header, time, load, deform)
    lbl_read.configure(text = 'Has been read!')
    for i in range(len(data)):
        tree.insert('', 'end',  values=data[i])
    btn_save['state'] = 'normal'

def save_csv():
    filename = filedialog.asksaveasfilename(defaultextension='csv')
    st = utils.save_to_csv(filename, data)
    if st > 0:
        lbl_csv.configure(text = ('Saved as ' + filename))
    else:
        lbl_csv.configure(text = 'Error!')

def reset_state():
    data = []
    lbl_sld.configure(text = '')
    lbl_read.configure(text = '')
    lbl_csv.configure(text = '')
    btn_read['state'] = 'disabled'
    btn_save['state'] = 'disabled'
    for item in tree.get_children():
      tree.delete(item)
    pass



# Window
window = Tk()
window.geometry('640x320')
window.title('sld2csv')

#Buttons
btn_sld = Button(window, text="Select *.sld", command=select_sld)  
btn_sld.grid(column=0, row=1, padx=2, pady=1, sticky='ew')
lbl_sld = Label(window, text='')
lbl_sld.grid(column=1, row=1, padx=2, pady=1, columnspan=2)


btn_read =  Button(window, text="Read", command=read_sld, state='disabled')
btn_read.grid(column=0, row=2, padx=2, pady=1, sticky='ew')
lbl_read = Label(window, text='')
lbl_read.grid(column=1, row=2, padx=2, pady=1)


btn_save = Button(window, text="Save as CSV", command=save_csv, state='disabled')
btn_save.grid(column=0, row=3, padx=2, pady=1, sticky='ew')
lbl_csv = Label(window, text='')
lbl_csv.grid(column=1, row=3, padx=2, pady=1)


#Table
tree = ttk.Treeview(window, show='', selectmode='browse', columns=('1', '2', '3'))
tree.grid(column=0, row=4, columnspan=2, rowspan=10, padx=2, pady=1, sticky='ew')
vsb = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
vsb.grid(column=3, row=4, rowspan=10, sticky='ns')
tree.configure(yscroll=vsb.set)

#Button
btn_reset = Button(window, text="Reset state", command=reset_state)  
btn_reset.grid(column=0, row=15, padx=2, pady=1, sticky='ew')

window.mainloop()