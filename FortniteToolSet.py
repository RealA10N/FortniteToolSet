import tkinter as tk
from tkinter import messagebox as tkmsgbx
import os
from PIL import Image, ImageTk
from colour import Color


# # # # # # # #
# A S S E T S #
# # # # # # # #

AssetsFolder = os.path.join(os.getcwd(), 'FortniteToolSetAssets')
DefaultFont = 'Alef'

BigFontSize = 20
RegularFontSize = 12
SmallFontSize = 8

DefaultPad = 10

# # # # # # # # # # # # # # # # #
# C O L O R   F U N C T I O N S #
# # # # # # # # # # # # # # # # #


class MyColor(Color):

    def __init__(self, *args, **kwargs):

        Color.__init__(self, *args, **kwargs)

    def NewChangeColorLightning(self, amount):

        newr = min(self.red * amount, 1)
        newg = min(self.green * amount, 1)
        newb = min(self.blue * amount, 1)

        return MyColor(rgb=(newr, newg, newb))


# # # # # # # # # # # # # #
# C O L O R   A S S E T S #
# # # # # # # # # # # # # #

BackgroundColor = MyColor('#222831')   # the color of the window
BackgroudOppositeColor = MyColor('#FFFFFF')  # For items on background
TrailingColor = MyColor('#393e46')     # buttons, text fields etc.
DefaultTextColor = MyColor('#51afe1')  # most of the text
DrakTextColor = DefaultTextColor.NewChangeColorLightning(
    0.7)   # For smaller and less importent text
LightTextColor = DefaultTextColor.NewChangeColorLightning(1.3)  # For text that pops up
DiffrentColor = MyColor('#fd5f00')  # For special buttons and functions


# # # # # # # # # # # # #
# G E N E R A L   G U I #
# # # # # # # # # # # # #


