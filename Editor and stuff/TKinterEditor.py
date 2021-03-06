#required for anything GUI related    ########   138   ########
import tkinter as tk
#required for fileopen and save options
from tkinter import filedialog
#required for file's basename
import os
#required for save_before_leave basically
from tkinter import messagebox
#required for delay starting starting message
import time
#required for run_file
import Interpreter

print('Powered by NaePad. Echo Code created by Echo Dev.')
time.sleep(1)

#Nae Unicode text entering is missing

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Untitled - NaePad & Echo Code")

        self.mainFrame = MainFrame(self)
        self.mainFrame.pack(fill="both", expand=True)

        self.mainFrame.text.focus_set()
        self.protocol("WM_DELETE_WINDOW", lambda : self.save_before_leave(self.destroy))

    def save_before_leave(self, callback, *args):

        textBuffer = self.mainFrame.text.get('1.0', 'end-1c')

        #if there's a current file
        if self.mainFrame.curFilePath:
            #if it content doesn't match the current buffer
            if self.mainFrame.curFileCont != textBuffer:
                response = messagebox.askyesnocancel("NaePad & Echo Code - Unsaved File", "Do you want to save before leaving?")
                #if response is yes
                if response:
                    self.mainFrame.save_file()
                    callback()
                #if response is no
                elif response is False:
                    callback()

            else:
                callback()

        else:
            #if there's any text in the buffer
            if textBuffer:
                response = messagebox.askyesnocancel("NaePad & Echo Code - Unsaved File", "Do you want to save before leaving?")
                #If it's a yes
                if response:
                    self.mainFrame.save_as_file()
                    callback()
                #if it's a no
                elif response is False:
                    callback()
            else:
                callback()
        #required in order to prevent "tagbinds" from happening
        return "break"


class MainFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        #creates and displays the Menu
        self.menu = MainMenu(master)
        master.config(menu=self.menu)

        #path of the current file
        self.curFilePath = ''

        #current file
        self.curFileCont = ''

        self.text = tk.Text(self, wrap="none")
        #color scheme
        self.text.config(bg='#282c34',fg='#abb2bf', selectbackground='#3e4451')
        self.text.grid(row=0, column=0, sticky="nsew")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.scroll_bar_config()
        self.menu_command_config()
        self.key_binds_config()


    #scrollbar configurations for self.text widget
    def scroll_bar_config(self):

        self.scrollY = AutoScrollbar(self, orient="vertical", command=self.text.yview)
        self.scrollY.grid(row=0, column=1, sticky="nsew")
        self.text['yscrollcommand'] = self.scrollY.set

        self.scrollX = AutoScrollbar(self, orient="horizontal", command=self.text.xview)
        self.scrollX.grid(row=1, column=0, sticky="nsew")
        self.text['xscrollcommand'] = self.scrollX.set

    def menu_command_config(self):
        #New
        self.menu.file.entryconfig(0, command=lambda : self.master.save_before_leave(self.new_file))
        #Open...
        self.menu.file.entryconfig(1, command=lambda : self.master.save_before_leave(self.open_file))
        #Save
        self.menu.file.entryconfig(2, command=self.save_file)
        #Save as
        self.menu.file.entryconfig(3, command=self.save_as_file)

        #Cut
        self.menu.edit.entryconfig(0, command=self.cut)
        #Copy
        self.menu.edit.entryconfig(1, command=self.copy)
        #Paste
        self.menu.edit.entryconfig(2, command=self.paste)
        #Delete
        self.menu.edit.entryconfig(3, command=self.delete)

    def key_binds_config(self):
        self.text.bind('<Control-n>', lambda event : self.master.save_before_leave(self.new_file))
        self.text.bind('<Control-N>', lambda event : self.master.save_before_leave(self.new_file))
        self.text.bind('<Control-o>', lambda event : self.master.save_before_leave(self.open_file))
        self.text.bind('<Control-O>', lambda event : self.master.save_before_leave(self.open_file))
        self.text.bind('<F5>', self.run_file)
        self.text.bind('<Control-s>', self.save_file)
        self.text.bind('<Control-S>', self.save_file)
        self.text.bind('<Control-Shift-s>', self.save_as_file)
        self.text.bind('<Control-Shift-S>', self.save_as_file)



    def run_file(self, *args):
        Interpreter.run_file(self.curFilePath)

    def new_file(self, *args):
        self.text.delete("1.0", "end")
        self.curFilePath = ''
        self.curFileCont = ''

        #update window name to file name BAD NAE BAD
        self.master.title("Untitled - NaePad & Echo Code")


    def open_file(self, *args):

        #get filepath from user with gui
        filePath = filedialog.askopenfilename(filetypes=(("Text files", "*.txt"),("Echo Code files", "*.ech"),("All files", "*.*")))

        # if filePath is selected
        if filePath:
            try:
                #open only UTF-8 encoded files
                with open(filePath, encoding="UTF-8") as f:
                    self.text.delete("1.0", "end")
                    self.curFileCont = f.read()
                    self.text.insert("1.0", self.curFileCont)
            #if it's not UTF-8 then
            except UnicodeDecodeError:
                #open as ANSI encoding
                with open(filePath, encoding="ANSI") as f:
                    self.text.delete("1.0", "end")
                    self.curFileCont = f.read()
                    self.text.insert("1.0", self.curFileCont)

            #update window name to file name BAD NAE BAD
            self.master.title(os.path.basename(f.name) + " - NaePad & Echo Code")

            #update current file path
            self.curFilePath = filePath

    def save_file(self, *args):
        #if there's already a file
        if self.curFilePath:
            try:
                #open only UTF-8 encoded files
                with open(self.curFilePath, 'w', encoding="UTF-8") as f:
                    self.curFileCont = self.text.get('1.0', 'end-1c')
                    f.write(self.curFileCont)
            #if it's not UTF-8 then
            except UnicodeDecodeError:
                #open as ANSI encoding
                with open(self.curFilePath, 'w', encoding="ANSI") as f:
                    self.curFileCont = self.text.get('1.0', 'end-1c')
                    f.write(self.curFileCont)

            #update window name to file name BAD NAE BAD
            self.master.title(os.path.basename(f.name) + " - NaePad & Echo Code")

        else:
            self.save_as_file()

    def save_as_file(self, *args):
        self.curFilePath = filedialog.asksaveasfilename(defaultextension=".ech", filetypes=(("Text files", "*.txt"),("Echo Code files", "*.ech"),("All files", "*.*")))
        #Checks wether a file is selected or not
        if self.curFilePath:
            self.save_file()


    def cut(self):
        #Is anything selected?
        if self.text.tag_ranges(tk.SEL):
            self.text.clipboard_clear()
            #append to cleared clipboard the (selection)
            self.text.clipboard_append(self.text.get(tk.SEL_FIRST, tk. SEL_LAST))
            self.text.delete(tk.SEL_FIRST, tk. SEL_LAST)

    def copy(self):
        #Is anything selected?
        if self.text.tag_ranges(tk.SEL):
            self.text.clipboard_clear()
            #append to cleared clipboard the (selection)
            self.text.clipboard_append(self.text.get(tk.SEL_FIRST, tk. SEL_LAST))

    def paste(self):
        #Is anything selected?
        if self.text.tag_ranges(tk.SEL):
            #keeping a reference on where the selection starts
            selFirstIndex = self.text.index(tk.SEL_FIRST)
            #removing selection first
            self.text.delete(tk.SEL_FIRST, tk. SEL_LAST)
            #copying from clipboard
            self.text.insert(selFirstIndex, self.text.clipboard_get())

        else:
            self.text.insert(tk.INSERT, self.text.clipboard_get())

    def delete(self):
        #Is anything selected?
        if self.text.tag_ranges(tk.SEL):
            self.text.delete(tk.SEL_FIRST, tk. SEL_LAST)


