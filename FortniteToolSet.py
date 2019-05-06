import tkinter as tk
from tkinter import messagebox


# Fonts
LargeFont = ('Alef', 20)
SmallFont = ('Alef', 12)
MenuFont = ('Alef', 8)


class ProgramGUI(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        # place window on top & in the middle of the screen
        self.eval('tk::PlaceWindow %s center' % self.winfo_toplevel())

        self.title('FortniteSetUpTool')  # default title
        self.LoadMenuBar()

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.LoadAllPages(parent=container, controller=self)
        self.ShowPage(HomePage)

    def LoadAllPages(self, parent, controller):
        pages = (HomePage, AboutPage)  # all the pages list
        for frame_obj in pages:
            frame = frame_obj(parent, controller)
            self.frames[frame_obj] = frame

    def ShowPage(self, page):
        frame = self.frames[page]
        frame.ShowMe()
        frame.tkraise()

    def GetTitle(self, page_name):
        return '%s | FortniteToolSet' % page_name

    def LoadMenuBar(self):
        menubar = tk.Menu(self)
        program_menu = tk.Menu(menubar, tearoff=0)

        menubar.add_cascade(label="Program", menu=program_menu)
        program_menu.add_command(label="Home", command=lambda: self.ShowPage(HomePage))
        program_menu.add_command(label="About", command=lambda: self.ShowPage(AboutPage))

        program_menu.add_separator()

        program_menu.add_command(label="Exit", command=lambda: self.Quit())

        self.config(menu=menubar)

    def Quit(self):
        quit = tk.messagebox.askyesno(
            title=self.GetTitle('Warning!'),
            message="You are about to exit. Are you sure?")
        if quit:
            self.deiconify()
            self.destroy()
            self.quit()


class DefaultPage(tk.Frame):

    # default init for all pages in the program
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        tk.Frame.__init__(self, self.parent)
        self.configure(bg='#212121')
        self.grid(row=0, column=0, sticky="nsew")

    # will run every time the page loads
    def ShowMe(self):
        pass


class HomePage(DefaultPage):

    def __init__(self, parent, controller):
        DefaultPage.__init__(self, parent, controller)

        Title = tk.Label(self, text='FortniteToolSet', font=LargeFont)
        Title.pack(padx=10, pady=10)

        SmallerTitle = tk.Label(self, text='Created By RealA10N', font=SmallFont)
        SmallerTitle.pack(padx=10, pady=10)

    def ShowMe(self):
        self.controller.title(self.controller.GetTitle('Home'))


class AboutPage(DefaultPage):

    def __init__(self, parent, controller):
        DefaultPage.__init__(self, parent, controller)

        Title = tk.Label(self, text='About', font=LargeFont)
        Title.pack(padx=10, pady=10)

        SmallerTitle = tk.Label(self, text='yay!', font=SmallFont)
        SmallerTitle.pack(padx=10, pady=10)

    def ShowMe(self):
        self.controller.title(self.controller.GetTitle('About'))


root = ProgramGUI()
root.mainloop()
