import tkinter as tk



class MenuBar:
    def __init__(self, gui):
        menu_bar = tk.Menu(gui.root)
        gui.root.config(menu=menu_bar)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New")
        file_menu.add_command(label="Open")
        file_menu.add_command(label="Save")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=gui.root.quit)

        edit_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo")
        edit_menu.add_command(label="Redo")
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut")
        edit_menu.add_command(label="Copy")
        edit_menu.add_command(label="Paste")

class LeftFrame:
    def __init__(self, gui):
        self.left_frame = tk.Frame(gui.root, width=200, bg="black")
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.listbox = tk.Listbox(
            self.left_frame,
            bg="black",
            activestyle="dotbox",
            font="Helvetica",
            fg="white",
        )
        for i in range(100):
            self.listbox.insert(tk.END, "This is line number " + str(i))
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar = tk.Scrollbar(gui.root)
        scrollbar.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.config(command=self.listbox.yview)
        self.listbox.config(yscrollcommand=scrollbar.set)

        self.listbox.bind('<<ListboxSelect>>', gui.select_item)




class DisplayFrame:
    def __init__(self, gui):
        display_frame = tk.Frame(gui.root, bg="blue")
        display_frame.pack(side=tk.LEFT, fill=tk.BOTH)
        text = tk.Text(display_frame, bg="blue", fg="white")
        text.pack(side=tk.LEFT, fill=tk.BOTH)
        # scrollbar = tk.Scrollbar(gui.root)
        # scrollbar.pack(side=tk.LEFT, fill=tk.BOTH)
        # scrollbar.config(command=text.yview)
        # text.config(yscrollcommand=scrollbar.set)

class GUI:
    # constructor
    def __init__(self):
        self.max_width, self.max_height = self.get_display_size()
        self.root = tk.Tk()
        self.root.geometry(f"{self.max_width}x{self.max_height}")
        self.left = LeftFrame(self)
        self.menu = MenuBar(self)
        self.right = DisplayFrame(self)
        self.root.mainloop()
    
    def select_item(self, event):
        widget = event.widget
        selection = widget.curselection()
        value = widget.get(selection[0])
        print(value)


    def get_display_size(self):
        root = tk.Tk()
        # set the Tk window to transparent
        root.attributes("-alpha", 0)
        display_height = root.winfo_screenheight()
        display_width = root.winfo_screenwidth()
        root.destroy()
        return display_width, display_height

# create an object to Scrollbar class
s = GUI()