#MainMenu object that contains Sub-menus
class MainMenu(tk.Menu):
    def __init__(self, master):
        super().__init__(master, tearoff=0)
        self.master = master

        #create Menu Options
        self.file = FileMenu(self)
        self.add_cascade(label="File", menu=self.file)

        self.edit = EditMenu(self)
        self.add_cascade(label="Edit", menu=self.edit)

        self.run = RunMenu(self)
        self.add_cascade(label="Run", menu=self.run)


#Menu class that handles File Operations
class FileMenu(tk.Menu):
    def __init__(self, master):
        super().__init__(master, tearoff=0)
        self.master = master

        self.add_command(label="New                Ctrl + N")
        self.add_command(label="Open...          Ctrl + O")
        self.add_command(label="Save               Ctrl + S")
        self.add_command(label="Save As...      Ctrl + Shift + S")


        #add the line before exit
        self.add_separator()
        #destroy's the grandparent, which is assumed to be a toplevel BAD NAE BAD
        self.add_command(label="Exit                 Alt + F4", command=lambda : master.master.save_before_leave(self.master.master.destroy))


#Menu class that handles editorial operations
class EditMenu(tk.Menu):
    def __init__(self, master):
        super().__init__(master, tearoff=0)

        self.add_command(label="Cut              Ctrl + X")
        self.add_command(label="Copy           Ctrl + C")
        self.add_command(label="Paste          Ctrl + V")
        self.add_command(label="Delete         Delete")

#Menu class that handles the run add_command
class RunMenu(tk.Menu):
    def __init__(self, master):
        super().__init__(master, tearoff=0)
        self.add_command(label="Run             F5")


#http://effbot.org/zone/tkinter-autoscrollbar.htm
class AutoScrollbar(tk.Scrollbar):
    # a scrollbar that hides itself if it's not needed.  only
    # works if you use the grid geometry manager.
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
        tk.Scrollbar.set(self, lo, hi)


def test():
    with open(__file__, "rU") as f:
        root.mainFrame.text.insert("1.0", f.read())


if __name__ == "__main__":
    root = MainWindow()
    #test()
    root.mainloop()
