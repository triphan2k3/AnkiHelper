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
        left_frame = tk.Frame(gui.root, width=200, bg="grey")
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        listbox = tk.Listbox(
            left_frame,
            bg="grey",
            activestyle="dotbox",
            font="Helvetica",
            fg="yellow",
        )
        for i in range(100):
            listbox.insert(tk.END, "This is line number " + str(i))
        listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar = tk.Scrollbar(gui.root)
        scrollbar.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.config(command=listbox.yview)
        listbox.config(yscrollcommand=scrollbar.set)
    

class GUI:

    # constructor
    def __init__(self):
        self.max_width, self.max_height = self.get_display_size()
        self.root = tk.Tk()
        self.root.geometry(f"{self.max_width}x{self.max_height}")

        LeftFrame(self)
        MenuBar(self)

        self.root.mainloop()
    
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
