import tkinter as tk


# Fonts
LargeFont = ('Alef', 20)
SmallFont = ('Alef', 12)
MenuFont = ('Alef', 8)


class ProgramGUI(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        self.title('FortniteSetUpTool')  # default title

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        frame = FrontPage(container, self)
        self.frames[FrontPage] = frame

        frame.grid(row=0, column=0, sticky="nsew")
        self.ShowPage(FrontPage)

    def ShowPage(self, page):

        frame = self.frames[page]
        frame.tkraise()

    def SetTitle(self, page_name):
        self.title('%s | FortniteToolSet' % page_name)


# default frame init for all pages in the program.
class DefaultPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg='#212121')


class FrontPage(DefaultPage):

    def __init__(self, parent, controller):
        DefaultPage.__init__(self, parent, controller)
        controller.SetTitle('Welcome')

        Title = tk.Label(self, text='FortniteToolSet', font=LargeFont)
        Title.pack(padx=10, pady=10)

        SmallerTitle = tk.Label(self, text='Created By RealA10N', font=SmallFont)
        SmallerTitle.pack(padx=10, pady=10)


root = ProgramGUI()
root.mainloop()


''' THE MENU BAR! COMING SOON (;

def AboutPopup():
    filewin = tk.Toplevel(root)
    button = tk.Button(filewin, text="About")
    button.pack()


root = tk.Tk()
menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="About", command=AboutPopup)

filemenu.add_separator()

filemenu.add_command(label="Exit", command=root.quit)

root.config(menu=menubar)
root.mainloop()
'''
