import tkinter as tk


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


class AboutPage(DefaultPage):

    def __init__(self, parent, controller):
        DefaultPage.__init__(self, parent, controller)

        Title = tk.Label(self, text='About', font=LargeFont)
        Title.pack(padx=10, pady=10)

        SmallerTitle = tk.Label(self, text='yay!', font=SmallFont)
        SmallerTitle.pack(padx=10, pady=10)

    def ShowMe(self):
        self.controller.title(self.controller.GetTitle('About'))