class ProgramGUI(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        # place window on top & in the middle of the screen
        self.eval('tk::PlaceWindow %s' % self.winfo_toplevel())

        # not be able to resize
        self.resizable(False, False)

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
        pages = (HomePage, AboutPage, SettingsPage)  # all the pages list
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
        program_menu.add_command(label="Settings", command=lambda: self.ShowPage(SettingsPage))
        program_menu.add_command(label="About", command=lambda: self.ShowPage(AboutPage))

        program_menu.add_separator()

        program_menu.add_command(label="Exit", command=lambda: self.Quit())

        self.config(menu=menubar)

    def Quit(self):
        quit = tkmsgbx.askyesno(
            title=self.GetTitle('Warning!'),
            message="You are about to exit. Are you sure?")
        if quit:
            self.deiconify()
            self.destroy()
            self.quit()


# # # # # # # # # # #
# G U I   P A G E S #
# # # # # # # # # # #

class DefaultPage(tk.Frame):

    # default init for all pages in the program
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        tk.Frame.__init__(self, self.parent, bg=BackgroundColor.get_hex_l())
        self.grid(row=0, column=0, sticky="nsew")

    # will run every time the page loads
    def ShowMe(self):
        pass


class HomePage(DefaultPage):

    def __init__(self, parent, controller):
        DefaultPage.__init__(self, parent, controller)

        # banner image
        imgBanner = Image.open(os.path.join(AssetsFolder, 'Banner.png')).resize((500, 250))
        Banner = ImageCanvas(self, imgBanner)
        Banner.pack(padx=DefaultPad, pady=DefaultPad)

        WelcomeTitle = BigLabel(self, text='Welcome Back!')
        WelcomeTitle.pack(padx=DefaultPad, pady=DefaultPad)

    def ShowMe(self):
        self.controller.title(self.controller.GetTitle('Home'))


class AboutPage(DefaultPage):

    def __init__(self, parent, controller):
        DefaultPage.__init__(self, parent, controller)

        Title = tk.Label(self, text='About - coming soon!')
        Title.pack(padx=DefaultPad, pady=DefaultPad)

    def ShowMe(self):
        self.controller.title(self.controller.GetTitle('About'))


class SettingsPage(DefaultPage):

    def __init__(self, parent, controller):
        DefaultPage.__init__(self, parent, controller)

        TestEntry = RegularEntry(self)
        TestEntry.grid(row=0, column=0)

    def ShowMe(self):
        self.controller.title(self.controller.GetTitle('Settings'))


# # # # # # # # # # # # # #
# G U I   E L E M E N T S #
# # # # # # # # # # # # # #

# crates a transperent canvas and pastes image on it
class ImageCanvas(tk.Canvas):

    def __init__(self, master, pilImg, *args, **kwargs):

        self.pilImg = pilImg
        self.tkImg = ImageTk.PhotoImage(self.pilImg)
        width, height = pilImg.size

        tk.Canvas.__init__(self, master, bg=BackgroundColor.get_hex_l(), highlightthickness=0,
                           height=height, width=width, *args, **kwargs)

        self.create_image(0, 0, image=self.tkImg, anchor='nw')


class BigLabel(tk.Label):

    def __init__(self, master, *args, **kwargs):

        Font = (DefaultFont, BigFontSize)

        tk.Label.__init__(self, master, bg=BackgroundColor.get_hex_l(), font=Font,
                          fg=DiffrentColor.get_hex_l(), *args, **kwargs)


class RegularLabel(tk.Label):

    def __init__(self, master, *args, **kwargs):

        Font = (DefaultFont, RegularFontSize)

        tk.Label.__init__(self, master, bg=BackgroundColor.get_hex_l(), font=Font,
                          fg=DefaultTextColor.get_hex_l(), *args, **kwargs)


class SmallLabel(tk.Label):

    def __init__(self, master, *args, **kwargs):

        Font = (DefaultFont, SmallFontSize)

        tk.Label.__init__(self, master, bg=BackgroundColor.get_hex_l(), font=Font,
                          fg=DrakTextColor.get_hex_l(), *args, **kwargs)


class RegularEntry(tk.Entry):

    def __init__(self, master, *args, **kwargs):

        tk.Entry.__init__(self, master, bg=TrailingColor.get_hex_l(),
                          font=(DefaultFont, RegularFontSize),  # font
                          relief=tk.FLAT,  # style of the entry
                          bd=2,  # size of border
                          fg=BackgroudOppositeColor.get_hex_l(),  # color of font
                          selectbackground=DrakTextColor.get_hex_l(),  # background color when text selected
                          *args, **kwargs)


class RegularButton(tk.Button):

    def __init__(self, master, *args, **kwargs):

        tk.Button.__init__(self, master,

                           # button
                           bg=LightTextColor.get_hex_l(),  # regular color
                           activebackground=DrakTextColor.get_hex_l(),  # while pressed color
                           bd=0,  # size of border

                           # font
                           font=(DefaultFont, RegularFontSize),
                           fg=BackgroudOppositeColor.get_hex_l(),  # regular color
                           activeforeground=BackgroudOppositeColor.get_hex_l(),  # while pressed color
                           justify=tk.CENTER,  # center all the text lines
                           *args, **kwargs)


class SpecialButton(tk.Button):

    def __init__(self, master, *args, **kwargs):

        tk.Button.__init__(self, master,

                           # button
                           bg=DiffrentColor.get_hex_l(),  # regular color
                           activebackground=DrakTextColor.get_hex_l(),  # while pressed color
                           bd=0,  # size of border

                           # font
                           font=(DefaultFont, RegularFontSize),
                           fg=BackgroudOppositeColor.get_hex_l(),  # regular color
                           activeforeground=BackgroudOppositeColor.get_hex_l(),  # while pressed color
                           justify=tk.CENTER,  # center all the text lines
                           *args, **kwargs)


root = ProgramGUI()
root.mainloop()
