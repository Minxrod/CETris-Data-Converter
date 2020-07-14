import tkinter as tk
import objects as obj
from PIL import Image, ImageTk, ImageDraw

# graphic info
pal = None
graphic = []

# object info
items = []   # items in listbox

# dialog classes created using effbot.org as reference
# https://effbot.org/tkinterbook/tkinter-dialog-windows.htm

class AddDialog:
    def __init__(self, master):
        self.master = master
        self.result = None

        self.dialog = tk.Toplevel(self.master)
        self.dialog.geometry()

        self.d_frame = tk.Frame(self.dialog)
        self.d_frame.pack()

        self.d_list = tk.Listbox(self.d_frame)
        self.d_list.pack(side=tk.TOP)
        self.d_list.bind("<Double-Button-1>", self.add)
        self.d_list.bind("<Return>", self.add)
        self.d_list.focus_set()

        for item in obj.item_types:
            self.d_list.insert(tk.END, item)

        self.d_button = tk.Button(self.d_frame, text="Add object", command=self.add)
        self.d_button.pack(side=tk.BOTTOM)

        self.dialog.protocol("WM_DELETE_WINDOW", self.cancel)
        self.dialog.grab_set()
        self.dialog.wait_window(self.dialog)

    def add(self, event=None):
        self.result = self.d_list.curselection()[0]
        self.cancel()

    def cancel(self, event=None):
        self.dialog.destroy()


class EditDialog:

    def __init__(self, master, object):
        self.master = master
        self.result = None

        self.dialog = tk.Toplevel(self.master)
        self.dialog.geometry()

        self.d_frame = tk.Frame(self.dialog)
        self.d_frame.pack()

        # edit options
        self.label = []
        self.entry = []

        r = 0
        cycling = True
        current = object

        while cycling:
            for name, data in zip(current.name, current.data):
                self.label.append(tk.Label(self.d_frame, text=name))
                self.label[-1].grid(row=r, column=0)

                self.entry.append(tk.Entry(self.d_frame))
                self.entry[-1].insert(0, str(data))
                self.entry[-1].grid(row=r, column=1)
                r += 1

            current = current.other

            if current is None:
                cycling = False

        self.d_button = tk.Button(self.d_frame, text="Save Changes", command=self.apply)
        self.d_button.grid(row=r, column=0, columnspan=2)

        self.dialog.protocol("WM_DELETE_WINDOW", self.cancel)
        self.dialog.grab_set()
        self.dialog.wait_window(self.dialog)

    def apply(self, event=None):
        temp = [entry.get() for entry in self.entry]

        self.result = temp

        self.cancel()

    def cancel(self, event=None):
        self.dialog.destroy()


class GUI:

    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master)
        self.frame.pack()

        self.image = Image.new("RGB", (320, 240), 0)
        self.display_image = ImageTk.PhotoImage(self.image)

        self.label = tk.Label(self.frame, image=self.display_image)
        self.label.grid(row=0, column=0)

        self.scroll = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.item_list = tk.Listbox(self.frame, width=50, height=8, yscrollcommand=self.scroll.set)

        self.scroll.config(command=self.item_list.yview)
        self.scroll.grid(row=1, column=1, rowspan=3, sticky="NS")
        self.item_list.grid(row=1, column=0, rowspan=3, columnspan=1)
        self.item_list.bind("<Double-Button-1>", self.edit)

        self.add_button = tk.Button(self.frame, text="Add", command=self.add)
        self.add_button.grid(row=1, column=2, sticky="NSEW")

        self.edit_button = tk.Button(self.frame, text="Edit", command=self.edit)
        self.edit_button.grid(row=2, column=2, sticky="NSEW")

        self.del_button = tk.Button(self.frame, text="Delete", command=self.delete)
        self.del_button.grid(row=3, column=2, sticky="NSEW")

        self.save_button = tk.Button(self.frame, text="Save", command=self.output)
        self.save_button.grid(row=4, column=2, sticky="NSEW")

    def add(self, event=None):
        dialog = AddDialog(self.master)
        select = dialog.result

        # add new item to list
        if select is not None:
            items.append(obj.create_object(select))
            print(items)
            self.item_list.insert(tk.END, obj.item_types[select])

            self.item_list.select_set(tk.END)
            self.edit()

    def edit(self, event=None):
        if len(self.item_list.curselection()) < 1:
            return

        current_obj = items[self.item_list.curselection()[0]]
        dialog = EditDialog(self.master, current_obj)
        result = dialog.result

        def set_obj(item, start):
            item.data = result[start:start+len(item.data)]
            print(item.data)

            if item.other is not None:
                set_obj(item.other, start+len(item.data))

        if result is not None:
            set_obj(current_obj, 0)

        self.draw()

    def delete(self, event=None):
        if len(self.item_list.curselection()) < 1:
            return

        current_obj = items[self.item_list.curselection()[0]]
        items.remove(current_obj)
        self.item_list.delete(tk.ANCHOR)

    def output(self, event=None):
        scan_order = [[], [], []]

        for item in items:
            nest = 0
            while item is not None:
                scan_order[nest].append(item)
                item = item.other
                nest += 1

        index = 0
        for scan in scan_order:
            for item in scan:
                if item.label is None:
                    item.label = "item" + str(index) + ":\n"
                    index += 1
                else:
                    print(item.convert_db())

    def draw(self):
        img = Image.new("RGB", (320, 240))
        imgdw = ImageDraw.Draw(img)

        for item in items:
            item.draw(imgdw)

        self.display_image = ImageTk.PhotoImage(img)
        self.label.config(image=self.display_image)
        self.label.update()


root = tk.Tk()

gui = GUI(root)

root.mainloop()
